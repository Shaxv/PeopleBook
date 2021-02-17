const handleAlerts = (type, text) =>{
    document.getElementById("alert_box").innerHTML = 
    `<div class='fixed-top alert alert-${type} alert-dismissible fade show'>
        ${text}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`
}

const likeAnimate = (id) =>{
    const likeIcon = document.getElementById("likeIcon" + id)
    const likeContainer = document.getElementById("likeContainer" + id)

    likeIcon.animate([
        {transform: 'rotate(0deg)', fontSize: '16px'},
        {transform: 'rotate(-35deg)', fontSize: '19px'},
        {fontSize: '16px'},
    ], {
        duration: 500,
        iterations: 1,
    })

    likeContainer.classList.add("active")
}

const changeLikeCount = (id, status) =>{
    const likeCount = document.getElementById("likeCount" + id)

    if (likeCount.innerHTML == "0"){
        likeCount.innerHTML = "0"
    }
    else if (likeCount.innerHTML == "0" || status == "me"){
        likeCount.innerHTML = "You"
    }
    else if (likeCount.innerHTML == "1" && status == "me"){
        likeCount.innerHTML = "You"
    }
    else if (likeCount.innerHTML == "2" && status == "me"){
        likeCount.innerHTML = "You and " + likeCount.innerHTML + " other"
    }
    else if (likeCount.innerHTML != "1" && likeCount.innerHTML != "2" && status == "me"){
        likeCount.innerHTML = "You and " + likeCount.innerHTML + " others"
    }
    else{
        likeCount.innerHTML = likeCount.innerHTML
    }
}

const alreadyLiked = (id) =>{
    const form = document.getElementById("likeForm" + id)

    form.onsubmit = function(){
        handleAlerts(type="danger", text="You already liked the post!");
        return false;
    }
    var x = true
}

const like = (id) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const post = document.getElementsByName('post_id')

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[id].value)
    fd.append('post', post[id].value)

    if (typeof x == 'undefined'){
        $.ajax({
            type: 'POST',
            url: '',
            data: fd,
            success: function(response){
                likeAnimate(id)
                changeLikeCount(id=id, status="me")
                alreadyLiked(id)
            },
            error: function(error){
                handleAlerts('danger', 'Something went wrong!')
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    }
    else{
        handleAlerts('danger', 'You cant like twice')
    }
}

const focusComment = (id) =>{
    const input = document.getElementById("comment" + id)
    input.focus()
}