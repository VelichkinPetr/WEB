function change(id){
    let inputElem = document.getElementById('input')

    if (id === 'disabled'){
        inputElem.disabled = true;
    }
    else{
        inputElem.disabled = false; 
    }
}
const btn1 = document.getElementById('btn1');
const btn2 = document.getElementById('btn2');

btn1.addEventListener('click', function(){change('unabled')});
btn2.addEventListener('click', function(){change('disabled')});