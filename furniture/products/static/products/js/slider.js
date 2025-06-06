document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const dotsContainer = document.getElementById('dotsContainer');
    const slidesWrapper = document.getElementById('slidesWrapper');
    let currentSlide = 0;
    
    // Инициализация слайдера
    function initSlider() {
        createDots();
        updateSlider();
    }
    
    // Создание точек
    function createDots() {
        slides.forEach((_, i) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        });
        updateDots();
    }
    
    // Переход к конкретному слайду
    function goToSlide(n) {
        currentSlide = n;
        updateSlider();
    }
    
    // Обновление слайдера
    

    function updateSlider() {
        const offset = -100 * currentSlide;
        slidesWrapper.style.transform = `translateX(${offset}%)`;
        updateDots();
    }
    
    // Обновление точек
    function updateDots() {
        const dots = document.querySelectorAll('.dot');
        dots.forEach(dot => dot.classList.remove('active'));
        dots[currentSlide]?.classList.add('active');
    }
    
    // Следующий слайд
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        updateSlider();
    }
    
    // Предыдущий слайд
    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        updateSlider();
    }
    
    // Обработчики событий
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // Автопрокрутка (опционально)
    // setInterval(nextSlide, 5000);
    
    // Инициализация
    initSlider();
});