function renderReferrals() {
    // example logic
    let referralsContainer = document.querySelector('#referrals');
    if(referralsContainer){
        referralsContainer.innerHTML = "<p>No referrals yet.</p>";
    }
}

// Existing code
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

// Call the function after defining it
renderReferrals();


function renderReferrals() {
    const referralsContainer = document.getElementById("referralsContainer");
    if (referralsContainer) {
        // Example: populate with dummy referrals
        referralsContainer.innerHTML = "<p>No referrals yet.</p>";
    }
}



function copyLink() {
    const referralLink = document.getElementById("referralLink");
    referralLink.select();
    document.execCommand("copy");
    alert("Referral link copied to clipboard!");
}

// Initialize referrals on page load
renderReferrals();

