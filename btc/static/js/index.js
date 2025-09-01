

const slides = document.querySelectorAll('.charting_area');
let index = 0;

function showSlide(){
    slides.forEach((charting_area, i) =>{
        charting_area.classList.remove('active');
        if(i === index){
         charting_area.classList.add('active');

        }
    })
    index = (index + 1) % slides.length

}

showSlide()

setInterval(showSlide, 3500)









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






const slidess = document.querySelectorAll('.hero-slide');
    let currentIndex = 0;

    setInterval(() => {
      slidess[currentIndex].classList.remove('active');
      currentIndex = (currentIndex + 1) % slidess.length;
      slidess[currentIndex].classList.add('active');
    }, 3000);














const investors = [
    { name: "John", country: "USA", amount: "$1,200" },
    { name: "Fatima", country: "UAE", amount: "$2,500" },
    { name: "Kofi", country: "Ghana", amount: "$750" },
    { name: "Chen", country: "China", amount: "$3,000" },
    { name: "Anna", country: "Germany", amount: "$980" },
    { name: "Ngozi", country: "Nigeria", amount: "$1,500" },
    { name: "Carlos", country: "Brazil", amount: "$2,100" }
  ];

let r = 0;
const box = document.getElementById('investmentBox');

function showInvestorNotification() {
    const investor = investors[r];
    box.textContent = `${investor.name} from ${investor.country} just invested ${investor.amount}!`;
    box.classList.add('show');

    // Hide after 2.5s to leave time for transition
    setTimeout(() => {
      box.classList.remove('show');
    }, 2500);

    r = (r + 1) % investors.length;
  }

  setInterval(showInvestorNotification, 4000); // every 3s
