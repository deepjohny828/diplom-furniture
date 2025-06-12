document.addEventListener('DOMContentLoaded', function() {
    const mobileFiltersBtn = document.getElementById('mobileFiltersBtn');
    const mobileFiltersOverlay = document.getElementById('mobileFiltersOverlay');
    const closeFilters = document.getElementById('closeFilters');
    const body = document.body;

    // Открытие фильтров
    function openFilters() {
        mobileFiltersOverlay.style.display = 'block';
        body.style.overflow = 'hidden';
        setTimeout(() => {
            mobileFiltersOverlay.classList.add('show');
        }, 10);
    }

    // Закрытие фильтров
    function closeFiltersModal() {
        mobileFiltersOverlay.classList.remove('show');
        setTimeout(() => {
            mobileFiltersOverlay.style.display = 'none';
            body.style.overflow = '';
        }, 300);
    }

    // Обработчики событий
    mobileFiltersBtn.addEventListener('click', openFilters);
    closeFilters.addEventListener('click', closeFiltersModal);

    // Закрытие при клике вне области
    mobileFiltersOverlay.addEventListener('click', function(e) {
        if (e.target === mobileFiltersOverlay) {
            closeFiltersModal();
        }
    });

    // Закрытие по ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileFiltersOverlay.style.display === 'block') {
            closeFiltersModal();
        }
    });
});