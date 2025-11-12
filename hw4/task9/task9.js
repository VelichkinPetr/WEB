const btn = document.getElementById('btn');

function appendElem(){
    let ulElem = document.getElementById('ul');
    let liNew = document.createElement('li');
    liNew.textContent = 'Текст';
    ulElem.appendChild(liNew)  
}

btn.addEventListener('click', function(){appendElem()})