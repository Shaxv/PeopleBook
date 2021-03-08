$(document).ready(function(){
    const form1 = document.getElementById("form1")
    const form2 = document.getElementById("form2")
    const form3 = document.getElementById("form3")

    const form1Button = document.getElementById("form1Button")
    const form2Button = document.getElementById("form2Button")
    const form3Button = document.getElementById("form3Button")

    form1Button.onclick = function(){
        form1.style.display = "none"
        form2.style.display = "block"
    }
})