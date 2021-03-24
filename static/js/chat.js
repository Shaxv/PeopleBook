const roomValidation = () =>{
    const name = document.getElementsByName("title")[0]

    if (name.value == ""){
        errorHandler(name)
    }
    else{
        const csrf = document.getElementsByName('csrfmiddlewaretoken')
        const title = document.getElementsByName("title")
        const limit = document.getElementsByName("limit")

        const fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('title', title[0].value)
        fd.append('limit', limit[0].value)
        fd.append('create_room', 'create_room')

        $.ajax({
            type: 'POST',
            url: '',
            data: fd,
            success: function(response){
                if (response["message"] == "alreadyExists"){
                    handleAlerts("danger", "Already exists a room with the given name!")
                }
                else{
                    location.reload()
                }
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger', 'Something went wrong!')
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    }
}