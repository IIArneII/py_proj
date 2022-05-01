var btns = document.querySelectorAll('button')
btns.forEach(function(btn) {
    btn.addEventListener('click', async function(e) {
        e.preventDefault();
        console.log('\n' + btn.name);
        str = "/" + btn.name
        var response = await fetch(str, {
            method: "GET",
            headers: { "Accept": "application/json" }
        });
        if (response.ok === true) {
            let s = btn.name.split('/')
            if (s[1] == 'subscribe'){
                btn.classList.remove('button_read')
                btn.classList.add('button_unread')
                btn.innerText = 'Перестать читать'
                btn.name = s[0] + '/unsubscribe'
                console.log('Подписка на ', s[0]);
            }
            else{
                btn.classList.remove('button_unread')
                btn.classList.add('button_read')
                btn.innerText = 'Читать'
                btn.name = s[0] + '/subscribe'
                console.log('Отписка от ', s[0]);
            }
        }
        else{
            console.log('Не удалось подписаться / отписаться');
        }
    })
})