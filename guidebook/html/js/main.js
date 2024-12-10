const GuideConfig = {
    // Only keep non-theme related settings
    IFrameInsertIntoPage: false,
    // ...other UI settings...
};

window.addEventListener('message', (event) => {
    try {
        const item = event.data;
        if (item.type === 'forceClose') {
            app.$data.visible = false;
            app.$data.isEditing = false;
            app.$data.isAdminPanelOpen = false;
            console.log('[Guidebook]: UI forcefully closed by command');
        }
    } catch (error) {
        console.error('[Guidebook Error]:', error);
    }
});

// Component definitions
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
const app = window.Vue.createApp({
    data() {
        return {
            visible: false,
            isEditing: false,
            isAdmin: false,
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
});

app.mount('#guidebook');

// Admin Panel Component
const AdminPanelComponent = {
    data() {
        return {
            categories: [],
            pages: []
        }
    },
    mounted() {
        try {
            console.log('[Guidebook]: Admin panel component mounted');
            this.fetchCategories();
            this.fetchPages();
        } catch (error) {
            console.error('[Guidebook Error]: Failed to mount admin panel -', error);
            fetch(`https://${GetParentResourceName()}/closeAdminPanel`, {
                method: 'POST'
            });
        }
    },
    methods: {
        async fetchCategories() {
            try {
                const response = await fetch(`https://${GetParentResourceName()}/fetchCategories`);
                if (response.ok) {
                    const data = await response.json();
                    this.categories = data.categories;
                }
            } catch (error) {
                console.error('[Guidebook Error]: Failed to fetch categories -', error);
            }
        },
        async fetchPages() {
            try {
                const response = await fetch(`https://${GetParentResourceName()}/fetchPages`);
                if (response.ok) {
                    const data = await response.json();
                    this.pages = data.pages;
                }
            } catch (error) {
                console.error('[Guidebook Error]: Failed to fetch pages -', error);
            }
        },
        async saveCategory() {
            const category = {
                name: this.newCategoryName,
                description: this.newCategoryDescription,
                order: this.newCategoryOrder,
                permissions: this.newCategoryPermissions
            };
            await fetch(`https://${GetParentResourceName()}/createCategory`, {
                method: 'POST',
                body: JSON.stringify(category)
            });
            this.fetchCategories();
        },
        async savePage() {
            const page = {
                category_id: this.newPageCategoryId,
                title: this.newPageTitle,
                content: this.newPageContent,
                key: this.newPageKey,
                order: this.newPageOrder,
                permissions: this.newPagePermissions
            };
            await fetch(`https://${GetParentResourceName()}/createPage`, {
                method: 'POST',
                body: JSON.stringify(page)
            });
            this.fetchPages();
        },
        async deleteCategory(categoryId) {
            await fetch(`https://${GetParentResourceName()}/deleteCategory`, {
                method: 'POST',
                body: JSON.stringify({ id: categoryId })
            });
            this.fetchCategories();
        },
        async deletePage(pageId) {
            await fetch(`https://${GetParentResourceName()}/deletePage`, {
                method: 'POST',
                body: JSON.stringify({ id: pageId })
            });
            this.fetchPages();
        }
    }
};

// Single Vue app initialization
document.addEventListener('DOMContentLoaded', () => {
    if (window.vueApp) {
        window.vueApp.unmount();
    }
    
    const vueApp = window.Vue.createApp({
        template: '<div></div>' // Empty template for base app
    });
    
    // Register all components
    const components = {
        'search-component': SearchComponent,
        'editor-component': EditorComponent,
        'admin-panel': AdminPanelComponent,
        'point-manager': pointManager,
        'permission-manager': permissionManager
    };

    Object.entries(components).forEach(([name, component]) => {
        vueApp.component(name, component);
    });

    window.vueApp = vueApp;
    window.vueApp.mount('#guidebook');
});

window.GuideConfig = GuideConfig;