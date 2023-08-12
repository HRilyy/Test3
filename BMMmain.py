import re
from tkinter import *
from tkinter.tix import Tk

yuliaos = []
danci_set = []
shuangci_set = []
sanci_set = []
sici_set = []
wuci_set = []
danci_dict = {}
shuangci_dict = {}
sanci_dict = {}
sici_dict = {}
wuci_dict = {}
pending = []


def is_chinese(uchar):
    if u'\u00a4' <= uchar <= u'\uffe5':
        return True
    else:
        return False


def analyse_corpus(lines):  # 分析语料库
    for i in range(0, len(lines)):
        lines[i] = lines[i].rstrip('\n')  # 去掉换行符

    for line in lines:
        sts = re.split(' ', line)  # 按空格切分
        for i in range(0, len(sts)):
            for ch in sts[i]:
                if not is_chinese(ch):
                    sts[i] = sts[i].replace(ch, '')  # 去除非中文字符
        while '' in sts:
            sts.remove('')  # 清洗处理过程中产生的空字符
        if sts != '':
            pending.append(sts)  # 将得到的所有中文字符放入待处理列表中

    for line in pending:  # 在待处理列表中分类单字词、双字词、三字词、四字词和五字词
        for word in line:
            if len(word) == 1:
                danci_set.append(word)
            elif len(word) == 2:
                shuangci_set.append(word)
            elif len(word) == 3:
                sanci_set.append(word)
            elif len(word) == 4:
                sici_set.append(word)
            elif len(word) == 5:
                wuci_set.append(word)

    for danci in danci_set:
        if danci in danci_dict:
            danci_dict[danci] += 1
        else:
            danci_dict[danci] = 1
    for shuangci in shuangci_set:
        if shuangci in shuangci_dict:
            shuangci_dict[shuangci] += 1
        else:
            shuangci_dict[shuangci] = 1
    for sanci in sanci_set:
        if sanci in sanci_dict:
            sanci_dict[sanci] += 1
        else:
            sanci_dict[sanci] = 1
    for sici in sici_set:
        if sici in sici_dict:
            sici_dict[sici] += 1
        else:
            sici_dict[sici] = 1
    for wuci in wuci_set:
        if wuci in wuci_dict:
            wuci_dict[wuci] += 1
        else:
            wuci_dict[wuci] = 1


def BMMsegment(ststring):  # BMM逆向最大匹配算法
    result = []
    j = len(ststring)
    while j > 0:
        n = j
        if n >= 5:  # 最大切分长度为5
            temp5 = ststring[j - 5:j]
            temp4 = ststring[j - 4:j]
            temp3 = ststring[j - 3:j]
            temp2 = ststring[j - 2:j]
            temp1 = ststring[j - 1:j]

            if temp5 in wuci_dict:
                result.insert(0, temp5)
                j -= 5
            elif temp4 in sici_dict:
                result.insert(0, temp4)
                j -= 4
            elif temp3 in sanci_dict:
                result.insert(0, temp3)
                j -= 3
            elif temp2 in shuangci_dict:
                result.insert(0, temp2)
                j -= 2
            else:
                result.insert(0, temp1)
                j -= 1

        elif n == 4:
            temp4 = ststring[j - 4:j]
            temp3 = ststring[j - 3:j]
            temp2 = ststring[j - 2:j]
            temp1 = ststring[j - 1:j]

            if temp4 in sici_dict:
                result.insert(0, temp4)
                j -= 4
            elif temp3 in sanci_dict:
                result.insert(0, temp3)
                j -= 3
            elif temp2 in shuangci_dict:
                result.insert(0, temp2)
                j -= 2
            else:
                result.insert(0, temp1)
                j -= 1

        elif n == 3:
            temp3 = ststring[j - 3:j]
            temp2 = ststring[j - 2:j]
            temp1 = ststring[j - 1:j]

            if temp3 in sanci_dict:
                result.insert(0, temp3)
                j -= 3
            elif temp2 in shuangci_dict:
                result.insert(0, temp2)
                j -= 2
            else:
                result.insert(0, temp1)
                j -= 1

        elif n == 2:
            temp2 = ststring[j - 2:j]
            temp1 = ststring[j - 1:j]

            if temp2 in shuangci_dict:
                result.insert(0, temp2)
                j -= 2
            else:
                result.insert(0, temp1)
                j -= 1

        elif n == 1:
            temp1 = ststring[j - 1:j]
            result.insert(0, temp1)
            j -= 1
    return result


if __name__ == '__main__':
    root = Tk()
root.title("自然语言处理实验——中文分词")  # 设置窗口标题
root.geometry("400x400")  # 设置窗口大小
root.resizable(width=True, height=True)  # 设置窗口是否可以变化长宽，False不可变，Ture可变
root.tk.eval('package require Tix')  # 引入升级包，使用升级的组合控件

with open('1998-01-2003版-带音.txt', errors='ignore') as corpus:
    lines = corpus.readlines()
    analyse_corpus(lines)

label = Label(root, text="实验三BMM算法", fg=f'#CC99FF', bd=5, font=("楷体", 20), width=15, height=1)
label.pack(side=TOP)

label_cipai = Label(root, text="输入内容", bg='white')
label_cipai.pack()

entey = Entry(root, text='0', width=200, bd=5)
entey.pack()


def PRINT():  # 根据输入语句得到切分结果并展示
    results = []

    a = entey.get()
    results.append(BMMsegment(a))
    for result in results:
        for word in result:
            test_insert.insert(END, word + ' / ')
        test_insert.insert(END, '\n')


button = Button(root, text='运行', command=PRINT, activeforeground='white', activebackground='black', bg='white',
                fg='black', width=12)
button.pack()

test_insert = Text(root)
test_insert.pack()

root.mainloop()
