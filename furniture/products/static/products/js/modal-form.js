
const modal = document.getElementById("myModal");
const btn = document.querySelectorAll("#openModalBtn")
const span = document.getElementsByClassName("close")[0];
const form = document.getElementById("contactForm");


    // Открываем модальное окно при клике на кнопку
btn.forEach(e => {
    e.onclick = () =>{
        const product_id = e.dataset.product_id
        document.getElementById("id_product").value = product_id
        modal.style.display = "block";
    }
});
    
    // Закрываем модальное окно при клике на крестик
span.onclick = function() {
    modal.style.display = "none";
}
    
    // Закрываем модальное окно при клике вне его
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
    
    // Обработка отправки формы
form.onsubmit = function(e) {
        
        // Здесь можно добавить код для отправки данных формы
        // alert("Форма отправлена! Спасибо за ваше сообщение.");
        // Очищаем форму и закрываем модальное окно
    modal.style.display = "none";
}