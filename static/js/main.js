// Auto-dismiss alert messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });
});

// Live search filter on book list page
const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        const bookCards = document.querySelectorAll('.book-card-wrapper');
        bookCards.forEach(function (card) {
            const title = card.dataset.title.toLowerCase();
            const author = card.dataset.author.toLowerCase();
            if (title.includes(query) || author.includes(query)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Confirm before deleting a book
const deleteForms = document.querySelectorAll('.delete-form');
deleteForms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
        if (!confirm('Are you sure you want to delete this book?')) {
            e.preventDefault();
        }
    });
});

// Show character count on description textarea
const descField = document.getElementById('id_description');
if (descField) {
    const counter = document.createElement('small');
    counter.classList.add('text-muted');
    descField.parentNode.appendChild(counter);
    function updateCount() {
        counter.textContent = descField.value.length + ' characters';
    }
    descField.addEventListener('input', updateCount);
    updateCount();
}