const catalogBtn = document.getElementById('catalogBtn');
const megaMenu = document.getElementById('megaMenu');
const categories = document.querySelectorAll('.category');
const submenus = document.querySelectorAll('.submenu');

// Показать/скрыть меню
catalogBtn.addEventListener('click', () => {
  megaMenu.classList.toggle('hidden');
});

// Переключение подменю
categories.forEach(cat => {
  cat.addEventListener('click', () => {
    // Удалить active и selected
    categories.forEach(c => c.classList.remove('selected'));
    submenus.forEach(s => s.classList.remove('active'));

    // Активировать выбранное
    cat.classList.add('selected');
    const target = cat.dataset.target;
    document.getElementById(target).classList.add('active');
  });
});

// Закрытие при клике вне
document.addEventListener('click', (e) => {
  if (!megaMenu.contains(e.target) && !catalogBtn.contains(e.target)) {
    megaMenu.classList.add('hidden');
  }
});