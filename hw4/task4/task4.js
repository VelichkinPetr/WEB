function square(){
    let inputElem = document.getElementById('input')
    let inputText = inputElem.value;

    if (inputText && (!isNaN(inputText)) ){
        alert(inputText**2)
    }
    else{
        alert('введено не число(')
    }
    inputElem.value=''
}
const btn = document.getElementById('btn')

btn.addEventListener('click', function(){square()})