// Import Vue (make sure this is at the top)
import Vue from 'vue';

// Configuration
const GuideConfig = {
    activeTheme: 'dark',
    themes: {
        dark: {
            background: '#1a1a1a',
            text: '#ffffff',
            border: '#333333',
            inputBackground: '#2a2a2a',
            accent: '#4a90e2',
            error: '#ff4444',
            success: '#4caf50'
        },
        light: {
            background: '#ffffff',
            text: '#000000',
            border: '#dddddd',
            inputBackground: '#f5f5f5',
            accent: '#2196f3',
            error: '#f44336',
            success: '#4caf50'
        },
        twilight: {
            background: '#2c2f33',
            text: '#99aab5',
            border: '#23272a',
            inputBackground: '#36393f',
            accent: '#7289da',
            error: '#dc3545',
            success: '#43b581'
        },
        cyber: {
            background: '#000000',
            text: '#00ff00',
            border: '#008000',
            inputBackground: '#002200',
            accent: '#00ff00',
            error: '#ff0000',
            success: '#00ff00'
        },
        neon: {
            background: '#0a0a0a',
            text: '#ff00ff',
            border: '#ff00ff',
            inputBackground: '#1a1a1a',
            accent: '#00ffff',
            error: '#ff0000',
            success: '#00ff00'
        },
        azure: {
            background: '#f0f8ff',
            text: '#000080',
            border: '#87ceeb',
            inputBackground: '#e6f3ff',
            accent: '#1e90ff',
            error: '#dc143c',
            success: '#32cd32'
        }
    }
};

// Search Component
const search = {
    data() {
        return {
            query: '',
            results: [],
            isSearching: false
        }
    },
    methods: {
        async searchContent() {
            if (!this.query) {
                this.results = [];
                return;
            }
            
            this.isSearching = true;
            const response = await fetch(`https://${GetParentResourceName()}/searchContent`, {
                method: 'POST',
                body: JSON.stringify({ query: this.query })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.results = data.results;
            }
            
            this.isSearching = false;
        }
    },
    watch: {
        query: {
            handler: 'searchContent',
            debounce: 300
        }
    }
};

// Point Manager Component
const pointManager = {
    data() {
        return {
            points: [],
            editing: null,
            types: ['marker', '3dtext'],
            selectedType: 'marker'
        }
    },
    methods: {
        async createPoint(point) {
            const response = await fetch(`https://${GetParentResourceName()}/createPoint`, {
                method: 'POST',
                body: JSON.stringify(point)
            });
            if (response.ok) {
                this.points.push(point);
                ShowNotification(Locales[Config.Locale]['point_created']);
            }
        },
        async deletePoint(pointId) {
            const response = await fetch(`https://${GetParentResourceName()}/deletePoint`, {
                method: 'POST',
                body: JSON.stringify({id: pointId})
            });
            if (response.ok) {
                this.points = this.points.filter(p => p.id !== pointId);
                ShowNotification(Locales[Config.Locale]['point_deleted']);
            }
        }
    }
};

// Permission Manager Component
const permissionManager = {
    data() {
        return {
            jobs: [],
            grades: {},
            selectedJob: null,
            selectedGrade: null,
            permissions: []
        }
    },
    methods: {
        async fetchJobs() {
            const response = await fetch(`https://${GetParentResourceName()}/getJobs`);
            if (response.ok) {
                const data = await response.json();
                this.jobs = data.jobs;
                this.grades = data.grades;
            }
        },
        
        addPermission() {
            if (!this.selectedJob || !this.selectedGrade) return;
            
            this.permissions.push({
                job: this.selectedJob,
                grade: this.selectedGrade
            });
            
            this.selectedJob = null;
            this.selectedGrade = null;
        },
        
        removePermission(index) {
            this.permissions.splice(index, 1);
        },
        
        getPermissions() {
            return this.permissions;
        }
    },
    mounted() {
        this.fetchJobs();
    }
};

// Editor Component
const editor = {
    data() {
        return {
            content: '',
            tools: ['bold', 'italic', 'image', 'video', 'link', 'list', 'header'],
            selectedTool: null
        }
    },
    methods: {
        applyFormat(tool) {
            switch(tool) {
                case 'bold':
                    document.execCommand('bold', false, null);
                    break;
                case 'italic':
                    document.execCommand('italic', false, null);
                    break;
                case 'image':
                    const imageUrl = prompt('Enter image URL:');
                    if (imageUrl) {
                        document.execCommand('insertImage', false, imageUrl);
                    }
                    break;
            }
        },
        
        insertList() {
            document.execCommand('insertUnorderedList', false, null);
        },
        
        insertHeader() {
            document.execCommand('formatBlock', false, '<h2>');
        },
        
        insertVideo() {
            const videoUrl = prompt('Enter video URL:');
            if (videoUrl) {
                const videoEmbed = `<div class="video-container"><iframe src="${videoUrl}" frameborder="0" allowfullscreen></iframe></div>`;
                document.execCommand('insertHTML', false, videoEmbed);
            }
        },
        
        getContent() {
            return this.$refs.editable.innerHTML;
        },

        setContent(html) {
            this.$refs.editable.innerHTML = html;
        }
    }
};

// Main App Component
const app = {
    data() {
        return {
            visible: false,
            searchQuery: '',
            selectedTheme: 'dark',
            themes: [
                { name: 'dark', label: 'Dark' },
                { name: 'light', label: 'Light' },
                { name: 'twilight', label: 'Twilight' },
                { name: 'cyber', label: 'Cyber' },
                { name: 'neon', label: 'Neon' },
                { name: 'azure', label: 'Azure' }
            ],
            categories: [],
            pages: [],
            activePage: null
        }
    },
    mounted() {
        window.addEventListener('message', this.handleMessage);
        this.setTheme(this.selectedTheme);
    },
    methods: {
        handleMessage(event) {
            const data = event.data;
            if (data.type === 'openGuidebook') {
                this.visible = true;
                if (data.page) {
                    this.openPage(data.page);
                }
            }
        },
        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
        },
        closeGuidebook() {
            this.visible = false;
            fetch(`https://${GetParentResourceName()}/closeguidebook`, {
                method: 'POST',
                body: JSON.stringify({})
            });
        }
    },
    watch: {
        selectedTheme(newTheme) {
            this.setTheme(newTheme);
        }
    }
};

// Admin Panel Component
const adminPanel = {
    data() {
        return {
            categories: [],
            pages: [],
            points: [],
            editing: {
                category: null,
                page: null,
                point: null
            },
            jobs: [],
            selectedPermissions: []
        }
    },
    methods: {
        async saveCategory(category) {
            const response = await fetch(`https://${GetParentResourceName()}/saveCategory`, {
                method: 'POST',
                body: JSON.stringify(category)
            });
            if (response.ok) {
                this.editing.category = null;
                this.fetchCategories();
            }
        },
        async savePage(page) {
            const response = await fetch(`https://${GetParentResourceName()}/savePage`, {
                method: 'POST',
                body: JSON.stringify(page)
            });
            if (response.ok) {
                this.editing.page = null;
                this.fetchPages();
            }
        },
        async savePoint(point) {
            const response = await fetch(`https://${GetParentResourceName()}/savePoint`, {
                method: 'POST',
                body: JSON.stringify(point)
            });
            if (response.ok) {
                this.editing.point = null;
                this.fetchPoints();
            }
        }
    }
};

// Initialize all components in a single place
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main app
    Vue.createApp(app).mount('#guidebook');
    
    // Initialize admin components
    Vue.createApp(adminPanel).mount('#admin-panel');
    Vue.createApp(permissionManager).mount('#permission-manager');
    Vue.createApp(pointManager).mount('#point-manager');
    
    // Initialize editor
    Vue.createApp(editor).mount('#page-editor');
    
    // Initialize search
    Vue.createApp(search).mount('#search-component');
});

// Export config for modules that need it
export { GuideConfig as default };