<?php
require_once '../config/config.php';

class ImageConverter {
    private $allowed_formats = ['dds', 'png', 'jpg'];
    private $max_file_size = 10485760; // 10MB
    private $upload_dir = '../uploads/';
    private $output_dir = '../converted/';

    public function __construct() {
        $this->ensureDirectoriesExist();
    }

    private function ensureDirectoriesExist() {
        foreach ([$this->upload_dir, $this->output_dir] as $dir) {
            if (!file_exists($dir)) {
                mkdir($dir, 0755, true);
            }
        }
    }

    public function handleRequest() {
        try {
            $this->validateRequest();
            $file = $this->processUpload();
            $output = $this->convertImage($file);
            $this->sendResponse($output);
        } catch (Exception $e) {
            http_response_code(400);
            echo json_encode(['error' => $e->getMessage()]);
        }
    }

    private function validateRequest() {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            throw new Exception('Invalid request method');
        }

        if (!isset($_FILES['file'])) {
            throw new Exception('No file uploaded');
        }

        if ($_FILES['file']['size'] > $this->max_file_size) {
            throw new Exception('File too large');
        }
    }

    private function processUpload() {
        $temp_name = $_FILES['file']['tmp_name'];
        $name = basename($_FILES['file']['name']);
        $upload_path = $this->upload_dir . uniqid() . '_' . $name;
        
        if (!move_uploaded_file($temp_name, $upload_path)) {
            throw new Exception('Failed to save uploaded file');
        }
        
        return $upload_path;
    }

    private function convertImage($input_file) {
        $format = $_POST['format'] ?? 'dds';
        $output_file = $this->output_dir . uniqid() . '.' . $format;

        if ($format === 'dds') {
            $this->convertToDDS($input_file, $output_file);
        } else {
            $this->convertFromDDS($input_file, $output_file, $format);
        }

        return $output_file;
    }

    private function convertToDDS($input, $output) {
        $command = sprintf(
            'magick convert %s -define dds:compression=dxt5 %s',
            escapeshellarg($input),
            escapeshellarg($output)
        );
        
        exec($command, $output, $return_var);
        if ($return_var !== 0) {
            throw new Exception('DDS conversion failed');
        }
    }

    private function convertFromDDS($input, $output, $format) {
        $command = sprintf(
            'magick convert %s %s',
            escapeshellarg($input),
            escapeshellarg($output)
        );
        
        exec($command, $output, $return_var);
        if ($return_var !== 0) {
            throw new Exception('Image conversion failed');
        }
    }

    private function validateLicense($license_key) {
        global $config;
        
        $stmt = $this->db->prepare("
            SELECT status, expires_at 
            FROM licenses 
            WHERE license_key = ? 
            AND status = 'active'
        ");
        
        $stmt->execute([$license_key]);
        $license = $stmt->fetch();
        
        if (!$license || strtotime($license['expires_at']) < time()) {
            throw new Exception('Invalid or expired license');
        }
    }

    private function sendResponse($file_path) {
        if (!file_exists($file_path)) {
            throw new Exception('Converted file not found');
        }

        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . basename($file_path) . '"');
        readfile($file_path);
    }
}

$converter = new ImageConverter();
$converter->handleRequest();