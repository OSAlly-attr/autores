import tkinter as tk
import tkinter.ttk as ttk
import glob
from tkinter import messagebox
from cancelfunc import *
from func import ver

# 抽選申込ボタンを押すと実行される関数
def click_cancel():
    if combo.get() == "":
        messagebox.showinfo("警告", "利用種目を入力してください")
        return
    else:
        sport.append(combo.get())
    
    if combo1.get() == "":
        messagebox.showinfo("警告", "アカウントの情報を入力してください")
        return
    
    if input_cancel[0].get() == "":
        messagebox.showinfo("警告", "学校名を入力してください")
        return
    else:
        school.append(input_cancel[0].get())
    
    # print(input_cancel[0].get())
    if input_cancel[1].get() == "":
        account.append(read_csv("./account/" + combo1.get())[0][0])
        password.append(read_csv("./account/" + combo1.get())[0][1])
    else:
        flg = False
        for file in option1:
            # print(file)
            for li in read_csv("./account/" + file):
                # print(li)
                if li[0] == input_cancel[1].get():
                    account.append(input_cancel[1].get())
                    password.append(li[1])
                    flg = True
                if flg:
                    break
            if flg:
                break
    
    if input_cancel[2].get() == "":
        messagebox.showinfo("警告", "日付を入力してください")
        return
    # elif len(input_cancel[2].get()):
    #     messagebox.showinfo("警告", "日付を正しく入力してください")
    #     return
    else:
        date.append(input_cancel[2].get())
    
    if combo2.get() == "":
        messagebox.showinfo("警告", "時間帯を入力してください")
        return
    else:
        jikan.append(combo2.get())
    
    
    
    # if combo1.get() == "" and input_cancel[1].get() =="":
    #     messagebox.showinfo("警告", "アカウントの情報を入力してください")
    #     return
    # elif input_cancel[1].get() == "":
    #     account_password_path[0] = "./account/" + combo1.get()
    #     account_password = read_csv(account_password_path[0])
    #     account.append(account_password[0][0])
    #     password.append(account_password[0][1])
    # else:
    #     flg = False
    #     for file in option1:
    #         for li in file:
    #             if li[0] == input_cancel[1].get():
    #                 account.append(input_cancel[1].get())
    #                 password.append(li[1])
    #                 flg = True
    #             if flg:
    #                 break
    #         if flg:
    #             break
    # if input_cancel[0].get() == "":
    #     messagebox.showinfo("警告", "学校名を入力してください")
    #     return
    # else:
    #     school.append(input_cancel[0].get())
    # if combo2.get() == "":
    #     messagebox.showinfo("警告", "時間帯を入力してください")
    #     return
    # else:
    #     time_area.append(combo2.get())
    # # account_password = read_csv(account_password_path[0])
        
    # if input_cancel[1].get() != "" or :
    #     messagebox.showinfo("警告", "")
    # if combo.get() == "":
    #     messagebox.showinfo("警告", "利用種目を入力してください")
    #     return
    # else:
    #     sports[0] = combo.get()
    chrome()


# accountフォルダ内のcsvファイル名を読み込む関数
def take_csv():
    files = glob.glob("./account/*.csv")
    for file in files:
        csv_list.append(file)
    csv_list.sort()

# パスの余分な部分をカットする関数
def name_csv():
    for i in range(len(csv_list)):
        option1.append(csv_list[i][10:])
    option1.sort()

# Tkinterインスタンスの生成
root = tk.Tk()
root.title("自動抽選システム キャンセル待ち")
root.geometry("400x430")

label_header1 = tk.Label(root, text=u'利用種目', font=("Arial", "12", "bold"))
label_header1.place(x=20, y=30)
option = ["バレーボール", "バドミントン", "卓球"]
variable = tk.StringVar()
combo = ttk.Combobox(root, values=option, textvariable=variable, width=15, font=("Arial", "12", "normal"))
combo.place(x=20, y=60)
combo.insert(0,option[0])

label_header2 = tk.Label(root, text=u'アカウントリスト(csv)', font=("Arial", "12", "bold"))
label_header2.place(x=190, y=30)
take_csv()
option1 = []
name_csv()
variable1 = tk.StringVar()
combo1 = ttk.Combobox(root, values=option1, textvariable=variable1, width=15, font=("Arial", "12", "normal"))
combo1.place(x=190, y=60)
combo1.insert(0,option1[0])

input_cancel = [0 for i in range(3)] 
label_header5 = tk.Label(root, text=u'学校名', font=("Arial", "12", "bold"))
label_header5.place(x=20, y=110) 
input_cancel[0] = tk.Entry(width=20, font=("Arial", "12", "normal"))
input_cancel[0].place(x=20, y=140)
label_header7 = tk.Label(root, text=u'アカウントID', font=("Arial", "12", "bold"))
label_header7.place(x=190, y=110)
input_cancel[1] = tk.Entry(width=20, font=("Arial", "12", "normal"))
input_cancel[1].place(x=190, y=140)
label_header1 = tk.Label(root, text=u'無入力のときはリストの先頭を参照する', font=("Arial", "9", "bold"))
label_header1.place(x=190, y=165)

label_header8 = tk.Label(root, text=u'日付(yyyymmdd)', font=("Arial", "12", "bold"))
label_header8.place(x=20, y=220) 
input_cancel[2] = tk.Entry(width=20, font=("Arial", "12", "normal"))
input_cancel[2].place(x=20, y=250)
label_header6 = tk.Label(root, text=u'時間帯', font=("Arial", "12", "bold"))
label_header6.place(x=190, y=220) 
option_time = ['午前(09:00~)', '昼  (11:00~)', '午後(14:30~)', '夜  (17:45or18:15~)']
variable1 = tk.StringVar()
combo2 = ttk.Combobox(root, values=option_time, textvariable=variable1, width=18, font=("Arial", "12", "normal"))
combo2.place(x=190, y=250)
combo2.insert(0,option_time[3])



button_3 = tk.Button(text="キャンセル待ち開始", font=("Arial", "12", "bold"), command=click_cancel)
button_3.place(x=190, y=320)

label_header3 = tk.Label(root, text=ver, font=("Arial", "12", "bold"))
label_header3.place(x=320, y=384)
root.mainloop()
