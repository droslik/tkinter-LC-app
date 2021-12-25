import tkinter as tk
from tkinter import ttk
import sqlite3
import sys


class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)      #метод super отыскивает базовый класс у класса main и возвращает его
                                    # дальше идет обращение к методу init этого найденного класса. Польза в том, что изменение родительского класса не требует изменения метода
        self.init_main()            # вызываем функцию через конструктор класса (init)
        self.db = db
        self.view_records()         # Для оторбажения данных в виджете treeview после первого запуска

    def init_main(self):            # создание функции, в которой будут храниться и инициализироваться все объекты графического интерфейса
        toolbar = tk.Frame(bg='grey', bd=2)   #bd - граница
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img=tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar, text='Add new LC', command=self.open_dialog, bg='grey', bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.png')
        btn_edit_dialog = tk.Button(toolbar, text='Edit', command=self.open_update_dialog, bg='grey', bd=0, compound=tk.TOP, image=self.update_img)     #6 реализация кнопки
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete = tk.Button(toolbar, text='Delete LC', command=self.delete_records, bg='grey', bd=0,
                                    compound=tk.TOP, image=self.delete_img)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Search', command=self.open_search_dialog, bg='grey', bd=0,
                               compound=tk.TOP, image=self.search_img)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.png')  # 8картинка для кнопки
        btn_refresh = tk.Button(toolbar, text='Refresh', command=self.view_records, bg='grey', bd=0,
                               compound=tk.TOP, image=self.refresh_img)
        btn_refresh.pack(side=tk.LEFT)


        self.tree = ttk.Treeview(self, columns=('ID', 'lc_number', 'imp_exp', 'applicant_name', 'beneficiary_name', 'beneficiary_address', 'lc_currency', 'lc_amount', 'issuance_date', 'expiry_date'), height=15, show='headings')    #2 Добавл. виджета tree(id=№п.п., show)
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('lc_number', width=100, anchor=tk.CENTER)
        self.tree.column('imp_exp', width=90, anchor=tk.CENTER)
        self.tree.column('applicant_name', width=130, anchor=tk.CENTER)
        #self.tree.column('applicant_address', width=160, anchor=tk.CENTER)
        self.tree.column('beneficiary_name', width=130, anchor=tk.CENTER)
        self.tree.column('beneficiary_address', width=170, anchor=tk.CENTER)
        self.tree.column('lc_currency', width=80, anchor=tk.CENTER)
        self.tree.column('lc_amount', width=100, anchor=tk.CENTER)
        self.tree.column('issuance_date', width=110, anchor=tk.CENTER)
        self.tree.column('expiry_date', width=110, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('lc_number', text='LC number')
        self.tree.heading('imp_exp', text='Import/Export')
        self.tree.heading('applicant_name', text="Applicant's name")
        #self.tree.heading('applicant_address', text="Applicant's address")
        self.tree.heading('beneficiary_name', text="Beneficiary's name")
        self.tree.heading('beneficiary_address', text="Beneficiary's address")
        self.tree.heading('lc_currency', text="LC currency")
        self.tree.heading('lc_amount', text="LC amount")
        self.tree.heading('issuance_date', text="Issuance date")
        self.tree.heading('expiry_date', text="Expiry date")
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date):   #5
        self.db.insert_data(lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date)
        self.view_records()     # необходимо для отображения информации в виджете Treeview после каждого запуска

    def update_record(self, lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date):     #6 функция для редактирования данных
        self.db.c.execute('''UPDATE lc1 SET lc_number=?, imp_exp=?, applicant_name=?, beneficiary_name=?, beneficiary_address=?, lc_currency=?, lc_amount=?, issuance_date=?, expiry_date=? WHERE ID=?''',
        (lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM lc1''')
        [self.tree.delete(i) for i in self.tree.get_children()]     # очистка содержимого виджета treeview при добавлении
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):    # функция для удаления записей
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM lc1 WHERE id=?''', (self.tree.set(selection_item, '#1'),))   #после #1 запятая, так как ID может быть двухзначным.
        self.db.conn.commit()
        self.view_records()

    def search_records(self, lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date):  #8 создаем функцию поиска по description
        self.lc_number = ('%' + lc_number + '%',)
        self.imp_exp = ('%' + imp_exp + '%',)
        self.applicant_name = ('%' + applicant_name + '%',)
        self.beneficiary_name = ('%' + beneficiary_name + '%',)
        self.beneficiary_address = ('%' + beneficiary_address + '%',)
        self.lc_currency = ('%' + lc_currency + '%',)
        self.lc_amount = ('%' + lc_amount + '%',)
        self.issuance_date = ('%' + issuance_date + '%',)
        self.expiry_date = ('%' + expiry_date + '%',)
        self.db.c.execute('''SELECT * FROM lc1 WHERE lc_number=upper? OR imp_exp=? OR applicant_name LIKE ? OR beneficiary_name=? OR beneficiary_address=? OR lc_currency=? OR lc_amount=? OR issuance_date=? OR expiry_date=?''', (lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date))
        [self.tree.delete(i) for i in self.tree.get_children()]                     # удаляем из таблицы все записи
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]   # вставляем в пустую таблицу найденные записи
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):   # функция, которая будет вызывать окно поиска по нажатию кнопки с главного окна программы и добавляет кнопку в тулбар
        Search()

class Password(tk.Frame):
    def __init__(self, passwind):
        super().__init__(passwind)
        self.init_password()

    def init_password(self):

        label1 = tk.Label(passwind, text='login', fg='black', font='100')
        label2 = tk.Label(passwind, text='password', fg='black', font='100')
        entry1 = tk.Entry(passwind, width=30, text='')
        entry2 = tk.Entry(passwind, width=30, text='')
        button1 = tk.Button(text='Enter', width=10, fg='black')
        label1.grid(row=0, column=0, sticky='E')
        label2.grid(row=1, column=0)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        button1.grid(row=4, column=1, sticky='W')

        checkbutt = tk.Checkbutton(passwind, text='remember me')
        checkbutt.grid(column=1, sticky='W')
        button1.bind('<Button-1>', lambda e: passwind.destroy())
        passwind.bind('<Escape>', lambda e: sys.exit())
        passwind.bind('<Alt-F4>', lambda e: sys.exit())
        passwind.protocol("WM_DELETE_WINDOW", lambda: sys.exit())


class Child(tk.Toplevel):           #создаем класс и наследуемся от Toplevel
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


        #self.open_window()
    def init_child(self):           # функция для инициализации виджетов и объектов дочерненго окна

        self.title('Add Letter of Credit')
        self.geometry('400x420+400+150')
        self.resizable(False, False)

        label_lc_number = ttk.Label(self, text='Please insert correct data in the fields:')
        label_lc_number.place(x=50, y=20)
        label_lc_number = ttk.Label(self, text='LC number:')
        label_lc_number.place(x=50, y=50)
        label_select = ttk.Label(self, text='Import/Export:')
        label_select.place(x=50, y=80)
        label_applicant_name = ttk.Label(self, text="Applicant's name:")
        label_applicant_name.place(x=50, y=110)
        label_applicant_address = ttk.Label(self, text="Applicant's address:")
        label_applicant_address.place(x=50, y=140)
        label_beneficiary_name = ttk.Label(self, text="Beneficiary's name:")
        label_beneficiary_name.place(x=50, y=170)
        label_beneficiary_address = ttk.Label(self, text="Beneficiary's address:")
        label_beneficiary_address.place(x=50, y=200)
        label_lc_currency = ttk.Label(self, text="LC currency:")
        label_lc_currency.place(x=50, y=230)
        label_lc_amount = ttk.Label(self, text="LC amount:")
        label_lc_amount.place(x=50, y=260)
        label_issuance_date = ttk.Label(self, text="Issuance date:")
        label_issuance_date.place(x=50, y=290)
        label_expiry_date = ttk.Label(self, text="Expiry date:")
        label_expiry_date.place(x=50, y=320)

        self.entry_lc_number = ttk.Entry((self))
        self.entry_lc_number.place(x=200, y=50, width=150)
        self.combobox = ttk.Combobox(self, values=[u'Import', u'Export'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80, width=150)
        self.entry_applicant_name = ttk.Entry((self))
        self.entry_applicant_name.place(x=200, y=110, width=150)

        self.btn_applicant_address = ttk.Button(self, text="Add Applicant's info", command=self.applicant_window)
        self.btn_applicant_address.place(x=200, y=140, width=150)
        self.btn_applicant_address.bind()

        #self.entry_applicant_address = ttk.Entry((self))
        #self.entry_applicant_address.place(x=200, y=140)
        self.entry_beneficiary_name = ttk.Entry((self))
        self.entry_beneficiary_name.place(x=200, y=170, width=150)
        self.entry_beneficiary_address = ttk.Entry((self))
        self.entry_beneficiary_address.place(x=200, y=200, width=150)
        self.entry_lc_currency = ttk.Entry((self))
        self.entry_lc_currency.place(x=200, y=230, width=150)
        self.entry_lc_amount = ttk.Entry((self))
        self.entry_lc_amount.place(x=200, y=260, width=150)
        self.entry_issuance_date = ttk.Entry((self))
        self.entry_issuance_date.place(x=200, y=290, width=150)
        self.entry_expiry_date = ttk.Entry((self))
        self.entry_expiry_date.place(x=200, y=320, width=150)


        btn_cancel=ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=300, y=360)
        self.btn_ok=ttk.Button(self, text='Add')
        self.btn_ok.place(x=200, y=360)

        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_lc_number.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_applicant_name.get(),
                                                                       #self.applicant_address(),
                                                                       self.entry_beneficiary_name.get(),
                                                                       self.entry_beneficiary_address.get(),
                                                                       self.entry_lc_currency.get(),
                                                                       self.entry_lc_amount.get(),
                                                                       self.entry_issuance_date.get(),
                                                                       self.entry_expiry_date.get()))



        self.grab_set()             # перехватыват все события в приложении
        self.focus_set()            # захватывает и удерживает фокус
    def applicant_window(self):
        self.applicant_address = Applicant(self)
        applicant.bind()
        self.applicant = applicant


class Applicant(tk.Toplevel):           #создаем класс и наследуемся от Toplevel
    def __init__(self, parent):
        super().__init__(parent)
        self.init_applicant_address()
        self.view = app
        #self.address()

    def address(self):
        self.applicant_address = [self.entry_applicant_country.get(),
                                  self.entry_applicant_region.get(),
                                  self.entry_applicant_district.get(),
                                  self.entry_applicant_city.get(),
                                  self.entry_applicant_street.get(),
                                  self.entry_applicant_building.get(),
                                  self.entry_applicant_room.get()]
        print(self.applicant_address)

    def init_applicant_address(self):           # функция для инициализации виджетов и объектов дочерненго окна
        self.title('Enter address')
        self.geometry('400x500+200+200')
        self.resizable(False, False)

        self.label_applicant_country = ttk.Label(self, text='Country:')
        self.label_applicant_country.place(x=50, y=50)
        self.label_applicant_region = ttk.Label(self, text='Region:')
        self.label_applicant_region.place(x=50, y=80)
        self.label_applicant_district = ttk.Label(self, text="District:")
        self.label_applicant_district.place(x=50, y=110)
        self.label_applicant_city = ttk.Label(self, text="City:")
        self.label_applicant_city.place(x=50, y=140)
        self.label_applicant_street = ttk.Label(self, text="Street:")
        self.label_applicant_street.place(x=50, y=170)
        self.label_applicant_building = ttk.Label(self, text="Building №:")
        self.label_applicant_building.place(x=50, y=200)
        self.label_applicant_room = ttk.Label(self, text="Room №:")
        self.label_applicant_room.place(x=50, y=230)


        self.entry_applicant_country = ttk.Entry((self))
        self.entry_applicant_country.place(x=200, y=50)
        self.entry_applicant_region = ttk.Entry((self))
        self.entry_applicant_region.place(x=200, y=80)
        self.entry_applicant_district = ttk.Entry((self))
        self.entry_applicant_district.place(x=200, y=110)
        self.entry_applicant_city = ttk.Entry((self))
        self.entry_applicant_city.place(x=200, y=140)
        self.entry_applicant_street = ttk.Entry((self))
        self.entry_applicant_street.place(x=200, y=170)
        self.entry_applicant_building = ttk.Entry((self))
        self.entry_applicant_building.place(x=200, y=200)
        self.entry_applicant_room = ttk.Entry((self))
        self.entry_applicant_room.place(x=200, y=230)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=300, y=270)

        self.btn_add = ttk.Button(self, text='Add', command=self.destroy)
        self.btn_add.place(x=220, y=270)
        self.btn_add.bind('<Button-1>', lambda event: self.address())
    def child_dialog (self):
        Child()

        self.grab_set()     # перехват всеx событий в приложении
        self.focus_set()



class Update(Child):                # Создание класса Update, который наследуется от класса Child
    def __init__(self):
        super().__init__()
        self.init_edit()            # Чтобы изменения в графическом интерфейсе отобразились пользователю
        self.view = app
        self.db = db
        self.auto_complete_data()
    def init_edit(self):            #6 функция редактирования, где создается новая кнопка "Редактировать"
        self.title('Edit item')
        btn_edit = ttk.Button(self, text='Edit', command=self.destroy)
        btn_edit.place(x=200, y=360)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_lc_number.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_applicant_name.get(),
                                                                          #self.entry_applicant_address.get(),
                                                                          self.entry_beneficiary_name.get(),
                                                                          self.entry_beneficiary_address.get(),
                                                                          self.entry_lc_currency.get(),
                                                                          self.entry_lc_amount.get(),
                                                                          self.entry_issuance_date.get(),
                                                                          self.entry_expiry_date.get()))
        self.btn_ok.destroy()           # удаление кнопки OK


    def auto_complete_data(self):       # функция для автозаполнения полей при открытии записи для редактирования
        self.db.c.execute('''SELECT * FROM lc1 WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0],'#1'),))
        row = self.db.c.fetchone()
        self.entry_lc_number.insert(0, row[1])
        if row[2] != 'Import':
            self.combobox.current(1)
        self.entry_applicant_name.insert(0, row[3])
        self.entry_beneficiary_name.insert(0, row[4])
        self.entry_beneficiary_address.insert(0, row[5])
        self.entry_lc_currency.insert(0, row[6])
        self.entry_lc_amount.insert(0, row[7])
        self.entry_issuance_date.insert(0, row[8])
        self.entry_expiry_date.insert(0, row[9])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app     # Для обращения из класса Search к функциям из класса Main

    def init_search(self):
        self.title('Поиск')
        self.geometry('400x400+400+150')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Please choose one or more criteria you wish to make a search by')
        label_search.place(x=50, y=20)
        label_search_options = tk.Label(self, text='Search by:')
        label_search_options.place(x=50, y=50)
        label_search_lc_number = tk.Label(self, text='LC number')
        label_search_lc_number.place(x=50, y=80)
        label_search_select = ttk.Label(self, text='LC type (Import/Export):')
        label_search_select.place(x=50, y=110)
        label_search_applicant_name = ttk.Label(self, text="Applicant's name:")
        label_search_applicant_name.place(x=50, y=140)
        #label_search_applicant_address = ttk.Label(self, text="Search by Applicant's address:")
        #label_search_applicant_address.place(x=50, y=110)
        label_search_beneficiary_name = ttk.Label(self, text="Beneficiary's name:")
        label_search_beneficiary_name.place(x=50, y=170)
        label_search_beneficiary_address = ttk.Label(self, text="Beneficiary's address:")
        label_search_beneficiary_address.place(x=50, y=200)
        label_search_lc_currency = ttk.Label(self, text="LC currency:")
        label_search_lc_currency.place(x=50, y=230)
        label_search_lc_amount = ttk.Label(self, text="LC amount:")
        label_search_lc_amount.place(x=50, y=260)
        label_search_issuance_date = ttk.Label(self, text="Issuance date:")
        label_search_issuance_date.place(x=50, y=290)
        label_search_expiry_date = ttk.Label(self, text="Expiry date:")
        label_search_expiry_date.place(x=50, y=320)

        self.entry_search_lc_number = ttk.Entry(self)
        self.entry_search_lc_number.place(x=220, y=80, width=150)
        self.combobox_search_import_export = ttk.Combobox(self, values=[u'Import', u'Export', u''])
        self.combobox_search_import_export.current()
        self.combobox_search_import_export.place(x=220, y=110, width=150)
        self.entry_search_applicant_name = ttk.Entry((self))
        self.entry_search_applicant_name.place(x=220, y=140, width=150)
        self.entry_search_beneficiary_name = ttk.Entry((self))
        self.entry_search_beneficiary_name.place(x=220, y=170, width=150)
        self.entry_search_beneficiary_address = ttk.Entry((self))
        self.entry_search_beneficiary_address.place(x=220, y=200, width=150)
        self.entry_search_lc_currency = ttk.Entry((self))
        self.entry_search_lc_currency.place(x=220, y=230, width=150)
        self.entry_search_lc_amount = ttk.Entry((self))
        self.entry_search_lc_amount.place(x=220, y=260, width=150)
        self.entry_search_issuance_date = ttk.Entry((self))
        self.entry_search_issuance_date.place(x=220, y=290, width=150)
        self.entry_search_expiry_date = ttk.Entry((self))
        self.entry_search_expiry_date.place(x=220, y=320, width=150)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=300, y=350)

        btn_search = ttk.Button(self, text='Search')
        btn_search.place(x=220, y=350)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search_lc_number.get(),
                                                                             self.combobox_search_import_export.get(),
                                                                             self.entry_search_applicant_name.get(),
                                                                             self.entry_search_beneficiary_name.get(),
                                                                             self.entry_search_beneficiary_address.get(),
                                                                             self.entry_search_lc_currency.get(),
                                                                             self.entry_search_lc_amount.get(),
                                                                             self.entry_search_issuance_date.get(),
                                                                             self.entry_search_expiry_date.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')   #8 Для закрытия окна поиска по нажатию клавиши.

        self.grab_set()  # перехват всеx событий в приложении
        self.focus_set()

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('lc1.db')  # соединение с БД. Метод connect, аргумент - файл finance.db. Если его нет, то будет создан.
        self.c = self.conn.cursor()     # создание эксзепляра класса курсор, который позволяет взаимодействовать с БД. ЧТобы создать БД - метод execute
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS lc1 (id integer primary key, lc_number text, imp_exp text, applicant_name text, beneficiary_name text, beneficiary_address text, lc_currency text, lc_amount integer, issuance_date date, expiry_date date)''')
        self.conn.commit()   # для сохранения результатов работы с БД необходимо вызвать метод commit класса connection.

    def insert_data(self, lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date):
        self.c.execute('''INSERT INTO lc1 (lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date) VALUES (?,?,?,?,?,?,?,?,?)''', (lc_number, imp_exp, applicant_name, beneficiary_name, beneficiary_address, lc_currency, lc_amount, issuance_date, expiry_date))  #5 добавляем в БД в поля ... значения (кортежа)
        self.conn.commit()    # cохранение


if __name__ == '__main__':          # если скрипт запущен как основная программа, то ее содержание выполнится. Если же он импортируется, то выполнения не будет.
    passwind = tk.Tk()              # создание окна авторизации
    app1 = Password(passwind)
    app1.grid()
    passwind.title('Log in')
    passwind.geometry('300x150+550+300')
    passwind.resizable(False, False)
    passwind.mainloop()

    root = tk.Tk()                  # создание корневого окна программы
    db = DB()                       # создается экземпляр класса DB для обращения к функциям класса DB из класса Main.
    app = Main(root)
    app.pack()

    root.title('Letters of Credit')
    root.geometry('1070x500+150+100')
    root.resizable(True, False)
    root.mainloop()