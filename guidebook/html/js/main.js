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
        }
    }
};

// Search Component
const SearchComponent = {
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
const EditorComponent = {
    data() {
        return {
            content: '',
            tools: ['bold', 'italic', 'image', 'video', 'link', 'list', 'header'],
            selectedTool: null
        }
    },
    methods: {
        applyFormat(tool) {
            document.execCommand(tool, false, null);
        },
        insertList() {
            document.execCommand('insertUnorderedList', false, null);
        },
        insertHeader() {
            document.execCommand('formatBlock', false, 'h1');
        },
        insertImage() {
            const url = prompt('Enter image URL');
            if (url) {
                document.execCommand('insertImage', false, url);
            }
        },
        insertVideo() {
            const url = prompt('Enter video URL');
            if (url) {
                const video = `<iframe src="${url}" frameborder="0" allowfullscreen></iframe>`;
                document.execCommand('insertHTML', false, video);
            }
        },
        insertLink() {
            const url = prompt('Enter link URL');
            if (url) {
                document.execCommand('createLink', false, url);
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
        },
        async fetchCategories() {
            const response = await fetch(`https://${GetParentResourceName()}/fetchCategories`);
            if (response.ok) {
                const data = await response.json();
                this.categories = data.categories;
            }
        },
        async fetchPages() {
            const response = await fetch(`https://${GetParentResourceName()}/fetchPages`);
            if (response.ok) {
                const data = await response.json();
                this.pages = data.pages;
            }
        },
        openPage(pageKey) {
            const page = this.pages.find(p => p.key === pageKey);
            if (page) {
                this.activePage = page;
            }
        }
    }
};

Vue.createApp(app).mount('#guidebook');

// Admin Panel Component
const AdminPanelComponent = {
    data() {
        return {
            categories: [],
            pages: [],
            newCategory: {
                name: '',
                description: '',
                order: 0,
                permissions: []
            },
            newPage: {
                category_id: null,
                title: '',
                content: '',
                key: '',
                order: 0,
                permissions: []
            }
        }
    },
    methods: {
        async fetchCategories() {
            const response = await fetch(`https://${GetParentResourceName()}/fetchCategories`);
            if (response.ok) {
                this.categories = await response.json();
            }
        },
        async fetchPages() {
            const response = await fetch(`https://${GetParentResourceName()}/fetchPages`);
            if (response.ok) {
                this.pages = await response.json();
            }
        },
        async saveCategory() {
            const response = await fetch(`https://${GetParentResourceName()}/saveCategory`, {
                method: 'POST',
                body: JSON.stringify(this.newCategory)
            });
            if (response.ok) {
                this.newCategory = { name: '', description: '', order: 0, permissions: [] };
                this.fetchCategories();
            }
        },
        async savePage() {
            const response = await fetch(`https://${GetParentResourceName()}/savePage`, {
                method: 'POST',
                body: JSON.stringify(this.newPage)
            });
            if (response.ok) {
                this.newPage = { category_id: null, title: '', content: '', key: '', order: 0, permissions: [] };
                this.fetchPages();
            }
        },
        async deleteCategory(categoryId) {
            const response = await fetch(`https://${GetParentResourceName()}/deleteCategory`, {
                method: 'POST',
                body: JSON.stringify({ id: categoryId })
            });
            if (response.ok) {
                this.fetchCategories();
            }
        },
        async deletePage(pageId) {
            const response = await fetch(`https://${GetParentResourceName()}/deletePage`, {
                method: 'POST',
                body: JSON.stringify({ id: pageId })
            });
            if (response.ok) {
                this.fetchPages();
            }
        }
    },
    mounted() {
        this.fetchCategories();
        this.fetchPages();
    }
};

// Initialize all components in a single place
document.addEventListener('DOMContentLoaded', () => {
    const vueApp = Vue.createApp({});

    // Register components globally
    vueApp.component('search-component', SearchComponent);
    vueApp.component('editor-component', EditorComponent);
    vueApp.component('admin-panel', AdminPanelComponent);
    vueApp.component('point-manager', pointManager);
    vueApp.component('permission-manager', permissionManager);

    // Mount main app
    vueApp.mount('#guidebook');
});

// Export config for modules that need it
export { GuideConfig as default };