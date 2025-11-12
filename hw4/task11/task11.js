const btn = document.getElementById('btn');

function removeElem(){
    let list = document.getElementById('list');
    let lastElem = list.lastElementChild;

    if (list.children.length === 0){
        alert('Список пуст');
    }
    else{
        list.removeChild(lastElem);
    }
    
}

btn.addEventListener('click', function(){removeElem()})