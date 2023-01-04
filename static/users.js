document.addEventListener('DOMContentLoaded', function(){
    let btnGetUsers = document.getElementById('btnGetUsers')
    btnGetUsers.addEventListener('click', usersDataHandler);
})

function usersDataHandler(){
    console.log('Button Clicked')
    xhr = new XMLHttpRequest();
    xhr.open('POST', '/users', true);
    xhr.getResponseHeader('Content-type', 'application/json');
    xhr.onload = function(){
        str = "";
        if(this.status == 200){
            let list = document.getElementById('list');
            let obj = JSON.parse(this.responseText);
            console.log(obj);
            for(key in obj){
                str += `<li>${obj[key].name}</li>`;
            }
            list.innerHTML = str;
        }
        else{
            console.error("Some Error has occured.")
        }
    }
    xhr.send();
}
console.log("We are Done.")