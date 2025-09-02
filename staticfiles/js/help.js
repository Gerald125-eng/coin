let help_container_1 = document.querySelector('.help_container_1')
let help_container_2 = document.querySelector('.help_container_2')

help_container_1.addEventListener('click', () =>{
  help_container_1.style.display = "none"
  help_container_2.style.display = "block"
})

help_container_2.addEventListener('click', () =>{
  help_container_2.style.display = "none"
  help_container_1.style.display = "flex"
})



// help_container_3

let help_container_3 = document.querySelector('.help_container_3')
let help_container_4 = document.querySelector('.help_container_4')

help_container_3.addEventListener('click', () =>{
  help_container_3.style.display = "none"
  help_container_4.style.display = "block"
})

help_container_4.addEventListener('click', () =>{
  help_container_4.style.display = "none"
  help_container_3.style.display = "flex"
})


// help_container_5

let help_container_5 = document.querySelector('.help_container_5')
let help_container_6 = document.querySelector('.help_container_6')

help_container_5.addEventListener('click', () =>{
  help_container_5.style.display = "none"
  help_container_6.style.display = "block"
})

help_container_6.addEventListener('click', () =>{
  help_container_6.style.display = "none"
  help_container_5.style.display = "flex"
})


// help_container_7

let help_container_7 = document.querySelector('.help_container_7')
let help_container_8 = document.querySelector('.help_container_8')

help_container_7.addEventListener('click', () =>{
  help_container_7.style.display = "none"
  help_container_8.style.display = "block"
})

help_container_8.addEventListener('click', () =>{
  help_container_8.style.display = "none"
  help_container_7.style.display = "flex"
})


// help_container_9

let help_container_9 = document.querySelector('.help_container_9')
let help_container_10 = document.querySelector('.help_container_10')

help_container_9.addEventListener('click', () =>{
  help_container_9.style.display = "none"
  help_container_10.style.display = "block"
})

help_container_10.addEventListener('click', () =>{
  help_container_10.style.display = "none"
  help_container_9.style.display = "flex"
})


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