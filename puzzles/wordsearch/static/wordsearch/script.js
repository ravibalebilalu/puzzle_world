 

 // eventlistner for checkboxes

document.addEventListener('DOMContentLoaded',()=>{

    for(let i=0;i<= 143;i++){
        const checkbox = document.getElementById(`id${i}`)
        const char = document.querySelector(`.char${i}`)

        if(checkbox && char){
            checkbox.addEventListener("change",()=>{
                char.style .backgroundColor = checkbox.checked ? 'rgb(104, 157, 242)' : ''
                //char.style .color = checkbox.checked ? 'rgb(255, 255, 255)' : ' rgb(8, 5, 5)'
            })
        }
    }
})