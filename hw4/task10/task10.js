const btn = document.getElementById('btn');

function appendElem(){
    let inputElem = document.querySelector('input');
    let inputNew = document.createElement('input');
    inputNew.type = ''
    inputElem.after(inputNew)  
}

btn.addEventListener('click', function(){appendElem()})