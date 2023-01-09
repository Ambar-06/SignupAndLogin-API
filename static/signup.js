document.addEventListener('DOMContentLoaded', function(){
    let signupbtn = document.getElementById('signupbtn');
    signupbtn.addEventListener('click', signupHandler);
})

function ValidateEmail(inputText)
{
var mailformat = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}/;
    if(inputText.match(mailformat))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function ValidatePassword(password)
{
    if (password.length>=8)
    {
        return true;
    }
    else
    {
        return false;
    }
}
function signupHandler(){
    console.log('Button Clicked.')
    const formElement = document.querySelector("form");
    const formData = new FormData(formElement);
    let email = formData.get('email')
    let p = formData.get('password')
    console.log(email)
    val_email = ValidateEmail(email)
    val_pass = ValidatePassword(p)
    if(val_email==true && val_pass==true){
        xhr = new XMLHttpRequest();
        xhr.open('POST', '/signup', true);
        console.log(formData)
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
    else if(val_email==false){
        alert("You have entered an invalid email address!");    //The pop up alert for an invalid email address
        document.form1.text1.focus();
    }
    else if (val_pass==false){
        alert("Your password must be at least 8 characters long!");    //The pop up alert for password lenght less than 8 
        document.form1.text1.focus();
    }
}