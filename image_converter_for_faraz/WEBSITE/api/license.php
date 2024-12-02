<?php
header('Content-Type: application/json');
require_once '../config/config.php';

class LicenseValidator {
    private $db;
    private $config;

    public function __construct() {
        $this->config = require '../config/config.php';
        $this->connectDB();
    }

    private function connectDB() {
        try {
            $this->db = new PDO(
                "mysql:host={$this->config['db']['host']};dbname={$this->config['db']['name']}",
                $this->config['db']['user'],
                $this->config['db']['pass']
            );
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            $this->sendError('Database connection failed');
        }
    }

    public function validateLicense() {
        try {
            $data = json_decode(file_get_contents('php://input'), true);
            
            if (!isset($data['license_key'])) {
                $this->sendError('Missing license key');
            }

            $license_key = $data['license_key'];
            
            // Query matches your actual database structure
            $stmt = $this->db->prepare("
                SELECT * FROM licenses 
                WHERE license_key = ? 
                AND status != 'expired'
            ");
            
            $stmt->execute([$license_key]);
            $license = $stmt->fetch(PDO::FETCH_ASSOC);

            if (!$license) {
                $this->sendError('Invalid license key');
            }

            // Check expiration
            if ($license['expires_at'] && strtotime($license['expires_at']) < time()) {
                // Update status to expired
                $updateStmt = $this->db->prepare("
                    UPDATE licenses 
                    SET status = 'expired' 
                    WHERE license_key = ?
                ");
                $updateStmt->execute([$license_key]);
                $this->sendError('License has expired');
            }

            if ($license['status'] === 'unused') {
                // Activate the license
                $updateStmt = $this->db->prepare("
                    UPDATE licenses 
                    SET status = 'active',
                        activated_at = NOW()
                    WHERE license_key = ?
                ");
                $updateStmt->execute([$license_key]);
            }

            $this->sendSuccess($license);

        } catch (Exception $e) {
            $this->sendError('License validation failed: ' . $e->getMessage());
        }
    }

    private function countActivations($license_id) {
        $stmt = $this->db->prepare("
            SELECT COUNT(*) FROM machine_activations 
            WHERE license_id = ?
        ");
        $stmt->execute([$license_id]);
        return $stmt->fetchColumn();
    }

    private function activateMachine($license_id, $machine_id) {
        $stmt = $this->db->prepare("
            INSERT INTO machine_activations (license_id, machine_id, activated_at)
            VALUES (?, ?, NOW())
        ");
        $stmt->execute([$license_id, $machine_id]);
    }

    private function sendError($message) {
        echo json_encode([
            'status' => 'error',
            'message' => $message
        ]);
        exit;
    }

    private function sendSuccess($license) {
        echo json_encode([
            'status' => 'valid',
            'type' => 'full', // You can modify this based on your needs
            'expires_at' => $license['expires_at'],
            'message' => 'License validated successfully'
        ]);
        exit;
    }
}

$validator = new LicenseValidator();
$validator->validateLicense();
