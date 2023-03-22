# Tkinterライブラリをインポートする
import tkinter as tk
from tkinter import messagebox
from func_varc import *


def click_botton():
    bool1 = True
    # count = 0
    # if input_range[0].get() == "":
    #     pw_range.append(2)
    # else:
    #     pw_range.append(int(input_range[0].get()))
    # if input_range[1].get() == "":
    #     pw_range.append(len(account_password))
    # else:
    #     pw_range.append(int(input_range[1].get()))
    # for i in range(15):
    #     tmp_list = []
    #     for j in range(3):
    #         # tmp = input_field[i][j].get()
    #         tmp = input_field[i][j]
    #         tmp_list.append(tmp)
    #         if tmp == "":
    #             count += 1
    #         elif j == 0 and check_text(tmp) == False:
    #             messagebox.showinfo("警告", str(i+1) + "番目の体育館名が正しくありません。")
    #             bool1 = False
    #         elif j == 1 and (int(tmp) < 1 or 31 < int(tmp) or ((int(tmp) == 31) and (year_month[1] in ['2', '4', '6', '9', '11']))):
    #             messagebox.showinfo("警告", str(i+1) + "番目の日付が正しくありません。")
    #             bool1 = False
    #         elif j == 2 and ((tmp < "0") or (tmp > "3")):
    #             messagebox.showinfo("警告", str(i+1) + "番目の時間帯番号が正しくありません。")
    #             bool1 = False

    #     if count in [1, 2]:
    #         messagebox.showinfo("警告", str(i+1) + "番目の入力が正しくありません。")
    #         bool1 = False
    #     elif count == 3:
    #         break
    #     elif count == 0:
    #         gym_day_time.append(tmp_list)
    # check_bl.append(bln.get())
    tmp = [int(x.strip()) for x in input_range.get().split(' ')]
    for i in range(len(tmp)):
        input_date.append(tmp[i])
    print(input_date)
    if bool1:
        chrome()


# Tkinterインスタンスの生成
root = tk.Tk()
# root.configure()
root.title("自動キャンセル待ち")
# root.geometry("1000x650")
root.geometry("400x300")

# label_header1 = tk.Label(
#     root, text=u'体育館・日付(dayのみ)・時間帯番号（0: 09:00 ～ 11:30", 1: "11:45 ～ 14:15", 2: 14:30 ～ 17:00, 3: 17:45 ～ 21:45, 18:15 ～ 21:45）', font=("Arial", "12", "bold"))
# label_header1.place(x=20, y=30)

# input_field = [[0 for i in range(3)] for j in range(15)]

# for i in range(15):
#     input_field[i][0] = tk.Entry(width=20, font=("Arial", "12", "normal"))
#     input_field[i][0].place(x=20, y=60+i*28)
#     input_field[i][1] = tk.Entry(width=5, font=("Arial", "12", "normal"))
#     input_field[i][1].place(x=210, y=60+i*28)
#     input_field[i][2] = tk.Entry(width=5, font=("Arial", "12", "normal"))
#     input_field[i][2].place(x=265, y=60+i*28)

# for i in range(15):
#     input_field[i] = ["","",""] # 初期化

# input_field[0] = ["東園小学校","1","3"]
# input_field[1] = ["東園小学校","4","3"]
# input_field[2] = ["東園小学校","11","3"]
# input_field[3] = ["東園小学校","15","3"]
# input_field[4] = ["東園小学校","18","3"]

# input_field[5] = ["和光小学校","1","3"]
# input_field[6] = ["和光小学校","4","3"]
# input_field[7] = ["和光小学校","8","3"]
# input_field[8] = ["和光小学校","25","3"]
# input_field[9] = ["和光小学校","29","3"]

# input_field[10] = ["北九条小学校","25","3"]
# input_field[11] = ["北九条小学校","29","3"]
# input_field[12] = ["美香保小学校","8","3"]
# input_field[13] = ["美香保小学校","25","3"]
# input_field[14] = []


label_header2 = tk.Label(
    root, text=u'取りたい日(例: 1 4 8 11)  無入力:毎日', font=("Arial", "12", "bold"))
label_header2.place(x=20, y=30)

# input_range = [0 for i in range(2)]
input_range = tk.Entry(width=25, font=("Arial", "12", "normal"))
input_range.place(x=20, y=58)
# input_range[1] = tk.Entry(width=5, font=("Arial", "12", "normal"))
# input_range[1].place(x=75, y=58)

button = tk.Button(text="キャンセル待ち開始", font=("Arial", "12", "bold"), command=click_botton)
button.place(x=20, y=90)
# bln = tk.BooleanVar(value=True)
# chk = tk.Checkbutton(root, text='親アカウントを参照する', font=("Arial", "12", "bold"), variable=bln)
# chk.place(x=130, y=58)
# img = tk.PhotoImage(file='pic.png')
# label_pic = tk.Label(root, image=img)
# label_pic.place(x=410, y=140)
root.mainloop()
