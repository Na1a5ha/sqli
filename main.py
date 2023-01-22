import os
from tkinter import *
from sqli_list_enter import sqli_list_enter
from sql_uri import sql_in_uri
from sqli_enter_form2 import sql_find_in_ef
from uri_check import click_ex_uri

#function recall
def click_ex():
    global key_s
    key_s = click_ex_uri(uri_enter.get())

#main function
def click_main():
    #sqli list -> c
    a = open('sqli_list', "r")
    b, c = [], []
    for i in a:
        b.append(i)
    if len(b) != 0:
        for i in b[0].split('*'):
            c.append(i)
        c.pop(0)
    #url valid?
    global lb1
    if key_s is False:
        lb1.config(text="Сначала подтвердите URI")
    else:
        # check conf
        k_conf = ""
        if v_chb_1.get() == 1:
            k_conf += "1"
        if v_chb_2.get() == 1:
            k_conf += "2"
        if v_chb_3.get() == 1:
            k_conf += "3"
        if len(k_conf) == 0:
            lb1.config(text='Сначала выбирите конфигурации')
            return
        #change rb
        if opt_sql.get() == 0:
            db = sql_find_in_ef(uri_enter.get(), k_conf, c)
            text_lb_1 = "Тип SQL-инъекции: SQL-инъекция в формы ввода\n"
            lb1.config(text=text_lb_1)
        else:
            db = sql_in_uri(uri_enter.get(), k_conf,c)
            text_lb_1 = "Тип SQL-инъекции: SQL-инъекция в URI\n"
            lb1.config(text=text_lb_1)
        #for y metrix
        y_for_lbl = 0.48
        #for test
            # db = ["0"]
            # db = ["1input[type='text']0", "2input[type='text']0", "2input[type='password']0", "2textarea[name='my_signature']1", "2input[type='text']1", "2input[type='password']1", '2all1', "31"]
        #draw answer
        file_4_answer = open('SQL-scanner.txt', 'w')
        #check db
        try:
            len(db)
        except:
            db = ["0"]
        # var for check y
        b = 0
        #draw ui answer
        for i in range(len(db)):
            if y_for_lbl > 0.8:
                if b == 0:
                    a = str(len(db) - i)
                    Label(text="и еще "+ a + " уязвимость(ей)", font=("Roboto Bold", 12)) \
                        .place(relx=0, rely=0.85, anchor="nw")
                    b = 1
            if db[i][:1].find("1") != -1:
                if len(db[i][1:-1]) > 0:
                    a = "SQLi - " + c[int(db[i][-1])] +" Уязвимость в поле \"" + db[i][1:-1] + "\" - статус код"
                    file_4_answer.write(a + "\n")
                    if b == 0:
                        Label(text=a, font=("Roboto Bold", 12)) \
                            .place(relx=0, rely=y_for_lbl, anchor="nw")
                        y_for_lbl+=0.08
                else:
                    a = "SQLi - " + c[int(db[i][-1])] +" Уязвимость статус код"
                    file_4_answer.write(a + "\n")
                    if b == 0:
                        Label(text=a, font=("Roboto Bold", 12)) \
                            .place(relx=0, rely=y_for_lbl, anchor="nw")
                        y_for_lbl+=0.08
            elif db[i][:1].find("2") != -1:
                if len(db[i][1:-1]) > 0:
                    a = "SQLi - " + c[int(db[i][-1])] +" Уязвимость в поле \"" + db[i][1:-1] + "\" - страница ошибки"
                    file_4_answer.write(a + "\n")
                    if b == 0:
                        Label(text=a, font=("Roboto Bold", 12)) \
                            .place(relx=0, rely=y_for_lbl, anchor="nw")
                        y_for_lbl += 0.08
                else:
                    a = "SQLi - " + c[int(db[i][-1])] +" - Уязвимость - страница ошибки"
                    file_4_answer.write(a + "\n")
                    if b == 0:
                        Label(text=a, font=("Roboto Bold", 12)) \
                            .place(relx=0, rely=y_for_lbl, anchor="nw")
                    y_for_lbl += 0.08
            elif db[i][:1].find("3") != -1:
                a = "SQLi - " + c[int(db[i][-1])] +" - Уязвимость - время загрузки страницы >1c"
                file_4_answer.write(a + "\n")
                if b == 0:
                    Label(text=a, font=("Roboto Bold", 12)) \
                        .place(relx=0, rely=y_for_lbl, anchor="nw")
                    y_for_lbl+=0.08
            else:
                a = "Уязвимость не обнаружена"
                file_4_answer.write(a + "\n")
                Label(text=a, font=("Roboto Bold", 12)) \
                    .place(relx=0, rely=y_for_lbl, anchor="nw")
                break
        Label(text="Полный отчет сформирован", font=("Roboto Bold", 12)) \
            .place(relx=0, rely=0.9, anchor="nw")

#clean func
def delete_all():
    y_for_lbl = 0.48
    a = " "*1000
    while y_for_lbl < 0.92:
        Label(text=a, font=("Roboto Bold", 12)) \
            .place(relx=0, rely=y_for_lbl, anchor="nw")
        y_for_lbl+=0.03

#fun open txt
def open_full_txt():
    osCommandString = "notepad.exe SQL-scanner.txt"
    os.system(osCommandString)

#main loop
if __name__ == "__main__":
    #main
    root = Tk()
    root['bg'] = '#Fafafa'
    root.title('SQLi-finder')
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry('600x600+{}+{}'.format(w // 2 - 300, h // 2 - 300))
    root.resizable(width=False, height=False)
    key_s = False

    #vars
    opt_sql = IntVar()
    v_chb_1 = IntVar()
    v_chb_2 = IntVar()
    v_chb_3 = IntVar()
    opt_sql.set(0)
    v_chb_1.set(0)
    v_chb_2.set(0)
    v_chb_3.set(0)

    #0 row
    Label(text="Введите URI:", font=("Roboto Bold", 12)) \
        .place(relx=0, rely=0, relheight=0.05, relwidth=0.2)

    uri_enter = Entry(root, font=("Roboto Bold", 12))
    uri_enter.place(relx=0.2, rely=0, relheight=0.05, relwidth=0.7)

    Button(text="Подтвердить URI", font=("Roboto Bold", 12), command=click_ex) \
        .place(relx=0.7, rely=0, relheight=0.05, relwidth=0.3)

    #1 row
    #call

    # #2 row
    Label(text="Выбирите тип SQL-инъекции:", font=("Roboto Bold", 12)) \
        .place(relx=0, rely=0.1, relheight=0.05, relwidth=0.38)

    rb0 = Radiobutton(text="1 - ", variable=opt_sql, value=0, font=("Roboto Bold", 12))
    rb0.place(relx=0.4, rely=0.1, relheight=0.05, relwidth=0.1)

    Label(text="SQL-инъекция в формы ввода", font=("Roboto Bold", 12)) \
        .place(relx=0.5, rely=0.1, relheight=0.05, relwidth=0.37)

    #3 row
    rb1 = Radiobutton(text="2 - ", variable=opt_sql, value=1, font=("Roboto Bold", 12))
    rb1.place(relx=0.4, rely=0.15, relheight=0.05, relwidth=0.1)

    Label(text="SQL-инъекция в URI", font=("Roboto Bold", 12)) \
        .place(relx=0.5, rely=0.15, relheight=0.05, relwidth=0.25)

    #4 row
    Label(text="Конфигурации:", font=("Roboto Bold", 12)) \
        .place(relx=0, rely=0.2, relheight=0.05, relwidth=0.2)

    chb_1 = Checkbutton(text="", variable=v_chb_1, font=("Roboto Bold", 12), onvalue=1, offvalue=0)
    chb_1.place(relx=0.2, rely=0.2, relheight=0.05, relwidth=0.1)

    Label(text="проверка статус кода страницы", font=("Roboto Bold", 12)) \
        .place(relx=0.26, rely=0.2, relheight=0.05, relwidth=0.4)

    #5 row
    chb_2 = Checkbutton(text="", variable=v_chb_2, font=("Roboto Bold", 12), onvalue=1, offvalue=0)
    chb_2.place(relx=0.2, rely=0.25, relheight=0.05, relwidth=0.1)

    Label(text="нахождение ошибки на странице", font=("Roboto Bold", 12)) \
        .place(relx=0.26, rely=0.25, relheight=0.05, relwidth=0.4)
    #6 row
    chb_3 = Checkbutton(text="", variable=v_chb_3, font=("Roboto Bold", 12), onvalue=1, offvalue=0)
    chb_3.place(relx=0.2, rely=0.3, relheight=0.05, relwidth=0.1)

    Label(text="проверка времени загрузки страцины", font=("Roboto Bold", 12)) \
        .place(relx=0.26, rely=0.3, relheight=0.05, relwidth=0.47)
    #7 row
    Button(text="Начать проверку на нахождение уязвимости", font=("Roboto Bold", 12), command=click_main, height=2) \
        .place(relx=0.03, rely=0.35, relheight=0.05, relwidth=0.6)
    Button(text="Список SQL-инъекций", font=("Roboto Bold", 12), command=sqli_list_enter, height=2) \
        .place(relx=0.68, rely=0.35, relheight=0.05, relwidth=0.3)
    #8 row
    lb1 = Label(text="", font=("Roboto Bold", 12))
    lb1.place(relx=0, rely=0.4, anchor="nw")
    #last row
    Button(root, text="Очистить поле вывода", font=("Roboto Bold", 12), command=delete_all) \
        .place(relx=0.3, rely=0.94, anchor="nw")
    Button(root, text="Открыть отчет", font=("Roboto Bold", 12), command=open_full_txt) \
        .place(relx=0.01, rely=0.94, anchor="nw")
    root.mainloop()
