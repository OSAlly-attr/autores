import time
import csv
import requests
import unicodedata
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime

# csvを読み込む関数
def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        data1_data2 = [row for row in reader]
        return data1_data2

# ChromeWebdriverを起動する関数
def chrome():
    ChromeOptions = Options()
    ChromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)
    auto_reservation(driver, pw_range[0], pw_range[1])
    return

# LINEに送信する関数
def send_line(text):
    f = open('line_key.txt', 'r')
    data = f.read()
    f.close()
    TOKEN =  data
    api_url = 'https://notify-api.line.me/api/notify'
    send_text = text
    TOKEN_dic = {'Authorization': 'Bearer ' + TOKEN}
    send_dic = {'message': send_text}
    requests.post(api_url, headers=TOKEN_dic, data=send_dic)

# def send_line(text):
#     return

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

# xpathのリストで，押せる方を押す関数
def xpath_click2(driver, xpath_list):
    if no_error[0]:
        for i in range(trymax):
            try:
                for k in range(len(xpath_list)):
                    if xpath_exist_check(driver, xpath_list[k], 2):
                        driver.find_element(By.XPATH, xpath_list[k]).click()
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

# xpath_listのどちらかの要素を取得する関数
def xpath_get2(driver, xpath_list):
    if no_error[0]:
        for i in range(trymax):
            try:
                for k in range(len(xpath_list)):
                    if xpath_exist_check(driver, xpath_list[k], 2):
                        return driver.find_element(By.XPATH, xpath_list[k]).text
            except:
                time.sleep(dtry)
        no_error[0] = False

# 時間帯指定する関数　(アカウントごとに半面AB交互、全面はとらない)
def select_time(driver, x, j):
    for i in range(trymax):
        elements = driver.find_elements(By.CLASS_NAME, time_slot_class_l)
        if len(elements)!=0:
            break
        else:
            #モーダルスキップ
            if len(driver.find_elements(By.XPATH, tutorial_skip_button))!=0:
                xpath_click(driver, tutorial_skip_button)
                continue
            else:
                time.sleep(dtry)
    elements_list = []
    for elm in elements:
        elm_text = elm.get_attribute('title')
        for i in range(len(elm_text)):
            if elm_text[i]=="時":
                elm_text = int(elm_text[0:i])
                break
        if start_time_list[int(j[2])] <= elm_text and elm_text < start_time_list[int(j[2])+1]:
            elements_list.append(elm)
    if len(elements_list) == 3:
        elements_list[1+x%2].click()
    elif len(elements_list) == 2:
        elements_list[x%2].click()
    elif len(elements_list) == 1:
        elements_list[0].click()

# 親アカウントの抽選申込をチェックする関数
def parent_check(driver):
    if check_bl[0] == False:
        return False
    time.sleep(1)
    xpath_click(driver, all_status)
    time.sleep(1)
    xpath_click(driver, num_view)
    time.sleep(1)
    xpath_click(driver, view_forty)
    time.sleep(1)
    tmp = []
    for i in range(1,40):
        count = 0
        if '抽選待ち' in xpath_get(driver, view_item_attr1 + str(i) + view_item_attr2):
            top_gym = xpath_get(driver, view_item_gym1 + str(i) + view_item_gym2)
            top_date = xpath_get(driver, view_item_date1 + str(i) + view_item_date2)
            top_time = xpath_get(driver, view_item_time1 + str(i) + view_item_time2)
            top_time = int(top_time[:top_time.find(':')])
            if top_time < 10:
                top_time_zone = 0
            elif top_time ==  11:
                top_time_zone = 1
            elif top_time == 14:
                top_time_zone = 2
            elif top_time > 16:
                top_time_zone = 3
            top_item = [top_gym[:top_gym.find(' /')], top_date[top_date.rfind('/')+1:top_date.find('(')], str(top_time_zone)]
            tmp.append(top_item)
            count += 1
            if count == 15:
                break
    
    tmp.reverse()
    tmp = sorted(tmp)
    # ファイル出力
    with open('./items.csv', 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(tmp)
    xpath_click(driver, to_home_from_status)
    xpath_click(driver, main_menu2)
    xpath_click(driver, logout_button)
    return True

# 途中から始める項目をチェックする関数
def start_check(driver, gym_day_time):
    try:
        if '抽選待ち' in xpath_get(driver, status_top_attr):
            top_gym = xpath_get(driver, status_top_gym)
            top_date = xpath_get(driver, status_top_date)
            top_time = xpath_get(driver, status_top_time)
            top_time = int(top_time[:top_time.find(':')])
            if top_time < 10:
                top_time_zone = 0
            elif top_time ==  11:
                top_time_zone = 1
            elif top_time == 14:
                top_time_zone = 2
            elif top_time > 16:
                top_time_zone = 3
            top_item = [top_gym[:top_gym.find(' /')], top_date[top_date.rfind('/')+1:top_date.find('(')], str(top_time_zone)]
            for j in range(len(gym_day_time)):
                if gym_day_time[j] == top_item:
                    idx = j
            if idx == len(gym_day_time)-1:
                print("次のアカウントから始めます")
            else:
                print(str(idx+2) + "枠目から始めます")
            return idx
        return -1
    except:
        return -1

# main関数
def auto_reservation(driver, pw_range_top, pw_range_bottom):
    # アカウントパスワードリストを読み込み
    account_password = read_csv(account_password_path[0])
    # harp札幌 ページ読み込み
    time.sleep(0.2)
    driver.get('https://yoyaku.harp.lg.jp/sapporo/')
    # 施設予約へ
    for x, i in enumerate(account_password, 1):
        #　 アカウントの範囲
        if(pw_range_top> x or x > pw_range_bottom):
            if check_bl[0]==False or x!=1:
                continue
        # 進行状況
        if check_bl[0] and x==1:
            print('現在' + str(x) + '番目のアカウントを参照中 (ID : ' + str(i[0].zfill(8)) + ')')
            # send_line('現在' + str(x) + '番目のアカウントを参照中 (ID : ' + str(i[0].zfill(8)) + ')')
        else:
            print('現在' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')')
            # send_line('現在' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')')
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
            send_line("\n"+str(x)+"番目のアカウント(ID: "+ str(i[0].zfill(8)) +")が期限切れです。")
            continue
        # 親アカウントの抽選申込をチェック
        if check_bl[0] and x == 1:
            if parent_check(driver):
                continue
        # 抽選申込ファイルitems.csvから項目を読み込み
        with open('./items.csv') as f:
            reader = csv.reader(f)
            gym_day_time = [row for row in reader]
        # idx：何枠目まで抽選ができているか
        idx = start_check(driver, gym_day_time)
        # 1項目目のフラグ False
        f_flag = False
        
        # 抽選申込
        for k, j in enumerate(gym_day_time):  # j[0] gym  j[1] day  j[2] time
            if k <= idx:
                continue
            if f_flag:
                # 施設がデフォルトと同じ場合は入力をスキップ
                if j[0] != xpath_get(driver, facility_name_default):                      
                    # 施設バツ
                    xpath_click(driver, gym_clear)
                    # 施設
                    xpath_send_keys(driver, facility_name_text_field_q, j[0])
                    while(1):
                        if xpath_get(driver, facility_item_q) == j[0]:
                            xpath_click(driver, facility_item_q)
                            break
                        else:
                            time.sleep(0.5)
                            xpath_click(driver, gym_clear)
                            xpath_send_keys(driver, facility_name_text_field_q, j[0])
                    xpath_click(driver, "/html/body/div/div/div[3]/div/main/div[1]/h1")
                # 利用日バツ
                xpath_click(driver, date_of_use_clear)
                # 利用日
                xpath_send_keys(driver, date_of_use_q, year_month[0]+year_month[1]+j[1].zfill(2))
                # 空き施設検索
                xpath_click(driver, facility_search_button_q)
                xpath_click(driver, facility_search_button_q)
            else:
                # 目的
                xpath_send_keys(driver, purpose_of_use, sports[0])
                xpath_click2(driver, purpose_of_item)
                xpath_click(driver, "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[1]/h2")
                while(1):
                    if xpath_exist_check(driver, purpose_pannel, 15):
                        break
                    else:
                        xpath_click2(driver, purpose_of_item)
                        xpath_click(driver, "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[1]/h2")
                
                # 施設
                xpath_send_keys(driver, facility_name_text_field, j[0])
                while(1):
                    if xpath_get2(driver, facility_item) == j[0]:
                        xpath_click2(driver, facility_item)
                        xpath_click(driver,"/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[1]/h2")
                        break
                    else:
                        time.sleep(0.5)
                        xpath_click(driver, facility_item_clear)
                        xpath_send_keys(driver, facility_name_text_field, j[0])
                # 利用日
                xpath_send_keys(driver, date_of_use, year_month[0]+year_month[1]+j[1].zfill(2))
                # 空き施設検索
                xpath_click(driver, facility_search_button)
                xpath_click(driver, facility_search_button)
            #空き状況
            xpath_click(driver, aki_joukyou_button)
            #時間帯指定
            select_time(driver, x, j)
            # 確認
            xpath_click(driver, time_check_button)
            # 抽選申込へ
            xpath_click(driver, to_application_button)
            # 利用人数
            xpath_send_keys(driver, num_of_people_form, num_of_people)
            # 確認
            xpath_click(driver, last_check)
            # 注意事項を確認しました&申込確定
            time.sleep(0.5)
            xpath_click(driver, application_ok)
            time.sleep(0.5)
            xpath_click(driver, last_error_text)
            xpath_click(driver, last_check_box)
            xpath_click(driver, application_ok2)
            # 施設一覧・検索へ
            xpath_click(driver, back_facility_view)
            f_flag = True
            # エラーが出たら通知して終了
            if no_error[0] == False:
                send_line('\nエラーが発生しました。\n' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
                print('エラーが発生しました。' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
                return
        # ログアウト
        xpath_click(driver, main_menu2)
        time.sleep(0.5)
        xpath_click(driver, logout_button)
        # エラーが出たら通知して終了
        if no_error[0] == False:
            send_line('\nエラーが発生しました。\n' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
            print('エラーが発生しました。' + str(x) + '番目のアカウント (ID : ' + str(i[0].zfill(8)) + ')で発生。')
            return
    #終了と通知
    driver.quit()
    send_line("\n"+str(pw_range_top)+" ~ "+str(pw_range_bottom)+"番目のアカウント(ID : " + str(account_password[pw_range_top-1][0]) + " ~ " + str(account_password[pw_range_bottom-1][0]) + ")の抽選申込が完了しました。")
    print(str(pw_range_top)+" ~ "+str(pw_range_bottom)+"番目のアカウント(ID : " + str(account_password[pw_range_top-1][0]) + " ~ " + str(account_password[pw_range_bottom-1][0]) + ")の抽選申込が完了しました。")


# 利用年・月・体育館・日付・時間帯
today = datetime.date.today()
delta = datetime.timedelta(days=15)
day = today+delta
year_month = [str(day.year), str(day.month).zfill(2)]
gym_day_time = [[0 for i in range(3)] for j in range(15)]
for i in range(15):
    gym_day_time[i] = ["","",""] # 初期化
# 自動化するアカウントの範囲
pw_range = ["",""]
# 途中からはじめるチェックbool
check_bl = []
# try繰り返す回数
trymax = 80
# try間隔
dtry = 0.1
# エラーフラグ
no_error = [True]
# 利用目的（競技）
sports = [""]
# アカウントのcsvリスト
csv_list = []
# アカウントリストのパス
account_password_path = ['']


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
# x件ずつ
view_twenty = "/html/body/div/div/div[8]/div/div[2]/div/div"
view_forty = "/html/body/div/div/div[8]/div/div[3]/div/div"
# 項目1
view_item_attr1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_attr2 = "]/div[1]/div[1]/span"
view_item_gym1 =  "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_gym2 = "]/div[1]/div[2]/div[2]/div[1]/a"
view_item_date1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_date2 = "]/div[1]/div[2]/div[2]/div[2]/time[1]"
view_item_time1 = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div["
view_item_time2 = "]/div[1]/div[2]/div[2]/div[2]/span[2]"
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
facility_item_clear = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[1]/dd/span[3]/span/div/div[2]/div[1]/div[1]/div[1]/span/span/button"
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
purpose_of_item = []
purpose_of_item.append("/html/body/div/div/div[12]/div/div[4]/div")
purpose_of_item.append("/html/body/div/div/div[11]/div/div[4]/div")
purpose_of_item.append("/html/body/div/div/div[10]/div/div[4]/div")
purpose_of_item.append("/html/body/div/div/div[9]/div/div[4]/div")

# 項目のパネル
purpose_pannel = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[1]/dd/span[1]/span/div/div[2]/div[1]/div[1]/div[1]/span/span/span"

# 施設
facility_name_text_field = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[2]/form/dl[1]/dd/span[3]/span/div/div[2]/div[1]/div[1]/div[1]/input"
facility_item = []
facility_item.append("/html/body/div/div/div[13]/div/div[2]/div")
facility_item.append("/html/body/div/div/div[12]/div/div[2]/div")
facility_item.append("/html/body/div/div/div[11]/div/div[2]/div")
facility_item.append("/html/body/div/div/div[10]/div/div[2]/div")

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
logout_button_s = "/html/body/div/div/div[3]/header/div/div[3]/div[1]/nav/div[2]/div/div[2]/a/div[2]/div"

# データ
start_time_list = [8,11,14,17,24]

# バージョン　
ver = "2.1.4"