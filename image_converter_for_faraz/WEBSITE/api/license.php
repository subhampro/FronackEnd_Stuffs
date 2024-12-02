<?php
header('Content-Type: application/json');
require_once '../config/config.php';

try {
    $data = json_decode(file_get_contents('php://input'), true);
    
    if (!isset($data['license_key']) || !isset($data['machine_id'])) {
        throw new Exception('Missing required parameters');
    }

    $license_key = $data['license_key'];
    $machine_id = $data['machine_id'];

    $db = new PDO(
        "mysql:host={$config['db']['host']};dbname={$config['db']['name']}",
        $config['db']['user'],
        $config['db']['pass'],
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );

    $stmt = $db->prepare("
        SELECT status, expires_at, machine_id 
        FROM licenses 
        WHERE license_key = ?
    ");
    
    $stmt->execute([$license_key]);
    $license = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$license) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid license key']);
        exit;
    }

    if ($license['status'] === 'expired' || strtotime($license['expires_at']) < time()) {
        http_response_code(400);
        echo json_encode(['error' => 'License has expired']);
        exit;
    }

    if ($license['status'] === 'unused') {
        // Activate license for this machine
        $stmt = $db->prepare("
            UPDATE licenses 
            SET status = 'active', 
                machine_id = ?,
                activated_at = CURRENT_TIMESTAMP 
            WHERE license_key = ?
        ");
        $stmt->execute([$machine_id, $license_key]);
    } else if ($license['machine_id'] && $license['machine_id'] !== $machine_id) {
        http_response_code(400);
        echo json_encode(['error' => 'License is already activated on another machine']);
        exit;
    }

    echo json_encode([
        'status' => 'valid',
        'expires_at' => $license['expires_at']
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Server error: ' . $e->getMessage()]);
}
