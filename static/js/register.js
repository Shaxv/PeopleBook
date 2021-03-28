
//
// Form 1
//

function Form1Submit(){
    const email_error = document.getElementById("email_error")

    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const email = document.getElementById('id_email')
    const first_name = document.getElementById('id_first_name')
    const last_name = document.getElementById('id_last_name')

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('email', email.value)
    fd.append('first_name', first_name.value)
    fd.append('last_name', last_name.value)
    fd.append('Form1', 'Form1')
    
    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            console.log(response)
            if (response["message"] == "success"){
                const form1 = document.getElementById("form1")
                const form2 = document.getElementById("form2")

                const nemtom = document.getElementById("nemtom")
                const title = document.getElementById("title")

                form1.animate([
                    { marginRight: "0", opacity: "1" },
                    { marginRight: "200px", opacity: "0.5" },
                    { marginRight: "400px", opacity: "0" },
                ], {
                    duration: 600,
                    iterations: 1,
                })
                
                nemtom.animate([
                    { opacity: "1" },
                    { opacity: "0.5" },
                    { opacity: "0" },
                ], {
                    duration: 600,
                    iterations: 1,
                })
                title.animate([
                    { opacity: "1" },
                    { opacity: "0.5" },
                    { opacity: "0" },
                ], {
                    duration: 600,
                    iterations: 1,
                })


                setTimeout(function(){
                    form1.style.display = "none"
                    
                    nemtom.style.opacity = "0"
                    nemtom.style.margin = "0 auto"

                    title.style.opacity = "0"
                    title.style.paddingLeft = "180px"
                    title.innerHTML = "Personal"

                    form2.style.opacity = "0"
                    form2.style.display = "block"

                    form2.animate([
                        { marginLeft: "300px", opacity: "0" },
                        { marginLeft: "150px", opacity: "0.5" },
                        { marginLeft: "0", opacity: "1" },
                    ], {
                        duration: 600,
                        iterations: 1,
                    })

                    nemtom.animate([
                        { opacity: "0" },
                        { opacity: "0.5" },
                        { opacity: "1" },
                    ], {
                        duration: 600,
                        iterations: 1,
                    })

                    title.animate([
                        { opacity: "0" },
                        { opacity: "0.5" },
                        { opacity: "1" },
                    ], {
                        duration: 600,
                        iterations: 1,
                    })

                    form2.style.opacity = "1"
                    nemtom.style.opacity = "1"
                    title.style.opacity = "1"
                }, 600)
            }
            else{
                $.each(response["message"], function(index, value){
                    if (index == "email"){
                        email_error.innerHTML = `<div class="alert alert-danger error-alert">${value}</div>`
                    }
                })
            }
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "Error while registering")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

function backToForm1(){
    const form1 = document.getElementById("form1")
    const form2 = document.getElementById("form2")

    const nemtom = document.getElementById("nemtom")
    const title = document.getElementById("title")

    form2.animate([
        { marginLeft: "0", opacity: "1" },
        { marginLeft: "170px", opacity: "0.5" },
        { marginLeft: "340px", opacity: "0" },
    ], {
        duration: 600,
        iterations: 1,
    })
    
    nemtom.animate([
        { opacity: "1" },
        { opacity: "0.5" },
        { opacity: "0" },
    ], {
        duration: 600,
        iterations: 1,
    })
    title.animate([
        { opacity: "1" },
        { opacity: "0.5" },
        { opacity: "0" },
    ], {
        duration: 600,
        iterations: 1,
    })


    setTimeout(function(){
        form2.style.display = "none"
        
        nemtom.style.opacity = "0"
        nemtom.style.margin = "0"

        title.style.opacity = "0"
        title.style.paddingLeft = "33px"
        title.innerHTML = "Account"

        form1.style.opacity = "0"
        form1.style.display = "block"

        form1.animate([
            { marginRight: "300px", opacity: "0" },
            { marginRight: "150px", opacity: "0.5" },
            { marginRight: "0", opacity: "1" },
        ], {
            duration: 600,
            iterations: 1,
        })

        nemtom.animate([
            { opacity: "0" },
            { opacity: "0.5" },
            { opacity: "1" },
        ], {
            duration: 600,
            iterations: 1,
        })

        title.animate([
            { opacity: "0" },
            { opacity: "0.5" },
            { opacity: "1" },
        ], {
            duration: 600,
            iterations: 1,
        })

        form1.style.opacity = "1"
        nemtom.style.opacity = "1"
        title.style.opacity = "1"
    }, 600)
}

//
// Form 2
//

function Form2Submit(){
    const image_error = document.getElementById("image_error")
    const birth_error = document.getElementById("birth_date_error")

    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const country = document.getElementById('id_country')
    const gender = document.getElementById('id_gender')
    const birth_date = document.getElementById('id_birth_date')
    const image = document.getElementsByName("image")[0].files[0]

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('country', country.value)
    fd.append('gender', gender.value)
    fd.append('birth_date', birth_date.value)
    fd.append('image', image)
    fd.append('Form2', 'Form2')
    
    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            console.log(response)
            if (response["message"] == "success"){
                const form2 = document.getElementById("form2")
                const form3 = document.getElementById("form3")

                const nemtom = document.getElementById("nemtom")
                const title = document.getElementById("title")

                form2.animate([
                    { marginRight: "0", opacity: "1" },
                    { marginRight: "200px", opacity: "0.5" },
                    { marginRight: "400px", opacity: "0" },
                ], {
                    duration: 600,
                    iterations: 1,
                })
                
                nemtom.animate([
                    { opacity: "1" },
                    { opacity: "0.5" },
                    { opacity: "0" },
                ], {
                    duration: 600,
                    iterations: 1,
                })
                title.animate([
                    { opacity: "1" },
                    { opacity: "0.5" },
                    { opacity: "0" },
                ], {
                    duration: 600,
                    iterations: 1,
                })


                setTimeout(function(){
                    form2.style.display = "none"
                    
                    nemtom.style.opacity = "0"
                    nemtom.style.margin = "0"
                    nemtom.style.float = "right"

                    title.style.opacity = "0"
                    title.style.paddingLeft = "330px"
                    title.innerHTML = "Secure"

                    form3.style.opacity = "0"
                    form3.style.display = "block"

                    form3.animate([
                        { marginLeft: "300px", opacity: "0" },
                        { marginLeft: "150px", opacity: "0.5" },
                        { marginLeft: "0", opacity: "1" },
                    ], {
                        duration: 600,
                        iterations: 1,
                    })

                    nemtom.animate([
                        { opacity: "0" },
                        { opacity: "0.5" },
                        { opacity: "1" },
                    ], {
                        duration: 600,
                        iterations: 1,
                    })

                    title.animate([
                        { opacity: "0" },
                        { opacity: "0.5" },
                        { opacity: "1" },
                    ], {
                        duration: 600,
                        iterations: 1,
                    })

                    form3.style.opacity = "1"
                    nemtom.style.opacity = "1"
                    title.style.opacity = "1"
                }, 600)
            }
            else{
                $.each(response["message"], function(index, value){
                    if (index == "image"){
                        image_error.innerHTML = `<div class="alert alert-danger error-alert">${value}</div>`
                    }
                    else if (index == "birth_date"){
                        birth_error.innerHTML = `<div class="alert alert-danger error-alert">${value}<br>Format: YYYY-MM-DD</div>`
                    }
                })
            }
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "Error while registering")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

function backToForm2(){
    const form2 = document.getElementById("form2")
    const form3 = document.getElementById("form3")

    const nemtom = document.getElementById("nemtom")
    const title = document.getElementById("title")

    form3.animate([
        { marginLeft: "0", opacity: "1" },
        { marginLeft: "170px", opacity: "0.5" },
        { marginLeft: "340px", opacity: "0" },
    ], {
        duration: 600,
        iterations: 1,
    })
    
    nemtom.animate([
        { opacity: "1" },
        { opacity: "0.5" },
        { opacity: "0" },
    ], {
        duration: 600,
        iterations: 1,
    })
    title.animate([
        { opacity: "1" },
        { opacity: "0.5" },
        { opacity: "0" },
    ], {
        duration: 600,
        iterations: 1,
    })


    setTimeout(function(){
        form3.style.display = "none"
        
        nemtom.style.opacity = "0"
        nemtom.style.margin = "0 auto"
        nemtom.style.float = "none"

        title.style.opacity = "0"
        title.style.paddingLeft = "180px"
        title.innerHTML = "Personal"

        form2.style.opacity = "0"
        form2.style.display = "block"

        form2.animate([
            { marginRight: "300px", opacity: "0" },
            { marginRight: "150px", opacity: "0.5" },
            { marginRight: "0", opacity: "1" },
        ], {
            duration: 600,
            iterations: 1,
        })

        nemtom.animate([
            { opacity: "0" },
            { opacity: "0.5" },
            { opacity: "1" },
        ], {
            duration: 600,
            iterations: 1,
        })

        title.animate([
            { opacity: "0" },
            { opacity: "0.5" },
            { opacity: "1" },
        ], {
            duration: 600,
            iterations: 1,
        })

        form2.style.opacity = "1"
        nemtom.style.opacity = "1"
        title.style.opacity = "1"
    }, 600)
}

//
// Form 3
//

function Form3Submit(){
    const pwd_error = document.getElementById("pwd_error")
    const pwd_comf_error = document.getElementById("pwd_comf_error")
    const uid_error = document.getElementById("uid_error")

    const csrf = document.getElementsByName("csrfmiddlewaretoken")
    const uid = document.getElementById("id_username")
    const pwd1 = document.getElementById("id_password1")
    const pwd2 = document.getElementById("id_password2")

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('username', uid.value)
    fd.append('password1', pwd1.value)
    fd.append('password2', pwd2.value)
    fd.append('Form3', 'Form3')
    
    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            console.log(response)
            if (response["message"] == "success"){
                location.href = location.href.replace("register", "login")
            }
            else{
                $.each(response["message"], function(index, value){
                    if (index == "password1"){
                        pwd_error.innerHTML = `<div class="alert alert-danger error-alert">${value}</div>`
                    }
                    else if (index == "password2"){
                        pwd_comf_error.innerHTML = `<div class="alert alert-danger error-alert">${value}</div>`
                    }
                    else if (index == "username"){
                        uid_error.innerHTML = `<div class="alert alert-danger error-alert">${value}</div>`
                    }
                })
            }
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "Error while registering")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}