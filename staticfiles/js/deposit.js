
        function invest() { 
          const amount = document.getElementById('amount').value;
          const currency = document.querySelector('input[name="currency"]:checked');
          
          if (!amount || !currency) {
            alert('Please fill out all fields.');
            return;
          }
          
          alert(`You have invested ${amount} in ${currency.value}.`);
        }
    
        function redirectToDashboard() {
          // Change this link to the actual dashboard link when ready
          window.location.href = 'dashboard.html';
        }




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
