function addToCart(id, TenSP, Gia){
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'TenSP': TenSP,
            'Gia': Gia
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(err => console.error(err))
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?") == true) {
        fetch('/api/pay', {
            method: 'post',
            headers: {
            'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            console.info(data)
            if (data.code === 200)
                alert("Thanh toán thành công")
                location.reload()
        }).catch(err => console.error(err))
    }
}

function updateCart(id, obj){
    fetch('/api/update-cart',{
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity

        let amount = document.getElementById('total-amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}

function deleteCart(id){
    if (confirm("Bạn chắc chắn muốn xóa không ?") == true){
        fetch('/api/delete-cart/' + id,{
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let counter = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity

            let amount = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let e = document.getElementById("product"+id)
            e.style.display = "none"
        }).catch(err => console.error(err))
    }
}

