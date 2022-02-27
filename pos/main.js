// 入力
const item = document.querySelector("#item");
const price = document.querySelector("#price");
const masBtn = document.querySelector("#mas-btn");
const masArea = document.querySelector("#mas-area");

const order = document.querySelector("#order");
const unit = document.querySelector("#unit");
const ordBtn = document.querySelector("#ord-btn");
const clrBtn = document.querySelector("#clr-btn");

const odrTxtArea = document.querySelector("#odr-txt-area");

const entBtn = document.querySelector("#enter-btn");
const checkout = document.querySelector("#checkout");
const checkBtn = document.querySelector("#checkout-btn");

// マスタ登録

async function view_master() {
    const eel_data = await eel.send_js_master()();
    const json_data = JSON.parse(eel_data);
    for (i = 0;i < json_data.length;i++) {
        //*// console.log(json_data[i]);
        if ( json_data[i] != null) {
            masArea.innerHTML += 
            "アイテムコード:" + json_data[i].value.item_code + "  アイテム名: " + json_data[i].value.item_name + "  商品金額: " +  json_data[i].value.price + "円 " + "\n";
        }
    }
    
}

// 商品を登録 する
masBtn.addEventListener("click",() => {
    eel.send_js_registor_to_csv(item.value,price.value);
    clearText()
})


// 商品を選択する
ordBtn.addEventListener("click",async function() {
    await eel.send_js_choice_item(order.value,unit.value)();
    // オーダーを表示をpyへ呼び出す
    eel.js_view_purchase_history(order.value,unit.value)();
    clearText();
    
})

// オーダー表示
eel.expose(view_order)
function view_order(has_item,total,unit) {
    const json_data = JSON.parse(has_item);
    odrTxtArea.innerHTML += 
    "アイテムコード:" + json_data.value.item_code + ",アイテム名: " + json_data.value.item_name + ",商品金額: " + json_data.value.price  + "円, " + unit + "個" + "\n";
    odrTxtArea.innerHTML += total + "\n";
}



checkBtn.addEventListener("click", () => {
    eel.send_js_calc_checkout(checkout.value);
})
// 釣り計算
eel.expose(view_checkout)
function view_checkout(change_money) {
    
    odrTxtArea.innerHTML += "------------------------" + "\n";
    odrTxtArea.innerHTML += change_money + "です" + "\n";
    eel.send_js_create_log_file(change_money)//jsからpyへpy関数をコール
    
}

// 商品クリア
clrBtn.addEventListener("click", () => {
    eel.clear();
    clearText()
    odrTxtArea.innerHTML += "オーダーを削除しました" + "\n";
})


// ログ出力
eel.expose(js_create_log_file)
function js_create_log_file() {
    odrTxtArea.innerHTML += "購入したレシートを発行しました。お買い上げありがとうございます。"
}
function clearText() {
    item.value = '';
    price.value = '';
    order.value = '';
    unit.value = '';
}

view_master()

