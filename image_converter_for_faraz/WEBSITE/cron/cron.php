
<?php
require_once '../api/cleanup.php';

// Set error reporting
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', '../logs/cron-error.log');

try {
    $cleaner = new FileCleanup();
    $cleaner->cleanup();
    file_put_contents('../logs/cron.log', date('Y-m-d H:i:s') . " - Cleanup completed\n", FILE_APPEND);
} catch (Exception $e) {
    error_log("Cleanup failed: " . $e->getMessage());
}