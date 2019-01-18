function hint(id) {
    return fetch(script_root + '/api/v1/hints/' + id, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        return response.json();
    });
}


function unlock(params){
    return fetch(script_root + '/api/v1/unlocks', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        return response.json();
    });
}

function loadhint(hintid) {
    var md = window.markdownit({
        html: true,
    });

    hint(hintid).then(function (response) {
        if (response.data.content) {
            ezal({
                title: "Хинт",
                body: md.render(response.data.content),
                button: "Понятно!"
            });
        } else {
            ezq({
                title: "Разблокировать хинт?",
                body: "Вы уверены, что хотите открыть этот хинт?",
                success: function () {
                    var params = {
                        target: hintid,
                        type: "hints"
                    };
                    unlock(params).then(function (response) {
                        if (response.success) {
                            hint(hintid).then(function(response) {
                                ezal({
                                    title: "Хинт",
                                    body: md.render(response.data.content),
                                    button: "Понятно!"
                                });
                            });
                        } else {
                            ezal({
                                title: "Ошибка",
                                body: md.render(response.errors.score),
                                button: "Понятно!"
                            });
                        }
                    });
                }
            });
        }
    });
}