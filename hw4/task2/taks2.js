
function ClickButton(){
    let inputElement = document.getElementsByTagName('input')[0];
    let buttonElement = document.getElementsByTagName('button')[0];
    let inputText = inputElement.value;
    
    if (inputText.length === 0){
        alert('Упс, вы не ввели тест(')
    }
    else{
        buttonElement.innerHTML = inputText;
    }
    
    inputElement.value = ''
    }
