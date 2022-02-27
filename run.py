import eel,json
from pos import Order,Init_pos,Item

"""
pos.pyから処理を受け取りJavaScriptへ各処理結果を渡す
"""

# Json形式にエンコードするクラス
class JsonEncoder(json.JSONEncoder):
    
    def default(self,object):
        if isinstance(object,str):
            return {
                "_type":"Item","value":{
                "code":object.item_code,
                "アイテム名":object.item_name,
                "金額":object.price
            }
                    }
        if isinstance(object,Item):
            return {'_type': 'Item', 'value': object.__dict__}
        return json.JSONEncoder.default(self, object)


# エンコードオブジェクトを生成
# アイテムオブジェクトをエンコードしJson形式で放出
item_master = "master.csv"
order = Order(item_master)
init = Init_pos(item_master)

@eel.expose
def send_js_master():
    # マスタ登録
    if init.run() is True:
        print("マスタ {} ok".format(init.run()))
    json_data = json.dumps(order.read_csv_file(),cls=JsonEncoder)
    return json_data

@eel.expose
def send_js_registor_to_csv(item:str,price:int):    
    # 商品を登録する
    # print("item: {}, price: {} ".format(item,price))
    if item and price is True:
        init.run()
    return order.registor_to_csv(item,price)
    

@eel.expose
def send_js_choice_item(choice,unit):
    # 商品を選択する
    # print("item: {}, price: {} ".format(choice,unit))
    return order.choice_item(choice,unit)

@eel.expose
# オーダー商品を削除する
def clear():
    order.init_order()
    order.item_order_list[:]= []
    order.unit_order_list[:] = []
    print("オーダー削除しました",order.item_order_list,order.unit_order_list)


@eel.expose
def js_view_purchase_history(choice,unit):
    # オーダー表示
    """初期化処理
        instance: アイテムオブジェクトの生成を初期化する
    """
    if order.init_order() == None:
        order.init_order()
    
    has_item = order.has_item_data(choice)
    json_data = json.dumps(has_item,cls=JsonEncoder)
    total = order.view_total()
    eel.view_order(json_data,total,unit)
    


@eel.expose
def send_js_calc_checkout(checkout):
    # 釣り計算
    change_money = order.calc_checkout(checkout)
    eel.view_checkout(change_money)

@eel.expose
def send_js_create_log_file(change_money):
    """jsからコールを受け取る

    Args:
        change_money (_type_): 合計金額を取得
    """
    # ログ出力
    order.create_log_file(change_money)
    eel.js_create_log_file()#pyからjsへ関数をコール
    init.run()
    order.init_order()


@eel.expose
def signup(user):
    """
    userのパスワードと登録パスワードを比較する
    """
    registor = "1111"
    if registor == user:# パスとuserが合致したなら真を返す
        print("pass is passed")
        return True
    elif registor != user:
        return False

if __name__ == "__main__":
    eel.init('pos')
    eel.start('signup.html',port=8000)
        