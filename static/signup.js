document.addEventListener('DOMContentLoaded', function(){
    let signupbtn = document.getElementById('signupbtn');
    signupbtn.addEventListener('click', signupHandler);
})

function signupHandler(){
    console.log('Button Clicked.')
    const formElement = document.querySelector("form");
    const formData = new FormData(formElement);
    xhr = new XMLHttpRequest();
    xhr.open('POST', '/signup', true);
    console.log(formData)
    // xhr.setRequestHeader('Content-type', 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW');
    // params = `photo=${photo}&name: str = Form(), email: str = Form(), password: str = Form(), company: str = Form("")`
    xhr.onload = function(){
        if (xhr.status==200){
            console.log("Success");
            let r = JSON.parse(this.responseText);
            console.log(r)
            if(r.Message){
                let page = document.querySelector('body');
                page.innerHTML= `<h3>${r.Message} OR <a href="login">Click Here</a> to Login</h3>`;
            }
            else if (r.Error){
                let page = document.querySelector('body');
                page.innerHTML= `<h3>${r.Error}. <a href="login">Click Here</a> to Login</h3>`;
            }
        }
        else{
            console.error("Some Error has occured.")
        }
    }
    xhr.send(formData);
}