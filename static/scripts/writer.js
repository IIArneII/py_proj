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
        console.log(writer_form.post.value)
        if(writer_form.post.value == 'True'){
            if(!retweets.classList.contains('retweet_yes')){
                retweets.classList.add('retweet_yes')
            }
        }
        else{
            if(!comments.classList.contains('comment_yes')){
                comments.classList.add('comment_yes')
            }
        }
        writer.classList.add('hide')
    }
});