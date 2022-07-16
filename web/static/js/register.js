console.log('working');
const submitBtn = document.getElementById('submit-btn')
const pass = document.getElementById('pass')
const cPass = document.getElementById('cPass')
const message = document.getElementById('message')

function validator() {
    if (pass.value === cPass.value) {
        submitBtn.disabled = false
    }
    else {
        message.innerHTML = 'Password did not match'
    }
    console.log('validator working');
    console.log(pass.value, cPass.value);
}
