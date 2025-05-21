const btn = document.getElementById("btn-query");
const modal = document.getElementById("myModal");
const span = document.getElementsByClassName("close")[0];
const form = document.getElementById("contactForm");

btn.onclick = () => {
    modal.style.display = "block";
}
span.onclick = function() {
        modal.style.display = "none";
    }
    
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
    

form.onsubmit = function(e) {
        
        // Здесь можно добавить код для отправки данных формы
        // alert("Форма отправлена! Спасибо за ваше сообщение.");
        // Очищаем форму и закрываем модальное окно
    console.log("отправка")
    modal.style.display = "none";
}