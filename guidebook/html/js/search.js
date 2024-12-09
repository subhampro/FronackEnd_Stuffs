
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
}

Vue.createApp(search).mount('#search-component');