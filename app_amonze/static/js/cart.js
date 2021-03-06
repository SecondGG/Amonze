var updateBtn = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener('click', function () {
        var itemId = this.dataset.product
        var action = this.dataset.action
        console.log('itemId:', itemId, 'action:', action)

        console.log('User :', user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in');
        }else{
            updateUserTransaction(itemId, action)
        }
    })
}

function updateUserTransaction(itemId, action){
    console.log('User logged in')
    
    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'itemId': itemId, 'action': action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data', data)
        location.reload()
    })
}