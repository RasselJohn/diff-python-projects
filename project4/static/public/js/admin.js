new Vue({
    el: '#admin',

    data: {
        adminCurrencies: [],
        newRate: '',
        ws: null
    },

    mounted() {
        flatpickr("#flatPick", {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        });

        this.ws = new WebSocket("ws://localhost:8000/ws/");

        this.ws.onmessage = ({data}) => {
            console.log('Message came!');
            let jsonData = JSON.parse(data);
            if (jsonData && jsonData.adminCurrencies) {
                this.adminCurrencies = jsonData.adminCurrencies.split('\n');
            }
        }
    },
    methods: {
        onChangeRate() {
            this.ws.send(JSON.stringify({
                newRate: this.newRate,
                expire: new Date(document.getElementById('flatPick').value)
            }));
        }
    },
    destroyed() {
        this.ws.close();
    }
});