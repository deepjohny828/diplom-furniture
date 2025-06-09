
const modal = document.getElementById("myModal");
const btn = document.querySelectorAll("#openModalBtn")
const span = document.getElementsByClassName("close")[0];
const form = document.getElementById("contactForm");


btn.forEach(e => {
    e.onclick = () =>{
        const productIds = [];
        if (window.location.pathname === "/group_products/"){
                document.querySelectorAll('.item-card').forEach(item => {
                const productId = item.dataset.id;
                productIds.push(productId);
            });
        }
        else{
            const productId = e.dataset.product_id;
            productIds.push(productId);
        }
        const container = document.getElementById('hiddenProducts')
        container.innerHTML = '';

        productIds.forEach(id =>{
            const input = document.createElement('input')
            input.type = 'hidden';
            input.name = 'products';
            input.value = id;
            container.appendChild(input)
        });

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