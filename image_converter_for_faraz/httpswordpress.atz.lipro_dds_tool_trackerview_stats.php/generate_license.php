<?php
function generate_license_key() {
    return strtoupper(substr(hash('sha256', uniqid(rand(), true)), 0, 16));
}

try {
    $key = generate_license_key();
    $stmt = $db->prepare("INSERT INTO licenses (license_key, created_at, expires_at) VALUES (?, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY))");
    $stmt->execute([$key]);
    echo "Generated license key: " . $key . "\nExpires in 30 days from activation.";
} catch (Exception $e) {
    echo "Error generating license: " . $e->getMessage();
}