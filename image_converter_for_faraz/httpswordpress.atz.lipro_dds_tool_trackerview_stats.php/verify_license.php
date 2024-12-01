<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

error_log("Verify license accessed");

$raw_data = file_get_contents('php://input');
error_log("Raw data received: " . $raw_data);

$data = json_decode($raw_data, true);

try {
    require_once __DIR__ . '/db_connect.php';
    
    // Add rate limiting
    $ip = $_SERVER['REMOTE_ADDR'];
    $rate_limit_key = "rate_limit:$ip";
    
    // Simple rate limiting using file system
    $rate_limit_file = sys_get_temp_dir() . "/$rate_limit_key";
    if (file_exists($rate_limit_file) && (time() - filemtime($rate_limit_file)) < 1) {
        throw new Exception("Rate limit exceeded");
    }
    touch($rate_limit_file);
    
    // Add request logging
    error_log("License verification request from: " . $_SERVER['REMOTE_ADDR']);
    
    if (!$data || !isset($data['machine_id'])) {
        throw new Exception("Invalid request data");
    }

    // Add response delay to prevent hammering
    usleep(100000); // 100ms delay
    
    // First check if user exists, if not create trial
    $stmt = $db->prepare("
        INSERT IGNORE INTO users (user_id, first_seen, last_seen)
        VALUES (?, NOW(), NOW())
        ON DUPLICATE KEY UPDATE last_seen = NOW()
    ");
    $stmt->execute([$data['machine_id']]);
    
    // Get user info including trial status
    $stmt = $db->prepare("
        SELECT 
            u.*,
            l.status as license_status,
            l.expires_at as license_expires,
            CASE 
                WHEN l.status = 'active' THEN 'licensed'
                WHEN l.id IS NULL AND TIMESTAMPDIFF(DAY, u.first_seen, NOW()) <= 7 THEN 'trial'
                WHEN l.status = 'expired' THEN 'expired'
                ELSE 'trial_expired'
            END as user_status,
            COALESCE(
                l.expires_at,
                DATE_ADD(u.first_seen, INTERVAL 7 DAY)
            ) as effective_expiry
        FROM users u
        LEFT JOIN licenses l ON u.user_id = l.machine_id
        WHERE u.user_id = ?
    ");
    $stmt->execute([$data['machine_id']]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$user) {
        throw new Exception("User not found");
    }
    
    $now = new DateTime();
    $expiry = new DateTime($user['effective_expiry']);
    $interval = $now->diff($expiry);
    $seconds_remaining = max(0, $expiry->getTimestamp() - $now->getTimestamp());
    
    // Try to update last check time if column exists
    try {
        $stmt = $db->prepare("UPDATE users SET last_check = NOW() WHERE user_id = ?");
        $stmt->execute([$data['machine_id']]);
    } catch (PDOException $e) {
        // Ignore error if column doesn't exist
        error_log("Warning: Could not update last_check time: " . $e->getMessage());
    }
    
    echo json_encode([
        'status' => 'valid',
        'type' => $user['license_status'] == 'active' ? 'licensed' : 'trial',
        'seconds_remaining' => $seconds_remaining,
        'user_status' => $user['user_status'],
        'expires_at' => $user['effective_expiry']
    ]);

} catch (Exception $e) {
    error_log("License verification error: " . $e->getMessage());
    http_response_code($e->getMessage() === "Rate limit exceeded" ? 429 : 500);
    echo json_encode([
        'status' => 'error',
        'message' => $e->getMessage(),
        'retry_after' => 1
    ]);
}