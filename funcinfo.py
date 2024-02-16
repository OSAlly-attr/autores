import time
import datetime
import csv
import requests
import operator
import unicodedata
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
from func import pw_range, account_password_path

# csvを読み込む関数
def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        return data

# ChromeWebdriverを起動する関数
def chrome_result():
    ChromeOptions = Options()
    ChromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)
    auto_reservation1(driver)
    return

# LINEに送信する関数
def send_line(text):
    TOKEN =  'Ghbzj30VWqKNzYTk1dZnh3NjkjRUntNJdUxCQNfEkOx'
    api_url = 'https://notify-api.line.me/api/notify'
    send_text = text
    TOKEN_dic = {'Authorization': 'Bearer ' + TOKEN}
    send_dic = {'message': send_text}
    requests.post(api_url, headers=TOKEN_dic, data=send_dic)

# winlist.txtを読み込む関数 (重複は消す)
def read_winlist():
    with open('./winlist.txt') as f:
        for line in f:
            winlist.append(line.rstrip('\n'))

# winlistからaccount_passwordを生成する関数
def generate_ap(ap, wl):
    res = []
    for w in wl:
        for i in range(len(ap)):
            if w == ap[i][0].zfill(8):
                res.append(ap[i])
        if len(res) == 0:
            print("アカウントが見つかりません。IDを確認してください。")
            return False
    return res

# xpathでクリックする関数
def xpath_click(driver, xpath):
    if no_error[0]:
        for i in range(trymax):
            try:
                driver.find_element(By.XPATH, xpath).click()
                return
            except:
                time.sleep(dtry)
        no_error[0] = False

# xpathで入力する関数
def xpath_send_keys(driver, xpath, keys):
    if no_error[0]:
        for i in range(trymax):
            try:
                tmp = driver.find_element(By.XPATH, xpath)
                tmp.clear()
                tmp.send_keys(keys)
                return
            except:
                time.sleep(dtry)
        no_error[0] = False

# idで入力する関数
def id_send_keys(driver, id, keys):
    if no_error[0]:
        for i in range(trymax):
            try:
                tmp = driver.find_element(By.ID,id)
                tmp.clear()
                tmp.send_keys(keys)
                return
            except:
                time.sleep(dtry)
        no_error[0] = False

# xpathで要素を取得する関数
def xpath_get(driver, xpath):
    if no_error[0]:
        for i in range(trymax):
            try:
                return driver.find_element(By.XPATH, xpath).text
            except:
                time.sleep(dtry)
        no_error[0] = False

# xpathでページ遷移ができるまで待つ関数(要素が存在するかチェックする関数)
def xpath_exist_check(driver, xpath, tm):
    for i in range(tm):
        try:
            if len(driver.find_elements(By.XPATH, xpath))!=0:
                return True
            time.sleep(dtry)
        except:
            time.sleep(dtry)
    return False

# 当選確認する関数
def infocheck(driver, x, account_password):
    try:
        # if '当選' in xpath_get(driver, status_top_attr):
        xpath_click(driver, all_status)
        xpath_click(driver, num_view)
        xpath_click(driver, view_twenty)
        tmp = []
        for i in range(1,16):
            if '当選' in xpath_get(driver, view_item_attr1 + str(i) + view_item_attr2) and '確定' not in xpath_get(driver, view_item_attr1 + str(i) + view_item_attr2):
                top_gym = xpath_get(driver, view_item_gym1 + str(i) + view_item_gym2)
                top_date = xpath_get(driver, view_item_date1 + str(i) + view_item_date2)
                top_time = xpath_get(driver, view_item_time1 + str(i) + view_item_time2) 
                xpath_click(driver, view_item_a1 + str(i) + view_item_a2)
                top_sports = xpath_get(driver, view_item_sports)
                top_item = [top_gym[:top_gym.find(' /')], top_date[top_date.rfind('/')+1:top_date.find('(')], top_date[top_date.find('('):],str(top_time),top_sports]
                tmp.append(top_item)
                # winlist.append([str(account_password[x][0].zfill(8)), top_item[0], top_item[1], top_item[2], top_item[3]])
                # 利用予約
                xpath_click(driver,confirm_win)
                xpath_click(driver, howtopay)
                xpath_click(driver, confirm_pay)
                time.sleep(0.5)
                xpath_click(driver, confirm_appl)
                time.sleep(0.5)
                xpath_click(driver, confirm_err)
                time.sleep(0.5)
                xpath_click(driver, confirm_check)
                xpath_click(driver, confirm_appl2)
                xpath_click(driver, to_status_appl)
                xpath_click(driver, num_view)
                xpath_click(driver, view_twenty)
        if len(tmp)>0:
            sendtext = ''
            for j in range(len(tmp)):
                sendtext = sendtext + '\n' + str(account_password[x][0].zfill(8)) + ' ' + str(tmp[j][0]) + ' ' + str(tmp[j][1]) + ' ' + str(tmp[j][2]) + ' ' + str(tmp[j][3]) + ' ' + str(tmp[j][4])
            send_line(sendtext)
            print(sendtext)
    except:
        return

# main関数
def auto_reservation1(driver):
    # アカウントパスワードリストを読み込み
    ap = read_csv(account_password_path[0])
    # harp札幌 ページ読み込み
    time.sleep(0.2)
    driver.get('https://yoyaku.harp.lg.jp/sapporo/')
    
    # winlist.txtを読み込む
    read_winlist()
    # print(winlist)
    wl = list(set(winlist))
    print(wl)
    # winlist_からaccount_passwordを生成
    account_password = generate_ap(ap,wl)
    if account_password == False:
        driver.quit()
        return
    
    # 施設予約へ
    for x, i in enumerate(account_password, 1):
        # 進行状況
        print('現在' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')')
        # 施設予約ログイン
        while True:
            xpath_click(driver, facility_reservation_login_button)
            if xpath_exist_check(driver, login_button, 15):
                break
            else:
                time.sleep(1)
                driver.back()
                time.sleep(0.5)
                driver.refresh()
                time.sleep(0.8)
        #ウィンドウサイズを指定のサイズに変更
        driver.set_window_size(1200,900)   
        # 番号・パスワード入力・ログイン
        id_send_keys(driver, registered_number_text_field, i[0].zfill(8))
        id_send_keys(driver, password_text_field, i[1])
        xpath_click(driver, login_button)
        # 利用者番号・パスワードが間違っている、もしくは登録していない場合
        if xpath_exist_check(driver, account_alert, 5):
            print('ログインエラー。アカウント登録情報に誤りがあります。\n' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
            send_line('\nログインエラー。アカウント登録情報に誤りがあります。\n' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
            # ログアウト
            xpath_click(driver, main_menu2)
            time.sleep(0.5)
            xpath_click(driver, logout_button_la)
            continue
        # ページ遷移確認
        while True:
            time.sleep(0.5)
            if xpath_exist_check(driver, now_login, 15):
                break
            elif xpath_exist_check(driver, login_button, 15):
                xpath_click(driver, login_button)
            else:
                driver.back()
        
        #　有効期限切れの場合はスキップ
        if xpath_exist_check(driver, expiration_alert, 15):
            # ログアウト       
            xpath_click(driver, main_menu2)
            time.sleep(0.5)
            xpath_click(driver, logout_button_s)
            print(str(x)+"番目のアカウント(ID: "+ str(i[0].zfill(8)) +")を飛ばしました。")
            continue
        
        # 当選確認と利用予約
        infocheck(driver, x-1, account_password)
        
        # ログアウト
        xpath_click(driver, main_menu2)
        time.sleep(0.5)
        xpath_click(driver, logout_button)
        # エラーが出たら通知して終了
        if no_error[0] == False:
            send_line('\nエラーが発生しました。\n' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
            print('エラーが発生しました。' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
            return
    
    # winlist1 = sorted(winlist, key=operator.itemgetter(2, 4, 1, 0))
    # with open('./result/rsl_'+ res_acc[0], 'a', newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(winlist1)
    # newres = read_csv('./result/rsl_'+ res_acc[0])
    # newres = sorted(newres,  key=operator.itemgetter(2, 4, 1, 0))
    # with open('./result/rsl_'+ res_acc[0], 'w', newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerows(winlist1)
    #終了と通知
    driver.quit()
    send_line("\n"+"当選確認が完了しました。")
    print("当選確認が完了しました。")


# 利用年・月・体育館・日付・時間帯
today = datetime.date.today()
delta = datetime.timedelta(days=15)
day = today+delta
year_month = [str(day.year), str(day.month).zfill(2)]
gym_day_time = [[0 for i in range(3)] for j in range(15)]
for i in range(15):
    gym_day_time[i] = ["","",""] # 初期化
# try繰り返す回数
trymax = 80
# try間隔
dtry = 0.1
# エラーフラグ
no_error = [True]

# 参照するアカウントリスト
# res_acc = [""]

# winlist.txtのアカウントIDリスト
winlist = []

# ログイン
facility_reservation_login_button = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[2]/div[1]/span[1]/a"
#　利用者番号
registered_number_text_field = "input-21"
# パスワード
password_text_field = "input-25"
# ログイン
login_button = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div/div[1]/div/button"
# ログインエラー
account_alert = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/ul/li"
logout_button_la = "/html/body/div/div/div[3]/header/div/div[3]/div[1]/nav/div[2]/a[1]/div[2]/div"
# 利用事項同意
agree_check_box = "/html/body/div/div/div[3]/div/main/div[1]/form/div/span/div/div/div[1]/div/label"
agree_button = "/html/body/div/div/div[3]/div/main/div[2]/div/div[1]/div/button/span"

# すべての申込状況へ
all_status = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[2]/a"
# 表示件数
num_view  = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div[1]"
# 20件ずつ
view_twenty = "/html/body/div/div/div[8]/div/div[2]/div/div"
# 項目1
view_item_attr1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_attr2 = "]/div[1]/div[1]/span"
view_item_gym1 =  "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_gym2 = "]/div[1]/div[2]/div[2]/div[1]/a"
view_item_date1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_date2 = "]/div[1]/div[2]/div[2]/div[2]/time[1]"
view_item_time1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_time2 = "]/div[1]/div[2]/div[2]/div[2]/span[2]"
view_item_a1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_a2 = "]/div[1]/div[2]/div[2]/div[1]/a"
view_item_sports = '/html/body/div/div/div[3]/div/main/div[1]/div[4]/div/div/div/div/div[1]/div/dl[1]/dd'
# 当選確定する
confirm_win = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/dl[2]/dd/div[2]/a/span"
# 支払い方法へ
howtopay = "/html/body/div/div/div[3]/div/main/div[2]/div/div[1]/div/button"
# 確認
confirm_pay = "/html/body/div/div/div[3]/div/main/div[1]/div[5]/div/div[1]/div/button"
# 申込確定
confirm_appl = "/html/body/div/div/div[3]/div/main/div[2]/div/div[1]/div/button[1]"
# エラーがあります
confirm_err = "/html/body/div/div/div[3]/div/main/div[2]/div/div[2]/div/div/div/button"
# 注意事項確認
confirm_check = "/html/body/div/div/div[3]/div/main/div[1]/form/div[4]/div[2]/div[3]/span/div/div/div[1]"
# 申込確定2回目
confirm_appl2 = "/html/body/div/div/div[3]/div/main/div[1]/div[5]/div/div[1]/div/button[1]"
# 申込状況へ
to_status_appl = "/html/body/div/div/div[3]/div/nav/ul/li[3]/a/span"
# ホームへ
to_home_from_status = "/html/body/div/div/div[3]/div/nav/ul/li[1]/a/span"

# 申し込み状況top属性
status_top_attr = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span"
status_top_gym = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/a"
status_top_date = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/time[1]"
status_top_time = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/span[2]"

# ヘッダーのログイン中
now_login = "/html/body/div/div/div[2]/header/div/div[4]/span[1]"
# 有効期限切れ
expiration_alert = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div/div/div/div/div/div[2]/a"


# 連続時
# 施設名
facility_name_default = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/div[1]/div/form/dl[1]/dd/span[3]/span/div/div[2]/div[1]/div[1]/div[1]/span/span/span"
# 施設バツ
gym_clear = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/div[1]/div/form/dl[1]/dd/span[3]/span/div/div[2]/div[1]/div[1]/div[2]/div/button"
# 施設
facility_name_text_field_q = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/div[1]/div/form/dl[1]/dd/span[3]/span/div/div[2]/div[1]/div[1]/div[1]/input"
facility_item_q = "/html/body/div/div/div[10]/div/div[2]/div/div/div"
# 利用日時バツ
date_of_use_clear = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/div[1]/div/form/dl[2]/dd/span[1]/div[1]/div/div[1]/div[2]/div/button"
# 利用日時
date_of_use_q = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/div[1]/div/form/dl[2]/dd/span[1]/div[1]/div/div[1]/div[1]/input"
# 検索
facility_search_button_q = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[1]/div/div[1]/div/form/div/div[1]/button"

#初回時
# 利用目的
purpose_of_use = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[1]/dd/span[1]/span/div/div[2]/div[1]/div[1]/div[1]/input"
# 項目(バレーボール)
purpose_of_item = "/html/body/div/div/div[9]/div/div[4]/div"
# 施設
facility_name_text_field = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[1]/dd/span[3]/span/div/div[2]/div[1]/div[1]/div[1]/input"
facility_item = "/html/body/div/div/div[10]/div/div[2]/div"
# 利用日時
date_of_use = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[2]/dd/span[1]/div[1]/div/div[1]/div[1]/input"
time_of_use = ["/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[2]/dd/span[2]/div/div/div[1]/fieldset/div[1]/div/div/div[1]/div/label","/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[2]/dd/span[2]/div/div/div[1]/fieldset/div[1]/div/div/div[1]/div/label","/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[2]/dd/span[2]/div/div/div[1]/fieldset/div[2]/div/div/div[1]/div/label","/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[2]/dd/span[2]/div/div/div[1]/fieldset/div[3]/div/div/div[1]/div/label"]
# 検索
facility_search_button = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/div/div[1]/button"

# 空き情報
aki_joukyou_button = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div[3]/div[1]/div/div[2]/div[3]/span/a/span/span/span[2]"
# チュートリアルスキップ
tutorial_skip_button = "/html/body/div/div/div[6]/div/div[2]/div[3]/div[3]/button/span"
# 時間選択枠全体
time_slot_class = "AvailabilityFrameSet_frame_content"
# 時間選択枠　抽選可能枠
time_slot_class_l = "is-lot"
# 確認
time_check_button = "/html/body/div/div/div[3]/div/main/div[2]/div[2]/div[1]/div/div/button/span"
# 抽選申込へ
to_application_button = "/html/body/div/div/div[9]/div/div[2]/button[1]/span"
#　利用人数
num_of_people_form = "/html/body/div/div/div[3]/div/main/div[1]/div[4]/div/div/form/div/div/div/div/dl[2]/dd/span/div/div/div[1]/div/input"
#　体育館利用人数
num_of_people = "24"
# 確認
last_check = "/html/body/div/div/div[3]/div/main/div[2]/div/div[1]/div/button/span"
# 注意事項を確認しました
last_check_box = "/html/body/div/div/div[3]/div/main/div[1]/form/div[4]/div[2]/div[3]/span/div/div/div[1]/div/label"
# エラー
last_error_text = "/html/body/div/div/div[3]/div/main/div[1]/div[4]/div[2]/ul/li/button/span"
# 申込確定
application_ok = "/html/body/div/div/div[3]/div/main/div[2]/div/div[1]/div/button"
application_ok2 = "/html/body/div/div/div[3]/div/main/div[1]/div[5]/div/div[1]/div/button"
# ホーム(左上)
back_menu_button = "/html/body/div/div/div[3]/div/nav/ul/li[1]/a/span"
# 施設一覧・検索(左上)
back_facility_view = "/html/body/div/div/div[3]/div/nav/ul/li[3]/a"
# メニューバーボタン
main_menu = "/html/body/div/div/div[2]/header/div/div[2]/button[2]/span/span/div/svg/text"
main_menu2= "/html/body/div/div/div[2]/header/div/div[2]/button/span/span/span"
# ログアウトボタン
logout_button = "/html/body/div/div/div[3]/header/div/div[3]/div[1]/nav/div[2]/div/div[2]/a[2]/div[2]/div"
# logout_button_s = "/html/body/div/div/div[3]/header/div/div[3]/div[1]/nav/div[2]/div/div[2]/a/div[2]/div"
logout_button_s = "/html/body/div/div/div[3]/header/div/div[3]/div[1]/nav/div[2]/div/div[2]/a[2]/div[2]/div"

# データ
start_time_list = [8,11,14,17,24]
