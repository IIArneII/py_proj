var btn_tweet = document.querySelector('.new_tweet')
if(btn_tweet){
    btn_tweet.addEventListener('click', async function(e) {
        let writer = document.querySelector('.writer')
        writer.classList.remove('hide')
        document.getElementById("post").value = "True";
        document.getElementById("parent_id").value = null;
    })
}