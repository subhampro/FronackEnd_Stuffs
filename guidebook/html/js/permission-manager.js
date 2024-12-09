
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
}

Vue.createApp(permissionManager).mount('#permission-manager');