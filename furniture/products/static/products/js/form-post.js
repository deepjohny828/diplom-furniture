document.querySelectorAll('#contactForm').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Очищаем предыдущие ошибки
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Успех!',
                    text: 'Заявка успешно отправлена!',
                    timer: 3000,
                    showConfirmButton: false
                });
                form.reset();
                modal.style.display = "none";
                document.body.style.overflow = '';
            } else {
                // Обработка ошибок для каждого поля
                if (data.errors) {
                    for (const [field, errors] of Object.entries(data.errors)) {
                        const input = form.querySelector(`[name="${field}"]`);
                        if (input) {
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'error-message';
                            errorDiv.style.color = 'red';
                            errorDiv.textContent = errors.join(', ');
                            input.parentNode.appendChild(errorDiv);
                        }
                    }
                }
            }
        })
        .catch(error => {
            Swal.fire({
                icon: 'error',
                title: 'Ошибка сервера',
                text: 'Попробуйте позже',
            });
        });
    });
});