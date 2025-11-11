const btn = document.getElementById('btn');

function change_image(){
    let img = document.getElementById('img');
    if (img.src.endsWith("image/b_and_w_mug.svg")){
        img.src = 'image/black_cup.svg'
    }
    else{img.src = "image/b_and_w_mug.svg"}
    
}

btn.addEventListener('click', function(){change_image()})