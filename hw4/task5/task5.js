function change(){
    let input1Elem = document.getElementById('input1')
    let input1Text = input1Elem.value;
    let input2Elem = document.getElementById('input2')
    let input2Text = input2Elem.value;

    if ((input1Text.length === 0) && (input2Text.length === 0)){
        alert('Поля пусты(')
    }
    else{
        input1Elem.value = input2Text
        input2Elem.value = input1Text
    }
    
}
const btn = document.getElementById('btn')

btn.addEventListener('click', function(){change()})