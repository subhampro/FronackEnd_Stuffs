
<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

try {
    $db = new PDO('mysql:host=localhost;dbname=wordpres_test', 'wordpres_test', '$$$Pro381998');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    echo "Database connection successful\n";
    
    $stmt = $db->query("SELECT COUNT(*) FROM users");
    echo "Total users: " . $stmt->fetchColumn() . "\n";
    
    $stmt = $db->query("SELECT COUNT(*) FROM usage_stats");
    echo "Total events: " . $stmt->fetchColumn() . "\n";
    
    echo "Recent events:\n";
    $stmt = $db->query("SELECT * FROM usage_stats ORDER BY created_at DESC LIMIT 5");
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        print_r($row);
    }
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}