var list = document.querySelectorAll('.list_element')
list.forEach(function(elem) {
    var btn = elem.querySelector('.button')
    if(btn){
        btn.addEventListener('click', async function(e) {
            e.cancelBubble = true
            let url = elem.querySelector('a.profile_name').href
            if(btn.classList.contains('button_read')){
                var response = await fetch(url + '/subscribe', {
                    method: "PUT",
                    headers: { "Accept": "application/json" }
                });
                if (response.ok === true) {
                    btn.classList.remove('button_read')
                    btn.classList.add('button_unread')
                    btn.innerText = 'Перестать читать'
                }
            }
            else{
                var response = await fetch(url + '/unsubscribe', {
                    method: "PUT",
                    headers: { "Accept": "application/json" }
                });
                if (response.ok === true) {
                    btn.classList.remove('button_unread')
                    btn.classList.add('button_read')
                    btn.innerText = 'Читать'
                }
            }
        })
        btn.addEventListener('mouseover', async function(e) {
            if(btn.classList.contains('button_unread')){
                btn.innerText = 'Перестать читать'
            }
        });
        btn.addEventListener('mouseout', async function(e) {
            if(btn.classList.contains('button_unread')){
                btn.innerText = 'В читаемых'
            }
        });
    }
    elem.addEventListener('click', async function(e) {
        location.href = elem.querySelector('a.profile_name').href
    })
})