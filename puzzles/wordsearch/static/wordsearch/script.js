 

 // eventlistner for checkboxes

document.addEventListener('DOMContentLoaded',()=>{

    for(let i=0;i<= 143;i++){
        const checkbox = document.getElementById(`id${i}`)
        const char = document.querySelector(`.char${i}`)

        if(checkbox && char){
            checkbox.addEventListener("change",()=>{
                char.style .backgroundColor = checkbox.checked ? 'rgb(54, 33, 33)' : ''
            })
        }
    }
})