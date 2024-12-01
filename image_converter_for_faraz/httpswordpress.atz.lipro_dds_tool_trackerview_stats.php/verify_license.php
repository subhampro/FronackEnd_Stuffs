<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Add at the top, before other code
if (!file_exists(__DIR__ . '/db_connect.php')) {
    die(json_encode(['status' => 'error', 'message' => 'Database configuration missing']));
}
require_once __DIR__ . '/db_connect.php';

$data = json_decode(file_get_contents('php://input'), true);

if (!$data || !isset($data['machine_id'])) {
    exit(json_encode(['status' => 'error', 'message' => 'Invalid request data']));
}

$machine_id = $data['machine_id'];

try {
    $stmt = $db->prepare("
        SELECT l.*, 
               TIMESTAMPDIFF(SECOND, NOW(), l.expires_at) as seconds_remaining,
               CASE 
                   WHEN l.status = 'active' AND l.expires_at > NOW() THEN 'valid'
                   ELSE l.status
               END as current_status
        FROM licenses l
        WHERE l.machine_id = ?
    ");
    $stmt->execute([$machine_id]);
    $license = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($license && $license['current_status'] === 'valid') {
        $remaining = max(0, $license['seconds_remaining']);
        echo json_encode([
            'status' => 'valid',
            'type' => 'full',
            'expires_at' => $license['expires_at'],
            'remaining' => [
                'days' => floor($remaining / 86400),
                'hours' => floor(($remaining % 86400) / 3600),
                'minutes' => floor(($remaining % 3600) / 60)
            ]
        ]);
        exit;
    }
    
    // Check for trial period
    $stmt = $db->prepare("
        SELECT 
            MIN(created_at) as first_use,
            TIMESTAMPDIFF(SECOND, NOW(), DATE_ADD(MIN(created_at), INTERVAL 7 DAY)) as trial_remaining
        FROM usage_stats 
        WHERE user_id = ?
    ");
    $stmt->execute([$machine_id]);
    $trial = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($trial && $trial['trial_remaining'] > 0) {
        $remaining = max(0, $trial['trial_remaining']);
        echo json_encode([
            'status' => 'valid',
            'type' => 'trial',
            'remaining' => [
                'days' => floor($remaining / 86400),
                'hours' => floor(($remaining % 86400) / 3600),
                'minutes' => floor(($remaining % 3600) / 60)
            ]
        ]);
        exit;
    }
    
    // Trial or license expired
    if ($trial) {
        echo json_encode([
            'status' => 'expired',
            'message' => 'Trial period has expired. Please activate a license to continue.'
        ]);
    } else {
        echo json_encode([
            'status' => 'valid',
            'type' => 'trial',
            'remaining' => [
                'days' => 7,
                'hours' => 0,
                'minutes' => 0
            ]
        ]);
    }
    
} catch (Exception $e) {
    error_log("License verification error: " . $e->getMessage());
    echo json_encode([
        'status' => 'error',
        'message' => 'Verification failed. Please try again later.'
    ]);
}