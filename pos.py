
# *todoマスタデータを読み込む
# *// 商品を選択する
# *// 商品を登録する
# *// 商品を表示する
# *// 商品合計計算


# *// 釣り計算
# *// ログ出力

import csv,os,sys,datetime,pprint,logging
# import pandas as pd
from logging import getLogger


item_master = "master.csv"

class Init_pos:
    def __init__(self,item_master):
        self.item_master = item_master

    def run(self):
        order = Order(item_master)
        csv_data = order.read_csv_file()
        self.item_master = []
        for data in csv_data:
            self.item_master.append(Item(data.item_code,data.item_name,data.price))
        # print(self.item_master)
        return True


### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price
    
    def __repr__(self):
        return f'{self.item_code,self.item_name,self.price}'

    
    
### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.unit_order_list=[]
        self.total_order_list=[]
        self.item_master=item_master
    
    def __del__(self):
        self.item_order_list[:] = []
        
    def add_item_order(self,item_code):
        self.item_order_list.append(item_code)
    
    def add_unit_order(self,unit):
        self.unit_order_list.append(unit)
    
    def add_total_order(self,total):
        self.total_order_list.append(total)

# 各ビューリストを参照
    def view_item_list(self):
        for item in self.item_order_list:
            return "商品コード: {},商品名: {},商品金額: {}".format(item.item_code,item.item_name,item.price)
    
    def view_unit_list(self):
        for unit in self.unit_order_list:
            return "商品個数: {} ".format(unit)
    
    def view_total(self):
        total = self.calc_sum_item()
        return "合計金額 {} 円".format(total)
    
    def view_purchase_hisotry(self):
        self.view_item_list()
        self.view_unit_list()
        self.view_total()
        return "{} {} {}".format(
            self.view_item_list(),
            self.view_unit_list(),
            self.view_total()
            )

# CSVから読み込み、書き込み実行
    def check_csv_file(self):
        file_name = 'master.csv'
        if os.path.exists(file_name):
                return file_name
        else:
                print(file_name,'存在しません')

    def read_csv_file(self)->None:
        self.item_master = []
        with open("master.csv",encoding="utf-8")as f:
            master = csv.reader(f)
            for item_code,item_name,price in master:
                self.item_master.append(Item(item_code,item_name,price))
        return self.item_master
    
    def writer_csv_file(self,item_name:str,price:str)->None:
        self.check_csv_file()# ファイルの存在を確認
        # nxt_code = len(self.item_master) + 1
        # fill_digits = str(nxt_code).zfill(3)
        # 0桁をマスタの登録数から取得し、次の0桁番号を生成
        digit = 1
        for item in self.item_master:
            code = int(item.item_code)
            code += digit
            fill_digits = str(code).zfill(3)
        print(fill_digits)

        
        with open("master.csv","a",newline="")as f:
            writer = csv.writer(f)
            writer.writerow([fill_digits,item_name,price])
            self.item_master.append(Item(fill_digits,item_name,price))
    
    def create_log_file(self,change_money):
        """
        商品購入を履歴としてログファイルへ出力
        
        """
        logger = getLogger(__name__)
        sh = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%S")
        # ロギングハンドラで受け取ったログレコードをフォーマットする
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        logger.warning("unauthorized")
        logging.basicConfig(level=logging.DEBUG)
        logging.info("purchased info ok")
        
        now = datetime.datetime.now()
        time_format = 'log_'+now.strftime('%Y%m%d%H%M')
        publish = ['レシートを発行します'] 

        total = ['合計金額 :￥{}'.format(self.calc_sum_item())]
        change_money = [change_money]
        with open(time_format,'w',encoding='utf-8') as f:
            writer = csv.writer(f,delimiter='\t')
            writer.writerow(publish)
            for item in self.item_order_list:
                purchased = ['商品コード :{}  商品名 :{}  商品金額 :￥{}円' .format(item.item_code,item.item_name,item.price)]
                writer.writerow(purchased)
            writer.writerow(total)
            writer.writerow(change_money)
            f.close()
        

        

# チェック
    def interval_break(self,order):
            if order == "0":
                print("中断します")
                return False

    def check_order(self,order:int,unit:int)->True:
        # *//print("order:",type(order))
        if not order == "" and not unit == "":
            # *//print("ok")
            return True
        return False

    def duplicated(self,item_name:str)->str:
        res_str_list = set([item.item_name for item in self.item_master]) # 重複を見つける
        if item_name in list(res_str_list):
            print("商品は重複しています もう一度入力してください")
            return self.registor_to_csv()
        else:
            return item_name
# 登録処理
    def registor_to_csv(self,item_name,price):
        """
        CSVファイルへコンソールから登録処理を実行
        連番で商品を追加する※003~005
            商品名、金額入力
            CSVへ書き込み
            
        """
        while True:
            # item_name = input("登録する商品名を入力してください(入力しないなら0): ")
            if item_name == "0":
                pass
            else:
                # price = input("商品の金額を入力してください: ")
                ans_duplicate = self.duplicated(item_name)# 重複ならもう一度入力をやり直す
                self.writer_csv_file(ans_duplicate,price)
            # if not self.over_input():break# 登録終了確認
            break




    def choice_item(self,order:int,unit:int)->int:
        """
        商品を選択したら、オーダーリストへ選択した商品を追加する
        
        """
        # order = input("商品を選択してください(コード番号): ")
        # unit = input("個数を入力してください")

        self.check_order(order,unit)# *!True
        has_item = self.has_item_data(order) # アイテムデータ取得

        self.add_item_order(has_item)
        self.add_unit_order(unit)

        # if not self.over_input():break# 登録終了


# アイテムデータ取得
    def has_item_data(self,code:int)->tuple:
        zero_fill = str(code).zfill(3)# 0digits
        for items in self.item_master:
            if zero_fill == items.item_code:
                return items
            
# 計算処理
    def calc_sum_item(self)->int:
        total = 0
        for item,unit in zip(self.item_order_list,self.unit_order_list):
            total_price = int(item.get_price()) * int(unit)
            total += total_price
        self.add_total_order(total)
        return total

    def calc_checkout(self,payment:int)->int:
        # payment = int(input("支払額を入力してください: ￥"))
        res_payment = int(payment) - self.calc_sum_item()
        if res_payment < 0:
            print("もう一度支払金額を入力してください。{}円足りません".format(abs(res_payment)))
            return self.calc_checkout()
        elif res_payment == 0:
            print("お釣りは0円です")
            return res_payment

        return "お釣り: ￥{} 円".format(res_payment)

# 入力終了処理
    def over_input(self):
        over = input('終了しますか?終了ならyes(y)続行ならenterを押してください: ')
        if over == 'y':
            return False
        else:
            return True
    
    def init_order(self):
        self.order = Order(self.item_master)
        
    
