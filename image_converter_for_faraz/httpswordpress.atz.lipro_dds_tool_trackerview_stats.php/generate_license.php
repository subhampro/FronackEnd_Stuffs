<?php
function generate_license_key() {
    return strtoupper(substr(hash('sha256', uniqid(rand(), true)), 0, 16));
}

try {
    $key = generate_license_key();
    $stmt = $db->prepare("INSERT INTO licenses (license_key) VALUES (?)");
    $stmt->execute([$key]);
    echo "Generated license key: " . $key;
} catch (Exception $e) {
    echo "Error generating license: " . $e->getMessage();
}