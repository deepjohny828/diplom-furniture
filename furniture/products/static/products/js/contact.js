// Инициализация карты
ymaps.ready(init);

function init() {
    var map = new ymaps.Map('map', {
        center: [59.222, 39.884], // Координаты Вологды
        zoom: 12
    });

    var placemark = new ymaps.Placemark([59.222, 39.884], {
        hintContent: 'Надом Мебель',
        balloonContent: 'Адрес: г. Вологда, ул. Ильюшина, 95'
    });

    map.geoObjects.add(placemark);
}