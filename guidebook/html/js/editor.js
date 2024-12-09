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
}

Vue.createApp(editor).mount('#page-editor');