class DDSConverter {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.convertBtn = document.getElementById('convertBtn');
        this.progress = document.getElementById('progress');
        this.result = document.getElementById('result');
        
        this.licenseKey = localStorage.getItem('licenseKey');
        this.validateLicense();

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.dropZone.addEventListener('drop', this.handleDrop.bind(this));
        this.dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        this.convertBtn.addEventListener('click', this.handleConvert.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        this.dropZone.classList.add('drop-zone--over');
    }

    handleDrop(e) {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) {
            this.fileInput.files = e.dataTransfer.files;
            this.handleFileSelect();
        }
    }

    handleFileSelect() {
        this.convertBtn.disabled = !this.fileInput.files.length;
    }

    async validateLicense() {
        if (!this.licenseKey) {
            this.showLicensePrompt();
            return;
        }

        try {
            const response = await fetch('/api/license.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    license_key: this.licenseKey,
                    machine_id: this.getMachineId()
                })
            });

            if (!response.ok) {
                throw new Error('Invalid license');
            }

            this.enableConverter();
        } catch (error) {
            this.showLicensePrompt();
        }
    }

    showLicensePrompt() {
        const license = prompt('Please enter your license key:');
        if (license) {
            this.licenseKey = license;
            localStorage.setItem('licenseKey', license);
            this.validateLicense();
        }
    }

    getMachineId() {
        const platform = navigator.platform;
        const userAgent = navigator.userAgent;
        const language = navigator.language;
        const fingerprint = `${platform}-${userAgent}-${language}`;
        return btoa(fingerprint).substring(0, 32);
    }

    enableConverter() {
        this.dropZone.style.opacity = '1';
        this.dropZone.style.pointerEvents = 'auto';
    }

    async handleConvert() {
        if (!this.licenseKey) {
            this.showLicensePrompt();
            return;
        }
        
        const file = this.fileInput.files[0];
        const format = document.getElementById('formatSelect').value;
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('format', format);

        this.progress.classList.remove('hidden');
        try {
            const response = await fetch('/api/convert.php', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Conversion failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            
            this.result.innerHTML = `
                <a href="${url}" download="converted.${format}">
                    Download Converted File
                </a>
            `;
            this.result.classList.remove('hidden');
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            this.progress.classList.add('hidden');
        }
    }
}

new DDSConverter();