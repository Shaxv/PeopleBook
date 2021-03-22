const roomValidation = () =>{
    const name = document.getElementsByName("title")[0]

    if (name.value == ""){
        errorHandler(name)
    }
    else{
        const rooms = document.getElementById("rooms")
        const csrf = document.getElementsByName("csrfmiddlewaretoken")
        const name = document.getElementsByName("title")
        const limit = document.getElementsByName("limit")

        const fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('name', name[0].value)
        fd.append('limit', limit[0].value)

        $.ajax({
            type: 'POST',
            url: '',
            data: fd,
            success: function(response){
                rooms.innerHTML += `
                <div class="col-4">
                    <div class="card room-card">
                        <div class="card-header">
                            <h1>${name[0].value}</h1>
                        </div>
                        <div class="room-pics">
                            <img src="https://storage.cloud.google.com/peoplebook/{{user.profile.image}}" height="75" width="75" class="rounded-circle">
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="d-flex">
                            <form action="{% url 'chat_room' room %}" id="leftForm{{ forloop.counter }}" class="rightForm">
                                <button type="submit" class="btn btn-primary"><i class="fas fa-external-link-square-alt"></i> Enter</button>
                            </form>

                            <form action="" method="POST" id="rightForm{{ forloop.counter }}" class="rightForm">
                                {% csrf_token %}
                                <input type="hidden" name="room_id" value="{{ room.id }}">
                                <button type="submit" class="btn btn-danger" name="leave_room">Leave <i class="fas fa-sign-out-alt fa-lg"></i></button>
                            </form>
                        </div>
                            {% else %}
                                <form action="" method="POST">
                                    {% csrf_token %}
                                    <input type="hidden" name="room_id" value="{{ room.id }}">
                                    <button type="submit" class="btn btn-primary" name="enter_room"><i class="fas fa-sign-in-alt fa-lg"></i> Join</button>
                                </form>
                            {% endif %}
                        </div>
                        <div class="card-footer">
                            <p>Created {{ room.get_date }}</p>
                        </div>
                    </div>
                </div>
                `
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