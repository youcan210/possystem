
/*
ログイン成功時にページの遷移を実行

成功時ページ遷移する

*/

const passBtn = document.querySelector("#login-btn");

const user = document.querySelector("#pass_field");
eel.expose(js_login)
function js_login() {
    passBtn.addEventListener("click", async function() {
        pass = await eel.signup(user.value)();
        if (pass == true){
            console.log(pass);
            alert("pass is passed");
        }else if(pass == false){
            alert("pass not ok");
            js_login()
        }
        if(pass == true){
            move_from_page("index.html")
        }
    });
}


// ページ遷移
function move_from_page(target) {
    window.location.replace(target);//代入したタイミングでページを遷移する

}
window.addEventListener("DOMContentLoaded", () => {
    js_login()
});