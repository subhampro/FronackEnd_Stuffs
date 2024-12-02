
<?php
return [
    'settings' => [
        'max_file_size' => 10 * 1024 * 1024, // 10MB
        'allowed_formats' => ['dds', 'png', 'jpg'],
        'temp_dir' => '../temp/',
        'output_dir' => '../converted/'
    ],
    'security' => [
        'rate_limit' => 100, // requests per hour
        'allowed_origins' => ['https://wordpress.atz.li']
    ]
];