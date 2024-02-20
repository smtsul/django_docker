// JavaScript для всплывающего окна
document.addEventListener('DOMContentLoaded', function () {
    const popup = document.getElementById('popup');
    const closePopup = document.getElementById('close-popup');
    const popupMessage = document.getElementById('popup-message');
    function showPopup(message) {
        popupMessage.textContent = message;
        popup.style.display = 'block';
    }
    function hidePopup() {
        popup.style.display = 'none';
    }
    closePopup.addEventListener('click', hidePopup);
    const successMessage = 'Плейлисты загружены';
    showPopup(successMessage);
});
