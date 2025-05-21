const slider = document.querySelector('.slides');
const slides = document.querySelectorAll('.slide');
const dotsContainer = document.getElementById('dotsContainer');
let currentIndex = 0;

slides.forEach((_, index) => {
    const dot = document.createElement('span');
    dot.classList.add('dot');
    if(index === 0) dot.classList.add('active');
    dot.addEventListener('click', () => { currentIndex = index; updateSlider(); });
    dotsContainer.appendChild(dot);
});

function updateSlider() {
    slider.style.transform = `translateX(-${currentIndex * 100}%)`;
    document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));
    document.querySelectorAll('.dot')[currentIndex].classList.add('active');
}

document.getElementById('prev').onclick = () => { currentIndex = (currentIndex - 1 + slides.length) % slides.length; updateSlider(); }
document.getElementById('next').onclick = () => { currentIndex = (currentIndex + 1) % slides.length; updateSlider(); }

setInterval(() => {
    currentIndex = (currentIndex + 1) % slides.length;
    updateSlider();
}, 5000);
