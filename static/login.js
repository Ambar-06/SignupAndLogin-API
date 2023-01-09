document.addEventListener('DOMContentLoaded', function(){
    let btnLogin = document.getElementById('btnLogin');
    btnLogin.addEventListener('click', loginHandler);
})

function loginHandler(){
    console.log('Button clicked.');
    const details = new FormData(form);
    let email = details.get('email');
    let p = details.get('password')
    console.log(email)
    console.log(p)
    xhr = new XMLHttpRequest();
    xhr.open('POST', '/login', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    let params = `username=${email}&password=${p}`;
    console.log(params)
    xhr.onload = function(){
        if(xhr.status==200){
            let r = JSON.parse(this.responseText);
            window.location.replace("/users");
        }
        else if(xhr.status==404){
            let r = JSON.parse(this.responseText);
            let body = document.querySelector('body')
            body.innerHTML = `<h3>${r.detail}</h3>`
        }
        else if(xhr.status==400){
            let r = JSON.parse(this.responseText);
            let body = document.querySelector('body')
            body.innerHTML = `<h3>${r.detail}</h3>`
        }
        else{
            console.error("Some Error has occured.")
        }
    }
    xhr.send(params);
}
