
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
}

Vue.createApp(pointManager).mount('#point-manager');