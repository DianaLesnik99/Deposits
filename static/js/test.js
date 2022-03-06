alert('Подключён, начинаю работу!')
$(document).ready(function () {
    console.log('ready!');
});

function onReady() {
    $("#forward").on("click", function () {
        $("h1").text("Йеее! Мы поменяли текст заголовка!")
    })

    $("#backward").on("click", function () {
        $("h1").text("Это Главная страница сайта")
    })
}

$(document).ready(onReady);

