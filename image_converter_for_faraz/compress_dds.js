const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

async function convertImage(inputPath) {
    // Validate file exists
    if (!fs.existsSync(inputPath)) {
        console.error('Error: Input file does not exist');
        return;
    }

    // Check if file is an image
    const validExtensions = ['.png', '.jpg', '.jpeg', '.webp', '.tiff', '.gif'];
    const ext = path.extname(inputPath).toLowerCase();
    if (!validExtensions.includes(ext)) {
        console.error('Error: File must be a valid image format:', validExtensions.join(', '));
        return;
    }

    const outputPath = path.join(
        path.dirname(inputPath),
        `${path.basename(inputPath, ext)}_processed.png`
    );

    try {
        // Convert to high-quality PNG
        await sharp(inputPath)
            .png({
                quality: 100,
                compressionLevel: 9
            })
            .toFile(outputPath);

        console.log(`Successfully saved as PNG: ${outputPath}`);
        console.log('Note: To convert to DDS, you will need to use a DDS conversion tool like:');
        console.log('- texconv (DirectXTex)')
        console.log('- ImageMagick with DDS plugin');
        console.log('- NVIDIA Texture Tools');
    } catch (error) {
        console.error('Error during conversion:', error);
    }
}

// Get the file path from command line arguments
const filePath = process.argv[2];
if (!filePath) {
    console.error('Please provide an image file path');
    process.exit(1);
}

convertImage(filePath);
