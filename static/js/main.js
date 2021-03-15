
//
//
//

const handleAlerts = (type, text) =>{
    document.getElementById("alert_box").innerHTML = 
    `<div class='fixed-top alert alert-${type} alert-dismissible fade show'>
        ${text}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`
}

const likeAnimate = (id, type) =>{
    const likeIcon = document.getElementById(type + id)

    likeIcon.animate([
        {transform: 'rotate(0deg)', fontSize: '16px'},
        {transform: 'rotate(-35deg)', fontSize: '19px'},
        {fontSize: '16px'},
    ], {
        duration: 500,
        iterations: 1,
    })
}

const commentLikeAnimate = (id) =>{
    const likeCount = document.getElementById("commentLikeCount" + id)

    likeCount.animate([
        {fontSize: '20px'},
        {fontSize: '15px'},
    ], {
        duration: 400,
        iterations: 1,
    })
}

const focusComment = (id) =>{
    const input = document.getElementById("comment" + id)
    input.focus()
}

//
// Post like system
//

const changeLikeCount = (id, status) =>{
    const likeCount = document.getElementById("likeCount" + id)
    if (likeCount.innerHTML == "1" && status == "me" || likeCount.innerHTML == "0" && status == "me"){
        likeCount.innerHTML = "You"
    }
    else if (likeCount.innerHTML == "2" && status == "me"){
        likeCount.innerHTML = "You and 1 other"
    }
    else if (likeCount.innerHTML != "1" || likeCount.innerHTML != "2" && status == "me"){
        s = parseInt(likeCount.innerHTML)-1
        likeCount.innerHTML = "You and " + s + " others"
    }
    else{
        likeCount.innerHTML = likeCount.innerHTML
    }
}

const alreadyLiked = (id, status) =>{
    const form = document.getElementById("likeForm" + id)

    if (status == "unlike"){
        form.onsubmit = function(){
            unlike(id)
            return false;
        }
    }
    else if (status == "like"){
        form.onsubmit = function(){
            like(id)
            return false;
        }
    }
}

const like = (id) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const post = document.getElementById('post_id' + id)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[id].value)
    fd.append('post_id', post.value)
    fd.append('like', 'like')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            likeAnimate(id, "likeIcon")
            const likeCount = document.getElementById("likeCount" + id)
            if (likeCount.innerHTML == "0"){
                likeCount.innerHTML = "You"
            }
            else if (likeCount.innerHTML == "1"){
                likeCount.innerHTML = "You and 1 other"
            }
            else{
                likeCount.innerHTML = "You and " + likeCount.innerHTML + " others"
            }
            alreadyLiked(id, status="unlike")
            const likeContainer = document.getElementById("likeContainer" + id)
            likeContainer.classList.add("active")
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

const unlike = (id) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const post = document.getElementById('post_id' + id)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[id].value)
    fd.append('post_id', post.value)
    fd.append('unlike', 'unlike')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            alreadyLiked(id, status="like")        
            likeAnimate(id, "likeIcon")
            const likeCount = document.getElementById("likeCount" + id)
            const s = likeCount.innerHTML.replace(/[^0-9]/g,'');
            likeCount.innerHTML = s
            if (s == 0){
                likeCount.innerHTML = 0
            }
            else{
                likeCount.innerHTML = s
            }
            const likeContainer = document.getElementById("likeContainer" + id)
            likeContainer.classList.remove("active")
        },
        error: function(error){
            console.log(error)
            handleAlerts('danger', 'Something went wrong while unlikeing')
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

//
// Post system
//

const newPost = () =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const content = document.getElementsByName('content')

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('content', content[0].value)
    fd.append('new_post', 'new_post')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            postHandler('create', fd)
            handleAlerts("success", "Successfully created a post!")
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "There was an error!")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

const deletePost = (id) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const post_id = document.getElementById('remove_post_id' + id)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[id].value)
    fd.append('post_id', post_id.value)
    fd.append('post_remove', 'post_remove')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            handleAlerts("success", "Successfully Removed a post!")
            postHandler('remove', "", id)
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "There was an error!")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

const postHandler = (status, fd, id) =>{
    if (status == 'remove'){
        const post = document.getElementById("post" + id)
        post.innerHTML = ""
    }
    else if (status == 'create'){
        const content = fd.get('content')
        const newPost = document.getElementById("newPost")
        
        newPost.innerHTML = newPost.innerHTML + newPostContent(content)    
    }
}

//
// Like Comment
//

const likeCommentList = (id, status, name) =>{
    const likeCountContainer = document.getElementById("commentLikeCountBadge" + id)
    const likeCount = document.getElementById("commentLikeCount" + id)
    const likeList = document.getElementById("like-list" + id)
    const likeListUl = document.getElementById("like-list-ul" + id)

    if (status == "like"){

        if (likeCount.innerHTML == "0"){
            likeListUl.innerHTML = `<li>${name}</li>`
        }
        else{
            likeListUl.innerHTML += `<li>${name}</li>`
        }
            
        const s = likeCount.innerHTML.replace(/[^0-9]/g,'');
        likeCount.innerHTML = parseInt(s) + 1

        Egy()

    }
    else if (status == "unlike"){
        const s = likeCount.innerHTML.replace(/[^0-9]/g,'');
        likeCount.innerHTML = parseInt(s) - 1
        
        const toReplace = likeListUl.innerHTML.replace(`<li>${name}</li>`, `<li></li>`)
        likeListUl.innerHTML = toReplace

        if (likeCount.innerHTML != "0"){
            Egy()
        }
        else{
            Ketto()     
        }
    }

    if (likeCount.innerHTML != "0"){
        Egy()  
    }

    function Egy(){
        likeCountContainer.style.cursor = "pointer"

        likeCountContainer.onmouseover = function(){
            likeList.style.visibility = "visible"
            likeList.style.opacity = "1"
        }
        likeCountContainer.onmouseleave = function(){
            likeList.style.visibility = "hidden"
            likeList.style.opacity = "0"
        } 
    }

    function Ketto(){
        likeCountContainer.style.cursor = "default"

        likeCountContainer.onmouseover = null
        likeCountContainer.onmouseleave = null   
    }
    
}

const alreadyCommentLiked = (id, status, name) =>{
    const form = document.getElementById("likeCommentForm" + id)
    const likeCommentIcon = document.getElementById("likeCommentIcon" + id)

    if (status == "unlike"){
        form.onsubmit = function(){
            unlikeComment(id, name)
            return false;
        }
        likeCommentIcon.classList.add("active")
    }
    else if (status == "like"){
        form.onsubmit = function(){
            likeComment(id, name)
            return false;
        }
        likeCommentIcon.classList.remove("active")
    }
}

const likeComment = (id, name) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const comment_id = document.getElementById('comment_id' + id)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[id].value)
    fd.append('comment_id', comment_id.value)
    fd.append('comment_like', 'comment_like')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(response){
            alreadyCommentLiked(id, "unlike", name)
            commentLikeAnimate(id)
            likeCommentList(id, "like", name)
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "Error while liking the comment!")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

const unlikeComment = (id, name) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const comment_id = document.getElementById('comment_id' + id)
    
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[id].value)
    fd.append('comment_id', comment_id.value)
    fd.append('comment_unlike', 'comment_unlike')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(){
            alreadyCommentLiked(id, "like", name)
            commentLikeAnimate(id)
            likeCommentList(id, "unlike", name)
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "Error while unliking the comment!")
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

//
// Comment system
//

const addComment = (id, image, name) =>{
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    const comment_post_id = document.getElementById("comment_post_id" + id)
    const content = document.getElementById("content" + id)

    const fd = new FormData
    fd.append('comment_post_id', comment_post_id.value)
    fd.append('content', content.value)
    fd.append('add_comment', 'add_comment')

    $.ajax({
        type: 'POST',
        url: '',
        data: fd,
        success: function(){
            commentHandler(id, "add", content, image, name)
        },
        error: function(error){
            console.log(error)
            handleAlerts("danger", "Error while adding comment")
        },
        cache: false,
        contentType: false,
        processData: false,
    })

}

const commentHandler = (id, status, content, image, name) =>{
    const newComment = document.getElementById("newComment" + id)

    if (status == "add"){
        newComment.innerHTML += `
            <div class="comment">
                <div class="card-header">
                    <img src="/${image}" height="36">
                </div>
                <div class="comment-body">
                    <a href="">
                        <h5>${name}</h5>
                    </a>
                    <p class="post-content">${content.value}</p>
                </div>
                <span style="position: absolute; left: 52px; top: 82px; font-weight: 400; font-size: 12px;">To like the comment or reply to it, reload the page.</span>
            </div>
        `
    }
}


//
// Test
//

const Test1 = (response) =>{
    const proba = document.getElementById("proba")
    const data = response.data

    $.each(data, function(index, value){
        proba.innerHTML += (`
        <div class="card p-3 mt-3 mb-3">
        ${value.author}
        <br>
        ${value.content}
        <br><br>
        ${value.date_posted}
        </div>`)
    })
}