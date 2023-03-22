import time                            # スリープを使うために必要
import csv
import unicodedata
from tkinter import messagebox
# Webブラウザを自動操作する（python -m pip install selenium)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime


# csv読み込み関数
def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        data1_data2 = [row for row in reader]
        return data1_data2

# ChromeWebdriver起動
def chrome():
    ChromeOptions = Options()
    ChromeOptions.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(
    ), options=ChromeOptions)            # Chromeを準備
    return main(driver)

# xpathでクリックする関数
def xpath_click(driver, xpath):
    time.sleep(0.2)
    driver.find_element(By.XPATH, xpath).click()
    
def hidden_xpath_click(driver, xpath):
    for i in range (5):
        time.sleep(0.5)
        elements = driver.find_elements(By.XPATH, xpath)
        if len(elements) != 0:
            driver.execute_script("arguments[0] click();", elements[0]) 
            break
        elif i == 4:
            sys.exit('(} no such element'.format(xpath))

# xpathで入力する関数
def xpath_send_keys(driver, xpath, keys):
    time.sleep(0.2)
    tmp = driver.find_element(By.XPATH, xpath)
    tmp.clear()
    tmp.send_keys(keys)

# idで入力する関数
def id_send_keys(driver, id, keys):
    time.sleep(0.2)
    tmp = driver.find_element(By.ID,id)
    tmp.clear()
    tmp.send_keys(keys)

# xpathで要素を取得する関数
def xpath_get(driver, xpath):
    return driver.find_element(By.XPATH, xpath).text

# xpathでページ遷移ができるまで待つ関数(要素が存在するかチェックする関数)
def xpath_exist_check(driver, xpath):
    for i in range(5):
        if len(driver.find_elements(By.XPATH, xpath))!=0:
            return True
        elif i==4:
            return False
        time.sleep(2)

# xpathで要素が存在するかチェックする関数
def xpath_exist_check1(driver, xpath):
    for i in range(5):
        time.sleep(0.5)
        if len(driver.find_elements(By.XPATH, xpath))!=0:
            return True
        elif i==4:
            return False

# 違反文字をチェックする関数
def check_text(text):
    for c in text:
        letter = unicodedata.east_asian_width(c)
        if letter != 'W':
            return False
    return True

# 時間帯指定する関数　(アカウントごとに半面AB交互、全面はとらない)
def select_time(driver, x, j):
    elements = driver.find_elements(By.CLASS_NAME, time_slot_class_l)
    elements_list = []
    for elm in elements:
        elm_text = elm.get_attribute('title')
        for i in range(len(elm_text)):
            if elm_text[i]=="時":
                elm_text = int(elm_text[0:i])
                break
        if start_time_list[int(j[2])] <= elm_text and elm_text < start_time_list[int(j[2])+1]:
            elements_list.append(elm)
    time.sleep(0.5)
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
    xpath_click(driver, view_twenty)
    time.sleep(1)
    tmp = []
    for i in range(1,16):
        if '落選' in xpath_get(driver, view_item_attr1 + str(i) + view_item_attr2):
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
    
    tmp.reverse()
    # print(tmp)
    # ファイル出力
    with open('./items.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(tmp)
    xpath_click(driver, to_home_from_status)
    time.sleep(2)
    if xpath_exist_check(driver, main_menu2):
        xpath_click(driver, main_menu2)
    time.sleep(1)
    xpath_click(driver, logout_button)
    return True


# 途中から始める項目をチェックする関数
def start_check(driver):
    if '本予約' in xpath_get(driver, status_top_attr):
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
        print(str(idx+2) + "番目から始めます")
        return idx
    return -1

# 空きがあるかどうかを見つけたらクリック、なければ更新を繰り返す関数
def search_take(driver):
    while True:
        for i in range(1,20):
            attr = driver.find_elements(By.XPATH, th_front+str(i)+th_rear)
            if len(attr)==0:
                continue
            if '半面' not in attr[0].get_attribute('abbr') and '体育館' not in attr[0].get_attribute('abbr'):
                continue
            for j in range(1,31):
                date = driver.find_elements(By.XPATH, th_front+str(i)+date_middle+str(j)+date_rear)
                if len(date)==0:
                    continue
                day_num = date[0].get_attribute('title')
                day_num = day_num[day_num.find('月')+1:]
                day_num = day_num[:day_num.find('日')]
                print(day_num)
                if day_num in input_date:
                    xpath_click(driver, th_front+str(i)+date_middle+str(j)+date_rear)
                
            print()
        time.sleep(1)
        driver.refresh()


# main関数
def main(driver):
    # harp札幌 ページ読み込み
    time.sleep(0.2)
    driver.get('https://yoyaku.harp.lg.jp/sapporo/')  # 予約サイトを開く
    # 施設予約ログイン
    time.sleep(1.5)
    if xpath_exist_check(driver, facility_reservation_login_button):
        xpath_click(driver, facility_reservation_login_button)
    # 親アカウントのIDとパスワードを入力、ログイン
    time.sleep(1)
    if xpath_exist_check(driver, login_button):
        id_send_keys(driver, registered_number_text_field, account_password[0][0].zfill(8))
        id_send_keys(driver, password_text_field, account_password[0][1])
    time.sleep(1)
    xpath_click(driver, login_button)
    if xpath_exist_check(driver, facility_search_button) == False:
        for i in range(10):
            time.sleep(2)
            xpath_click(driver, login_button)
            xpath_click(driver, login_button)
            if xpath_exist_check(driver, facility_search_button):
                break
    
    # 目的
    time.sleep(1)
    if xpath_exist_check(driver, facility_search_button):
        xpath_send_keys(driver, purpose_of_use, "バレーボール")
    time.sleep(2)
    xpath_click(driver, purpose_of_item)

    # 施設名を入力
    for i, gym in enumerate(gym_list):
        xpath_send_keys(driver, facility_name_text_field, gym)
        time.sleep(2)
        xpath_click(driver, facility_item)
        if gym == gym_list[-1]:
            break
        for j in range(len(gym)):
            xpath_send_keys(driver, facility_name_text_field, Keys.BACK_SPACE)         

    # 一度施設検索をクリックしてプルダウンを閉じる
    time.sleep(0.5)
    xpath_click(driver, text_shisetsukensaku)
    # 空き施設検索
    time.sleep(0.5)
    xpath_click(driver, facility_search_button)

    # 複数室場の空きを一括で確認
    time.sleep(1)
    xpath_click(driver, aki_fukusu_button)

    #モーダルスキップ
    time.sleep(1)
    if xpath_exist_check(driver, tutorial_skip_button):
        xpath_click(driver, tutorial_skip_button)
    
    # 見つけるまで更新
    time.sleep(1)
    search_take(driver)

    time.sleep(1)
    print(len(driver.find_elements(By.XPATH, "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/td[13]/span/a")))
    print(driver.find_elements(By.XPATH, "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/td[13]/span/a")[0].get_attribute('title'))

    time.sleep(10)
    # 終了
    # driver.quit()


# 利用年・月・体育館・日付・時間帯
today = datetime.date.today()
delta = datetime.timedelta(days=15)
day = today+delta
year_month = [str(day.year), str(day.month).zfill(2)]
gym_day_time = [[0 for i in range(3)] for j in range(15)]
for i in range(15):
    gym_day_time[i] = ["","",""] # 初期化
# 入力の日付リスト
input_date = []
# 途中からはじめるチェックbool
check_bl = []


account_password_path = "./account_password.csv"
account_password_path2 = "./account_password2.csv"
account_password_path_main = "./account_password_main.csv"
account_password = read_csv(account_password_path_main)
# account_password = read_csv(account_password_path)
# account_password2 = read_csv(account_password_path2)
# account_password.extend(account_password2)
gym_date_path = r".\gym_date.csv"

# ログイン
facility_reservation_login_button = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[2]/div[1]/span[1]/a"
#　利用者番号
registered_number_text_field = "input-21"
# パスワード
password_text_field = "input-25"
# ログイン
login_button = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div/div[1]/div/button"
# 利用事項同意
agree_check_box = "/html/body/div/div/div[3]/div/main/div[1]/form/div/span/div/div/div[1]/div/label"
# agree_button = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div/div[1]/div/button"
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
# ホームへ
to_home_from_status = "/html/body/div/div/div[3]/div/nav/ul/li[1]/a/span"

# 申し込み状況top属性
status_top_attr = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span"
status_top_gym = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/a"
status_top_date = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/time[1]"
status_top_time = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/span[2]"

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
# 施設検索h2
text_shisetsukensaku = "/html/body/div/div/div[3]/div/main/div[1]/div[1]/div[1]/div[1]/div[1]/h2"
# 複数室場の空きを一括で確認
aki_fukusu_button = "/html/body/div/div/div[3]/div/main/div[1]/div[2]/div[2]/div[1]/div[3]/a"
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

# メニューバーボタン
main_menu = "/html/body/div/div/div[2]/header/div/div[2]/button[2]/span/span/div/svg/text"
main_menu2= "/html/body/div/div/div[2]/header/div/div[2]/button/span/span/span"

# ログアウトボタン
logout_button = "/html/body/div/div/div[3]/header/div/div[3]/div[1]/nav/div[2]/div/div[2]/a[2]/div[2]/div"


# データ
start_time_list = [8,11,14,17,24]
# gym_list = ['和光小学校', '東園小学校', '北園小学校', '北陽中学校', '北九条小学校', '日新小学校']
gym_list = ['和光小学校', '東園小学校']


# キャン待ち画面th前半
th_front = "/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr["
# キャン待ち画面th前半
th_rear = "]/th"
# 日付中間・後半
date_middle = "]/td["
date_rear = "]/span/a"
# 日新小学校3/7全面
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/td[4]/span"
# 日新小学校3/11全面
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/td[8]/span"
# 日新小学校3/7半面A
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[4]/td[4]/span"
# 日新小学校3/7半面B
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[5]/td[4]/span"
# 和光小学校3/7全面
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[8]/td[4]/span"
# 和光小学校3/11全面
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[8]/td[8]/span"

"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/td[13]/span/a/time"
"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/td[4]/span/a"
# 日新小学校3/7半面A

# 日新小学校3/7半面B

"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[3]/th/a/span"

"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[4]/th/a/span"

"/html/body/div/div/div[3]/div/main/div[1]/div[3]/div[5]/div[2]/table/tbody/tr[8]/th/a/span"