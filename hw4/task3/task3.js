const myList = document.getElementsByClassName('my-list')[0]
const redBtn = document.getElementsByClassName('red-btn')[0]
const greenBtn = document.getElementsByClassName('green-btn')[0]
function changeTextColor(colorClass){
    myList.classList.remove('red-text', 'green-text')
    myList.classList.add(colorClass)
    }
redBtn.addEventListener('click', function(){changeTextColor('red-text')})
greenBtn.addEventListener('click', function(){changeTextColor('green-text')})