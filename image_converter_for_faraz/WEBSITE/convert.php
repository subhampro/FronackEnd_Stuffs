
<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    die(json_encode(['success' => false, 'error' => 'Invalid request method']));
}

if (!isset($_FILES['image']) || !isset($_POST['compression'])) {
    die(json_encode(['success' => false, 'error' => 'Missing required fields']));
}

$uploadDir = 'uploads/';
if (!file_exists($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

$tempFile = $_FILES['image']['tmp_name'];
$originalName = pathinfo($_FILES['image']['name'], PATHINFO_FILENAME);
$compression = $_POST['compression'];
$outputFile = $uploadDir . $originalName . '.dds';

// Path to texconv executable (you'll need to upload this to your hosting)
$texconv = './texconv.exe';

// Compression format mapping
$compressionFlags = [
    'bc7' => '-f BC7_UNORM',
    'bc3' => '-f BC3_UNORM',
    'bc1' => '-f BC1_UNORM',
    'none' => '-f R8G8B8A8_UNORM'
];

$flag = $compressionFlags[$compression] ?? $compressionFlags['none'];

// Execute conversion
$command = "$texconv -nologo $flag -y -o $uploadDir $tempFile";
exec($command, $output, $returnCode);

if ($returnCode === 0) {
    $downloadUrl = $uploadDir . basename($outputFile);
    echo json_encode([
        'success' => true,
        'downloadUrl' => $downloadUrl
    ]);
} else {
    echo json_encode([
        'success' => false,
        'error' => 'Conversion failed'
    ]);
}
?>