<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

error_log("Verify license accessed");

$raw_data = file_get_contents('php://input');
error_log("Raw data received: " . $raw_data);

$data = json_decode($raw_data, true);

if (!$data || !isset($data['machine_id'])) {
    error_log("Invalid request data: " . print_r($data, true));
    exit(json_encode([
        'status' => 'error', 
        'message' => 'Invalid request data',
        'debug' => ['raw_data' => $raw_data]
    ]));
}

try {
    require_once __DIR__ . '/db_connect.php';
    
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
            GREATEST(
                COALESCE(l.expires_at, DATE_ADD(u.first_seen, INTERVAL 7 DAY)),
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
    $seconds_remaining = $expiry->getTimestamp() - $now->getTimestamp();
    
    // Update last check time
    $stmt = $db->prepare("UPDATE users SET last_check = NOW() WHERE user_id = ?");
    $stmt->execute([$data['machine_id']]);
    
    echo json_encode([
        'status' => 'valid',
        'type' => $user['license_status'] == 'active' ? 'licensed' : 'trial',
        'seconds_remaining' => max(0, $seconds_remaining),
        'user_status' => $user['user_status'],
        'expires_at' => $user['effective_expiry']
    ]);

} catch (Exception $e) {
    error_log("License verification error: " . $e->getMessage());
    echo json_encode([
        'status' => 'error',
        'message' => 'Server error during verification'
    ]);
}