
<?php
require_once '../config/config.php';

class FileCleanup {
    private $dirs = ['../uploads/', '../converted/', '../temp/'];
    private $max_age = 3600; // 1 hour

    public function cleanup() {
        foreach ($this->dirs as $dir) {
            $this->cleanDirectory($dir);
        }
    }

    private function cleanDirectory($dir) {
        if (!is_dir($dir)) return;
        
        $files = glob($dir . '*');
        $now = time();

        foreach ($files as $file) {
            if (is_file($file) && ($now - filemtime($file) > $this->max_age)) {
                unlink($file);
            }
        }
    }
}

// Run cleanup
$cleaner = new FileCleanup();
$cleaner->cleanup();