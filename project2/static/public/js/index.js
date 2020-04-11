let ws = new WebSocket("ws://localhost:8000/ws/");
let dataElem = document.getElementById('data');

ws.onopen = () => {
    console.log('Сокет открыт!');
    dataElem.innerText = 'Пожалуйста, ждите (данные загружаются)!'
};

ws.onmessage = ({data}) => {
    console.log('Пришли данные!');
    dataElem.innerText = data;
};
