
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
}

Vue.createApp(app).mount('#guidebook');