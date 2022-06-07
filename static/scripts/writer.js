var writer = document.querySelector('.writer')

writer.addEventListener('click', async function(e) {
    if (e.target.classList.contains('writer')){
        writer.classList.add('hide')
    }
})

var writer_form = document.forms.writer

writer_form.addEventListener("submit", async function(event){
    event.preventDefault();
    var response = await fetch('/', {
        method: "POSt",
        headers: { "Accept": "application/json" },
        body: new FormData(writer_form)
    });
    if(response.ok === true){
        writer.classList.add('hide')
        if(writer_form.post.value == 'True'){
            if(!retweets.classList.contains('retweet_yes')){
                console.log(retweets)
                retweets.classList.add('retweet_yes')
            }
            let l = retweets.querySelector('.retweets_count')
            l.innerText = Number(l.innerText) + 1
        }
        else{
            if(!comments.classList.contains('comment_yes')){
                comments.classList.add('comment_yes')
            }
            let l = comments.querySelector('.comments_count')
            l.innerText = Number(l.innerText) + 1
        }
    }
});