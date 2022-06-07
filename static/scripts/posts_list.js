var list = document.querySelectorAll('.list_element')
list.forEach(function(elem) {
    var btn = elem.querySelector('.likes')
    if(btn){
        btn.addEventListener('click', async function(e) {
            e.cancelBubble = true
            let url = elem.querySelector('a.date').href
            if(btn.classList.contains('like_yes')){
                var response = await fetch(url + '/unlike', {
                    method: "PUT",
                    headers: { "Accept": "application/json" }
                });
                if (response.ok === true) {
                    btn.classList.remove('like_yes')
                    let l = btn.querySelector('.likes_count')
                    l.innerText = Number(l.innerText) - 1
                }
            }
            else{
                var response = await fetch(url + '/like', {
                    method: "PUT",
                    headers: { "Accept": "application/json" }
                });
                if (response.ok === true) {
                    btn.classList.add('like_yes')
                    let l = btn.querySelector('.likes_count')
                    l.innerText = Number(l.innerText) + 1
                }
            }
        })
    }
    
    var btn_retweets = elem.querySelector('.retweets')
    if(btn_retweets){
        btn_retweets.addEventListener('click', async function(e) {
            e.cancelBubble = true
            let writer = document.querySelector('.writer')
            writer.classList.remove('hide')
            document.getElementById("post").value = "True";
            let id = elem.querySelector('a.date').href.split('/')
            document.getElementById("parent_id").value = id[id.length - 1];
            retweets = elem.querySelector('.retweets')
            console.log(retweets)
        })
    }

    var btn_comments = elem.querySelector('.comments')
    if(btn_comments){
        btn_comments.addEventListener('click', async function(e) {
            e.cancelBubble = true
            let writer = document.querySelector('.writer')
            writer.classList.remove('hide')
            document.getElementById("post").value = "False";
            let id = elem.querySelector('a.date').href.split('/')
            document.getElementById("parent_id").value = id[id.length - 1];
            comments = elem.querySelector('.comments')
        })
    }
    
    elem.addEventListener('click', async function(e) {
        location.href = elem.querySelector('a.date').href
    })
})

var list = document.querySelectorAll('.parent_post')
list.forEach(function(elem) {
    elem.addEventListener('click', async function(e) {
        e.cancelBubble = true
        location.href = elem.querySelector('a.date').href
    })
})