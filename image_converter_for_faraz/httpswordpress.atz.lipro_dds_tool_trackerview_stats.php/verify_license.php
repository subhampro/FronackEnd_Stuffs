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
    ");
    $stmt->execute([$data['machine_id']]);
    
    // Then get or create trial license
    $stmt = $db->prepare("
        SELECT * FROM licenses 
        WHERE machine_id = ? 
        AND status = 'active'
    ");
    $stmt->execute([$data['machine_id']]);
    $license = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$license) {
        // Create new trial license
        $stmt = $db->prepare("
            INSERT INTO licenses (machine_id, created_at, activated_at, expires_at, status)
            VALUES (?, NOW(), NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), 'active')
        ");
        $stmt->execute([$data['machine_id']]);
        
        echo json_encode([
            'status' => 'valid',
            'type' => 'trial',
            'seconds_remaining' => 7 * 24 * 3600,
            'first_seen' => date('Y-m-d H:i:s')
        ]);
        exit;
    }
    
    // Return existing license info
    $seconds_remaining = strtotime($license['expires_at']) - time();
    echo json_encode([
        'status' => 'valid',
        'type' => 'trial',
        'seconds_remaining' => max(0, $seconds_remaining),
        'expires_at' => $license['expires_at']
    ]);

} catch (Exception $e) {
    error_log("License verification error: " . $e->getMessage());
    echo json_encode([
        'status' => 'error',
        'message' => 'Server error during verification'
    ]);
}