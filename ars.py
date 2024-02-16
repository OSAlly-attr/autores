import tkinter as tk
import tkinter.ttk as ttk
import glob
from tkinter import messagebox
from funcinfo import *
from func import *
# from cancelfunc import *


# 抽選申込ボタンを押すと実行される関数
def click_reservation():
    if combo1.get() == "":
        messagebox.showinfo("警告", "アカウントリスト(csv)を入力してください")
        return
    else:
        account_password_path[0] = "./account/" + combo1.get()
    account_password = read_csv(account_password_path[0])
    if input_range[0].get() == "":
        pw_range[0] = 2
    else:
        if int(input_range[0].get())>0 and int(input_range[0].get())<=len(account_password):
            pw_range[0] = int(input_range[0].get())
        else:
            messagebox.showinfo("警告", "数値入力が正しくありません")
            return 
    if input_range[1].get() == "":
        pw_range[1] = len(account_password)
    else:
        if int(input_range[1].get())>0 and int(input_range[1].get())<=len(account_password):     
            pw_range[1] = int(input_range[1].get())
        else:
            messagebox.showinfo("警告", "数値入力が正しくありません")
            return 
    check_bl.append(bln.get())
    chrome_reservation()

def click_result():
    if combo1.get() == "":
        messagebox.showinfo("警告", "アカウントリスト(csv)を入力してください")
        return
    else:
        account_password_path[0] = "./account/" + combo1.get()
        # res_acc[0] = combo1.get()
    account_password = read_csv(account_password_path[0])
    if input_range[0].get() != "":
        messagebox.showinfo("警告", "アカウントの範囲に数値を入力しないでください")
        return
    if input_range[1].get() != "":
        messagebox.showinfo("警告", "アカウントの範囲に数値を入力しないでください")
        return 
    chrome_result()

# accountフォルダ内のcsvファイル名を読み込む関数
def take_csv():
    files = glob.glob("./account/*.csv")
    for file in files:
        option1.append(file[10:])
    option1.sort()


# Tkinterインスタンスの生成
root = tk.Tk()
root.title("自動抽選システム")
root.geometry("400x300")

option1 = []
take_csv()
variable1 = tk.StringVar()
combo1 = ttk.Combobox(root, values=option1, textvariable=variable1, width=15, font=("Arial", "12", "normal"))
combo1.place(x=20, y=152)
combo1.insert(0,option1[0])

label_header = tk.Label(root, text=u'アカウント範囲', font=("Arial", "12", "bold"))
label_header.place(x=20, y=30)
input_range = [0 for i in range(2)]
input_range[0] = tk.Entry(width=5, font=("Arial", "12", "normal"))
input_range[0].place(x=20, y=58)
input_range[1] = tk.Entry(width=5, font=("Arial", "12", "normal"))
input_range[1].place(x=75, y=58)
label_header1 = tk.Label(root, text=u'無入力：抽選申込は2番目から最後  抽選確認は先頭から最後', font=("Arial", "9", "bold"))
label_header1.place(x=20, y=88)
label_header2 = tk.Label(root, text=u'アカウントリスト(csv)', font=("Arial", "12", "bold"))
label_header2.place(x=20, y=124)
button = tk.Button(text="抽選申込開始", font=("Arial", "12", "bold"), command=click_reservation)
button.place(x=190, y=152)
button_2 = tk.Button(text="抽選確認開始", font=("Arial", "12", "bold"), command=click_result)
button_2.place(x=190, y=190)
bln = tk.BooleanVar()
chk = tk.Checkbutton(root, text='親アカウントを参照する', font=("Arial", "12", "bold"), variable=bln)
chk.place(x=130, y=58)

label_header3 = tk.Label(root, text=ver, font=("Arial", "12", "bold"))
label_header3.place(x=320, y=264)

root.mainloop()
