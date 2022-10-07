document.addEventListener("DOMContentLoaded", (event) => {
    var decline = document.getElementsByName('reject_application')[0]
    decline.disabled = true;

})


const reason = document.getElementById('id_reason_for_decline');
// enable decline button if reason length > 0
reason.addEventListener('input', (event) => {
    var decline = document.getElementsByName('reject_application')[0]
    if (reason.value == '') {
        decline.disabled = true;
    } else {
        decline.disabled = false;
    }
})