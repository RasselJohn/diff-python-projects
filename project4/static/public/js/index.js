new Vue({
    el: '#currency',

    data: {
        currency: 'неизвестно.',
        ws: null
    },

    mounted() {
        this.ws = new WebSocket("ws://localhost:8000/ws/");

        this.ws.onmessage = ({data}) => {
            console.log('Message came!');
            let jsonData = JSON.parse(data);
            if (jsonData && jsonData.currencyRate) {
                this.currency = (+jsonData.currencyRate).toFixed(2);
            }
        };

    },
    destroyed() {
        this.ws.close();
    }
});