;(function () {
    let form = document.getElementById('form');

    if (!form) {
        return false;
    }

    form.onsubmit = () => {
        let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        let options = {
            method: 'POST',
            headers: {'X-CSRFToken': csrf},
            body: new FormData(form)
        };
        makeAjaxRequest(form.action, options);
        return false;
    };


    // materialize modal
    document.addEventListener('DOMContentLoaded', () => {
        let elems = document.querySelectorAll('.modal');
        let instances = M.Modal.init(elems, {});
    });

    function openModal(message) {
        let elem = document.getElementById('modalMessage');
        elem.innerText = message;
        document.getElementById('modalOpenButton').click();
    }

    function makeAjaxRequest(url, options) {
        fetch(url, options)
            .then((response) => response.json())
            .then((json) => {
                if (json.url) {
                    location = json.url;
                    return;
                }

                if (json.error) {
                    throw new Error(json.error);
                } else {
                    throw new Error('Неизвестная ошибка !');
                }
            })
            .catch(openModal);
    }
})();