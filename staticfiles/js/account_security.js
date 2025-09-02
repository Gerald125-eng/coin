let OIP_removebg = document.querySelector('.OIP-removebg')
let buger_2 = document.querySelector('.buger_2')
let icons8_close = document.querySelector('.icons8-close')

OIP_removebg.addEventListener('click', () =>{
    buger_2.style.display = "flex"
    icons8_close.style.display = "block"
    OIP_removebg.style.display = "none"
})


icons8_close.addEventListener('click', () =>{
    buger_2.style.display = "none"
    OIP_removebg.style.display = "block"
    icons8_close.style.display = "none"
})
