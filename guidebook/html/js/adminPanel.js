
const adminPanel = {
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

Vue.createApp(adminPanel).mount('#admin-panel');