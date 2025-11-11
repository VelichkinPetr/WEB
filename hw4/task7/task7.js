const rect = document.getElementById('rect-yellow');
const text = document.getElementById('text');

rect.addEventListener('mouseenter', function(){
    text.style.opacity = '1';
    rect.style.justifyItems = 'center';
    rect.style.alignContent = 'center';
})

rect.addEventListener('mouseleave', function(){
    text.style.opacity = '0';
})