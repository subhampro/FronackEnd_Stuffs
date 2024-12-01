<?php
header('Content-Type: application/json');

try {
    $db = new PDO('mysql:host=localhost;dbname=wordpres_test', 'wordpres_test', '$$$Pro381998');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo json_encode(['status' => 'ok', 'message' => 'Database connection successful']);
} catch (PDOException $e) {
    echo json_encode(['status' => 'error', 'message' => 'Database connection failed: ' . $e->getMessage()]);
}