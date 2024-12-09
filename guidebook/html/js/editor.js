
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

Vue.createApp(editor).mount('#page-editor');