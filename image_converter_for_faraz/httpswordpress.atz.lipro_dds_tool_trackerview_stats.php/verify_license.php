<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

require_once __DIR__ . '/db_connect.php';

$data = json_decode(file_get_contents('php://input'), true);

if (!$data || !isset($data['machine_id'])) {
    exit(json_encode(['status' => 'error', 'message' => 'Invalid request data']));
}

try {
    // First check for full license
    $stmt = $db->prepare("
        SELECT 
            l.*,
            TIMESTAMPDIFF(SECOND, NOW(), l.expires_at) as seconds_remaining
        FROM licenses l
        WHERE l.machine_id = ? AND l.status = 'active'
    ");
    $stmt->execute([$data['machine_id']]);
    $license = $stmt->fetch(PDO::FETCH_ASSOC);

    // If no active license, check trial status
    if (!$license) {
        $stmt = $db->prepare("
            SELECT 
                u.first_seen,
                TIMESTAMPDIFF(SECOND, NOW(), DATE_ADD(u.first_seen, INTERVAL 7 DAY)) as trial_remaining
            FROM users u
            WHERE u.user_id = ?
        ");
        $stmt->execute([$data['machine_id']]);
        $trial = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($trial && $trial['trial_remaining'] > 0) {
            echo json_encode([
                'status' => 'valid',
                'type' => 'trial',
                'seconds_remaining' => $trial['trial_remaining'],
                'first_seen' => $trial['first_seen']
            ]);
            exit;
        }
        
        if ($trial) {
            echo json_encode([
                'status' => 'expired',
                'message' => 'Trial period has expired'
            ]);
        } else {
            // New user - start trial
            echo json_encode([
                'status' => 'valid',
                'type' => 'trial',
                'seconds_remaining' => 7 * 24 * 3600,
                'first_seen' => date('Y-m-d H:i:s')
            ]);
        }
        exit;
    }

    echo json_encode([
        'status' => 'valid',
        'type' => 'full',
        'seconds_remaining' => $license['seconds_remaining'],
        'expires_at' => $license['expires_at']
    ]);

} catch (Exception $e) {
    error_log("License verification error: " . $e->getMessage());
    echo json_encode([
        'status' => 'error',
        'message' => 'Server error during verification'
    ]);
}