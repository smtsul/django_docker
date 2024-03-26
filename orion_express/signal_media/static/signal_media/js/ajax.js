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
    //checker for errors
    function checker(filename) {
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
                // Предположим, что у вас есть элемент с id "errorBlock"
                var errorBlock = $("#errorBlock");
                errorBlock.html(errorMessage);
            } else {
                // Выводим сообщение об ошибке данных в блок ошибок
                // Предположим, что у вас есть элемент с id "errorBlock"
                var errorBlock = $("#errorBlock");
                errorBlock.html("Ошибка: нет данных для проверки");
            }
        },
        function (error) {
            // Выводим сообщение об ошибке AJAX-запроса в блок ошибок
            // Предположим, что у вас есть элемент с id "errorBlock"
            var errorBlock = $("#errorBlock");
            errorBlock.html("Error sending AJAX request: " + JSON.stringify(error));
        }
    );
}

    $(document).on('click', '#testupld', function (event) {
            console.log('кнопка нажата');
            var inputElement = document.getElementById('myfile');
            var files = inputElement.files;
            var yearValue = document.getElementById('year').value; // Получаем значение года
            var formData = new FormData();
            // Добавляем файлы в объект FormData
            for (var i = 0; i < files.length; i++) {
                formData.append('myfile', files[i]);
            }
            // Добавляем значение года в объект FormData
            formData.append('year', yearValue);
            // Отправляем данные на сервер с помощью fetch
            fetch('/signal_media/upload_files_better/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                updateFileList();
                checker()

            })
            .catch(error => {
                console.error('Error:', error);
                // Обработка ошибки, если необходимо
            });
        });
    $(document).on('click', '.signal_mediaBtn', function (event) {
    event.preventDefault();
    updateFileList();
    checker();
    $("form").append(`
        <p class="other-element"> <!-- Добавляем класс other-element -->
            <input type="file" id="myfile" name="myfile" multiple accept=".xlsx">
        </p>
        <label for="year" class="other-element">Год:</label> <!-- Добавляем класс other-element -->
        <input value="2024" type="text" id="year" name="year" required>
        <button type="button" id="testupld"> Загрузить test </button>
        <button type="submit" id="logged" value="log">Очистить список</button>
    `);
    $("body").addClass("flex-container");
    $(".flex-container").append(`
        <div class="file-list other-element"> <!-- Добавляем класс other-element -->
            <h2>Список плейлистов:</h2>
            <ul id="fileList">
            </ul>
        </div>
        <div class="error-block other-element" id="errorBlock">Cписок ошибок</div> <!-- Добавляем класс other-element -->
    `);
});
    $(document).on('click','#logged',function(event){
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
    })
console.log('Скрипт запущен');
updateFileList();
});
