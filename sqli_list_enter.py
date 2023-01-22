from tkinter import *

#sql list
def sqli_list_enter():
    root2 = Tk()
    root2['bg'] = '#Fafafa'
    root2.title('SQLi_list')
    w = root2.winfo_screenwidth()
    h = root2.winfo_screenheight()
    root2.geometry('300x600+{}+{}'.format(w // 2 + 300, h // 2 - 300))
    root2.resizable(width=False, height=False)

    #fun clean all list
    def all_pop():
        y_for_lbl = 0.1
        while y_for_lbl < 0.8:
            Label(root2, text="                                         ", font=("Roboto Bold", 12)) \
                .place(relx=0, rely=y_for_lbl, anchor="nw")
            y_for_lbl += 0.04

    #fun add sql in list
    def add_sqli_in_list():
        if sqli_enter.get() != "":
            a = open('sqli_list', "a")
            a.write("*" + sqli_enter.get())
            a.close()
            sql_list()

    #fun
    def sql_list():
        y_for_lbl = 0.1
        a = open('sqli_list', "r")
        b, c = [], []
        for i in a:
            b.append(i)
        if len(b) != 0:
            for i in b[0].split('*'):
                c.append(i)
            c.pop(0)
            i = 0
            while y_for_lbl < 0.8:
                try:
                    Label(root2, text=c[i], font=("Roboto Bold", 12)) \
                        .place(relx=0, rely=y_for_lbl, anchor="nw")
                    y_for_lbl += 0.04
                    i += 1
                except:
                    Label(root2, text="                                         ", font=("Roboto Bold", 12)) \
                        .place(relx=0, rely=y_for_lbl, anchor="nw")
                    y_for_lbl += 0.04
        a.close()

    #fun delete last sqli
    def delete_last_sqli():
        a = open('sqli_list', "r")
        b, c = [], []
        for i in a:
            b.append(i)
        if len(b) != 0:
            for i in b[0].split('*'):
                c.append(i)
            c.pop(0)
            a.close()
            c.pop()
            a = open('sqli_list', "w")
            for i in c:
                a.write('*' + i)
            a.close()
            if len(c) != 0:
                sql_list()
            else:
                all_pop()
        else:
            a.close()

    #main fun clean all
    def delete_sqli_list():
        a = open('sqli_list', "w")
        a.close()
        all_pop()

    # 0 row
    sqli_enter = Entry(root2, font=("Roboto Bold", 12))
    sqli_enter.place(relx=0.01, rely=0.01, anchor="nw")
    Button(root2, text="Добавить", font=("Roboto Bold", 12), command=add_sqli_in_list) \
        .place(relx=0.7, rely=0, anchor="nw")
    # 1 row
    Label(root2, text="Список SQl-инъекций:", font=("Roboto Bold", 12)) \
        .place(relx=0, rely=0.05, anchor="nw")
    # 2 row
    sql_list()
    # relast row
    Button(root2, text="Удалить последнию SQL-инъекцию", font=("Roboto Bold", 12), command=delete_last_sqli) \
        .place(relx=0, rely=0.88, anchor="nw")
    # last row
    Button(root2, text="Очистить весь список", font=("Roboto Bold", 12), command=delete_sqli_list) \
        .place(relx=0, rely=0.94, anchor="nw")
    # main loop
    root2.mainloop()