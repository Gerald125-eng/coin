let OIP_removebg = document.querySelector('.OIP-removebg')
let buger_2 = document.querySelector('.buger_2')
let buger = document.querySelector('.buger')
let icons8_close = document.querySelector('.icons8-close')

OIP_removebg.addEventListener('click', () =>{
    buger_2.style.display = "flex"
    buger.style.display = "none"
    icons8_close.style.display = "block"
    OIP_removebg.style.display = "none"
})


icons8_close.addEventListener('click', () =>{
    buger_2.style.display = "none"
    OIP_removebg.style.display = "block"
    icons8_close.style.display = "none"
    buger.style.display = "block"
})


let removebg = document.querySelector('.removebg')
// let buger_2 = document.querySelector('.buger_2')
let close_ = document.querySelector('.close')

removebg.addEventListener('click', () =>{
    buger_2.style.display = "flex"
    close_.style.display = "block"
    removebg.style.display = "none"
})


close_.addEventListener('click', () =>{
    buger_2.style.display = "none"
    removebg.style.display = "block"
    close_.style.display = "none"
})
