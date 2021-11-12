function save_post(postId) {

    let newPost = document.querySelector(`#p${postId}`).value;

    fetch('/save', {
       method:'PUT',
       body:JSON.stringify({
           text:newPost,
           postId:postId
       })
    });

    document.querySelector(`#f${postId}`).style.display = 'none';
    document.querySelector(`#e${postId}`).style.display = 'block';
    document.querySelector(`#t${posId}`).innerHTML = newPost;
}

function show_edit(postId) {

  document.querySelector(`#f${postId}`).style.display = 'block';
  document.querySelector(`#e${postId}`).style.display = 'none';
  document.querySelector(`#t${postId}`).style.display = 'none';

}

function like(postId) {

    fetch(`/like`, {
        method:'PUT',
        body:JSON.stringify({
           id:postId
        })
    });

    var currentLikes = parseInt(document.querySelector(`#tl${postId}`).innerHTML);
    var updatedLikes = currentLikes + 1;
    document.querySelector(`#tl${postId}`).innerHTML = updatedLikes;
    document.querySelector(`#l${postId}`).style.display = 'none';
    document.querySelector(`#dl${postId}`).style.display = 'block';

}

function dislike(postId) {

    fetch(`/dislike`, {
        method:'PUT',
        body:JSON.stringify({
           id:postId
        })
    });

    var currentLikes = parseInt(document.querySelector(`#tl${postId}`).innerHTML);
    var updatedLikes = currentLikes - 1;
    document.querySelector(`#tl${postId}`).innerHTML = updatedLikes;
    document.querySelector(`#l${postId}`).style.display = 'block';
    document.querySelector(`#dl${postId}`).style.display = 'none';

}