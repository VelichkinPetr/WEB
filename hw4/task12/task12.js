const listItems = document.querySelectorAll('#list li');

listItems.forEach(item => {
            item.addEventListener('click', function() {
                this.remove();
            });
});