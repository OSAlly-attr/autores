import tkinter as tk
import tkinter.ttk as ttk
import glob
from tkinter import messagebox
from func import *

# 抽選申込ボタンを押すと実行される関数
def click_botton():
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
    if combo.get() == "":
        messagebox.showinfo("警告", "利用種目を入力してください")
        return
    else:
        sports[0] = combo.get()
    
    check_bl.append(bln.get())
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
root.title("自動抽選システム")
root.geometry("400x300")

option = ["バレーボール", "バドミントン"]
variable = tk.StringVar()
combo = ttk.Combobox(root, values=option, textvariable=variable, width=15, font=("Arial", "12", "normal"))
combo.place(x=20, y=122)
combo.insert(0,option[0])

take_csv()
option1 = []
name_csv()
variable1 = tk.StringVar()
combo1 = ttk.Combobox(root, values=option1, textvariable=variable1, width=15, font=("Arial", "12", "normal"))
combo1.place(x=190, y=122)
combo1.insert(0,option1[0])

label_header = tk.Label(root, text=u'アカウント範囲 (無入力: 2番目・最後)', font=("Arial", "12", "bold"))
label_header.place(x=20, y=30)
input_range = [0 for i in range(2)]
input_range[0] = tk.Entry(width=5, font=("Arial", "12", "normal"))
input_range[0].place(x=20, y=58)
input_range[1] = tk.Entry(width=5, font=("Arial", "12", "normal"))
input_range[1].place(x=75, y=58)
label_header1 = tk.Label(root, text=u'利用種目', font=("Arial", "12", "bold"))
label_header1.place(x=20, y=94)
label_header2 = tk.Label(root, text=u'アカウントリスト(csv)', font=("Arial", "12", "bold"))
label_header2.place(x=190, y=94)
label_header3 = tk.Label(root, text=u'ver 2.1.2', font=("Arial", "12", "bold"))
label_header3.place(x=320, y=254)
button = tk.Button(text="抽選申込開始", font=("Arial", "12", "bold"), command=click_botton)
button.place(x=20, y=154)
bln = tk.BooleanVar()
chk = tk.Checkbutton(root, text='親アカウントを参照する', font=("Arial", "12", "bold"), variable=bln)
chk.place(x=130, y=58)
root.mainloop()
