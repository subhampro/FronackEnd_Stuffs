<?php
$base_path = '/home/wordpres/public_html/pro-dds-tool';

return [
    'db' => [
        'host' => 'localhost',
        'name' => 'wordpres_test',
        'user' => 'wordpres_test',
        'pass' => '$$$Pro381998'
    ],
    'settings' => [
        'max_file_size' => 10 * 1024 * 1024, // 10MB
        'allowed_formats' => ['dds', 'png', 'jpg'],
        'base_url' => 'https://wordpress.atz.li/pro-dds-tool',
        'temp_dir' => $base_path . '/temp/',
        'output_dir' => $base_path . '/converted/',
        'upload_dir' => $base_path . '/uploads/',
        'log_dir' => $base_path . '/logs/'
    ],
    'security' => [
        'rate_limit' => 100, // requests per hour
        'allowed_origins' => ['wordpress.atz.li']
    ]
];