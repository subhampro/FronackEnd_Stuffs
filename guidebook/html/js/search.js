
const search = {
    data() {
        return {
            query: '',
            results: []
        }
    },
    methods: {
        async searchContent() {
            const response = await fetch(`https://${GetParentResourceName()}/searchContent`, {
                method: 'POST',
                body: JSON.stringify({ query: this.query })
            });
            if (response.ok) {
                this.results = await response.json();
            }
        }
    },
    watch: {
        query: {
            handler: 'searchContent',
            debounce: 300
        }
    }
};

Vue.createApp(search).mount('#search-component');