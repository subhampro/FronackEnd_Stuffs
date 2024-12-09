
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
}

Vue.createApp(adminPanel).mount('#admin-panel');