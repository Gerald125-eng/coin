 // JavaScript
    // const referrals = [
    //   { name: "John Doe", status: "Active" },
    //   { name: "Jane Smith", status: "Pending" },
    //   { name: "Alex Johnson", status: "Active" },
    // ];

    // const referralsList = document.getElementById("referralsList");

    // function renderReferrals() {
    //   referralsList.innerHTML = "";
    //   referrals.forEach((referral, index) => {
    //     const referralItem = document.createElement("div");
    //     referralItem.classList.add("referral-item");
    //     referralItem.innerHTML = `
    //       <span>${referral.name}</span>
    //       <span>${referral.status}</span>
    //     `;
    //     referralsList.appendChild(referralItem);
    //   });
    // }

    function copyLink() {
      const referralLink = document.getElementById("referralLink");
      referralLink.select();
      document.execCommand("copy");
      alert("Referral link copied to clipboard!");
    }

    // Initialize referrals on page load
    renderReferrals();



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
