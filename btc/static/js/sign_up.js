let OIP_removebg = document.querySelector('.OIP-removebg')
let nav_second = document.querySelector('.nav_second')
let icons8_close = document.querySelector('.icons8-close')

OIP_removebg.addEventListener('click', () =>{
    nav_second.style.display = "flex"
    icons8_close.style.display = "block"
    OIP_removebg.style.display = "none"
})


icons8_close.addEventListener('click', () =>{
    nav_second.style.display = "none"
    OIP_removebg.style.display = "block"
    icons8_close.style.display = "none"
})