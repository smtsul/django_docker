$(document).ready(function () { //todo полностью разобраться с ajax и jquerry
    // Функция для получения значения куки по имени
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Получаем CSRF-токен
    var csrftoken = getCookie('csrftoken');

    // Перед отправкой запроса добавляем CSRF-токен в заголовок
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Функция для отправки AJAX-запроса
    function sendAjaxRequest(url, method, data, successCallback, errorCallback) {
        $.ajax({
            url: url,
            type: method,
            data: data,
            processData: false,
            contentType: false,
            success: successCallback,
            error: errorCallback
        });
    }

    // Функция для обновления списка файлов
    function updateFileList() {
        sendAjaxRequest(
            "/signal_media/ajax_get_file_list/",
            "GET",
            null,
            function (data) {
                console.log("Success. Received data:", data);

                var fileList = data.files;
                var fileListContainer = $("#fileList");
                fileListContainer.empty();
                fileList.forEach(function (file) {
                    fileListContainer.append("<li><a href='#' class='download-link' data-filename='" + file + "'>" + file + "</a></li>");
                });

                // Добавляем обработчик события для скачивания файлов
                $(".download-link").on("click", function (event) {
                    event.preventDefault();
                    var filename = $(this).data("filename");
                    downloadFile(filename);
                });
            },
            function (error) {
                console.error("Error fetching file list:", error);
            }
        );
    }

    // Функция для скачивания файла
    function downloadFile(filename) {
        console.log("Downloading file:", filename);
        window.location.href = "/signal_media/download_file/" + encodeURIComponent(filename);
    }

    // Обработчик события клика по кнопке "Запустить функцию rename"
    // Обработчик события клика по кнопке "Запустить функцию rename"
var renameBtn = $("#renameBtn"); //TODO переделать
renameBtn.on("click", function (event) {
    event.preventDefault();
    var year = $("#year").val();
    var formData = new FormData($("#uploadForm")[0]);
    formData.append("year", year);
    sendAjaxRequest(
        "/signal_media/your_ajax_url/",  // Замените на фактический URL
        "POST",
        formData,
        function (data) {
            console.log("Success. Received data:", data);
            // Обработка успешного ответа от сервера

            // После успешной загрузки файла вызываем функцию для обновления списка
            updateFileList();
        },
        function (error) {
            console.error("Error sending AJAX request:", error);
        }
    );
});
var loggedBtn = $("#logged");
loggedBtn.on("click", function (event) {
    event.preventDefault();  // Это предотвратит стандартное поведение кнопки submit
    sendAjaxRequest(
        "/signal_media/logged/",
        "POST",
        null,
        function (data) {
            console.log("Success. Received data:", data);
            // Обработка успешного ответа от сервера
            // Например, обновление списка файлов
            updateFileList();
        },
        function (error) {
            console.error("Error sending AJAX request:", error);
        }
    );
});

// Обработчик события клика по кнопке "Проверить плейлисты"
var checkPlaylistsBtn = $("#action");
var errorBlock = $("#errorBlock"); // Получаем блок ошибок

var checkPlaylistsBtn = $("#action");
var errorBlock = $("#errorBlock"); // Получаем блок ошибок

var checkPlaylistsBtn = $("#action");
var errorBlock = $("#errorBlock"); // Получаем блок ошибок

checkPlaylistsBtn.on("click", function (event) {
    event.preventDefault();

    sendAjaxRequest(
        "/signal_media/test_ajax_log/",
        "GET",
        null,
        function (data) {
            if (data.results) {
                var errorMessage = "";

                for (var i = 0; i < data.results.length; i++) {
                    errorMessage += data.results[i].result_min.message + "<br>" + data.results[i].result_sec.message + "<br>";
                }

                // Обновляем содержимое блока ошибок
                errorBlock.html(errorMessage);
            } else {
                // Выводим сообщение об ошибке данных в блок ошибок
                errorBlock.html("Ошибка: нет данных для проверки");
            }
        },
        function (error) {
            // Выводим сообщение об ошибке AJAX-запроса в блок ошибок
            errorBlock.html("Error sending AJAX request: " + JSON.stringify(error));
        }
    );
});





    // Вызываем функцию для обновления списка файлов при загрузке страницы
    updateFileList();
});
