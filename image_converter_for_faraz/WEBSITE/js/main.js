class DDSConverter {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.convertBtn = document.getElementById('convertBtn');
        this.progress = document.getElementById('progress');
        this.result = document.getElementById('result');
        
        this.licenseKey = localStorage.getItem('licenseKey');
        this.apiBase = 'https://wordpress.atz.li/pro-dds-tool/api';

        this.initializeEventListeners();
        this.validateLicense();
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
        const licenseKey = localStorage.getItem('licenseKey');
        const machineId = this.getMachineId();

        if (!licenseKey) {
            this.showLicensePrompt();
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/license.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    license_key: licenseKey,
                    machine_id: machineId
                })
            });

            const data = await response.json();

            if (!response.ok || data.error) {
                throw new Error(data.error || 'License validation failed');
            }

            this.enableConverter();
            this.updateLicenseStatus('License valid', false);
        } catch (error) {
            this.updateLicenseStatus(error.message, true);
            localStorage.removeItem('licenseKey');
            this.showLicensePrompt();
        }
    }

    updateLicenseStatus(message, isError = false) {
        const statusElement = document.getElementById('licenseStatus');
        statusElement.textContent = message;
        statusElement.className = `license-status ${isError ? 'license-invalid' : ''}`;
    }

    showLicensePrompt() {
        const dialog = document.createElement('div');
        dialog.className = 'license-dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <h3>Enter License Key</h3>
                <input type="text" id="licenseInput" placeholder="XXXXX-XXXXX-XXXXX"/>
                <div class="error-message" style="display:none; color:red;"></div>
                <button id="submitLicense">Activate</button>
            </div>
        `;

        document.body.appendChild(dialog);

        const submitBtn = dialog.querySelector('#submitLicense');
        const licenseInput = dialog.querySelector('#licenseInput');
        const errorMsg = dialog.querySelector('.error-message');

        submitBtn.addEventListener('click', async () => {
            const license = licenseInput.value.trim();
            if (!license) {
                errorMsg.textContent = 'Please enter a license key';
                errorMsg.style.display = 'block';
                return;
            }

            try {
                const response = await fetch(`${this.apiBase}/license.php`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        license_key: license,
                        machine_id: this.getMachineId()
                    })
                });

                const data = await response.json();

                if (!response.ok || data.error) {
                    throw new Error(data.error || 'Invalid license key');
                }

                localStorage.setItem('licenseKey', license);
                dialog.remove();
                this.enableConverter();
                this.updateLicenseStatus('License valid', false);
            } catch (error) {
                errorMsg.textContent = error.message;
                errorMsg.style.display = 'block';
            }
        });
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
            const response = await fetch(`${this.apiBase}/convert.php`, {
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