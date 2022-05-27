
import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="add.gif")
        btn_open_dialog = tk.Button(toolbar, text='Add data', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.udpate_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='Edit', bg='#d7d8e0', bd=0, image=self.udpate_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.del_img= tk.PhotoImage(file='delete.gif')
        btn_del = tk.Button(toolbar, text='Delete', bg ='#d7d8e0', bd=0, image=self.del_img,
                            compound=tk.TOP, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='Search', bg='#d7d8e0',bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='Refresh', bg='#d7d8e0', bd=0, image=self.refresh_img,
                               compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('Id','Agent id', 'Client name','Patronymic','Surname', 'costs', 'Status'),
                                 height=20, show='headings')
        self.tree.column('Id', width=30, anchor=tk.CENTER)
        self.tree.column("Agent id", width=60, anchor=tk.CENTER)
        self.tree.column("Client name", width=115, anchor=tk.CENTER)
        self.tree.column("Patronymic", width=125, anchor=tk.CENTER)
        self.tree.column("Surname", width=135, anchor=tk.CENTER)
        self.tree.column("costs", width=150, anchor=tk.CENTER)
        self.tree.column("Status", width=60, anchor=tk.CENTER)

        self.tree.heading('Id', text='Id')
        self.tree.heading("Agent id", text='Agent id')
        self.tree.heading("Client name", text='Client name')
        self.tree.heading("Patronymic", text='Patronymic')
        self.tree.heading("Surname", text="Surname")
        self.tree.heading("costs", text='Costs')
        self.tree.heading("Status", text='Status')

        self.tree.pack(side=tk.LEFT)

        scroll =  tk.Scrollbar(self, command=self.tree.yview())
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
    def records(self, agent_id, first_name, second_name, last_name, price, status):
        self.db.insert_data(agent_id, first_name, second_name, last_name, price, status)
        self.view_records()

    def update_records(self, agent_id, first_name, second_name, last_name, price, status):
        self.db.c.execute('''UPDATE data SET agent_id=?,client_name=?, client_second_name=?,
                        client_last_name=?, cost=?, status=? WHERE agent_id=?''',
                        (agent_id, first_name, second_name, last_name, price, status,
                         self.tree.set(self.tree.selection()).get('Agent id')))
        #print(self.tree.set(self.tree.selection()).get('Agent id'))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM data''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values= row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM data WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, status):
        status = ('%'+status+'%',)
        self.db.c.execute('''SELECT * FROM data WHERE status LIKE ?''', status)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values= row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view =  app

    def init_child(self):
        self.title('Add client to data')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_id = tk.Label(self, text='Agent id:')#create if not exist
        label_id.place(x=50, y=20)
        label_fname = tk.Label(self, text='Client first name:')
        label_fname.place(x=50, y=50)
        label_second = tk.Label(self, text='Patronymic:')
        label_second.place(x=50, y=80)
        label_last = tk.Label(self, text='Surname:')
        label_last.place(x=50, y=110)
        label_sum = tk.Label(self, text='Price:')
        label_sum.place(x=50, y=140)
        label_st = tk.Label(self, text='Status:')
        label_st.place(x=50, y=170)

        self.entry_id = ttk.Entry(self)
        self.entry_id.place(x=200, y=20)
        self.entry_fname = ttk.Entry(self)
        self.entry_fname.place(x=200, y=50)
        self.entry_second= ttk.Entry(self)
        self.entry_second.place(x=200, y=80)
        self.entry_last= ttk.Entry(self)
        self.entry_last.place(x=200, y=110)
        self.entry_sum=ttk.Entry(self)
        self.entry_sum.place(x=200,y=140)
        #изменить расположение полей для ввода
        self.combobox = ttk.Combobox(self, values=[False, True])
        self.combobox.current(0)
        self.combobox.place(x=200, y=170)

        btn_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        btn_cancel.place(x=320, y=195)

        self.btn_ok = ttk.Button(self, text='Add')
        self.btn_ok.place(x=250, y=195)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_id.get(),self.entry_fname.get(),
                                                                  self.entry_second.get(),self.entry_last.get(),
                                                                  self.entry_sum.get(),self.combobox.get()))

        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.inint_edit()
        self.view = app
        self.db = db
        self.default_data()
    def inint_edit(self):
        self.title('Edit')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=250, y=195)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_id.get(),
                                                                           self.entry_fname.get(),
                                                                           self.entry_second.get(),
                                                                           self.entry_last.get(),
                                                                           self.entry_sum.get(),
                                                                           self.combobox.get()))
        self.btn_ok.destroy()
    def default_data(self):
        print(self.view.tree.set(self.view.tree.selection()))
        self.db.c.execute('''SELECT * FROM data WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0],'#1')))
        row = self.db.c.fetchone()
        self.entry_id.insert(0, row[1])
        self.entry_fname.insert(0, row[2])
        self.entry_second.insert(0, row[3])
        self.entry_last.insert(0, row[4])
        self.entry_sum.insert(0, row[5])
        if row[5] != True:
            self.combobox.current(0)


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Search')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        lable_search = tk.Label(self, text='Search')
        lable_search.place(x=50, y=20)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        bnt_canсel = ttk.Button(self, text='Close', command=self.destroy)
        bnt_canсel.place(x=185, y=50)

        bnt_search = ttk.Button(self, text='Search', command= self.entry_search)
        bnt_search.place(x=105, y=50)

        bnt_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        bnt_search.bind('Button-1', lambda event: self.destroy(), add='+')

class DB():
    def __init__(self):
        self.conn = sqlite3.connect("agency.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS data (id integer primary key autoincrement,agent_id integer, 
                        client_name text, client_second_name text, client_last_name text,cost int, status blob)''')
        self.conn.commit()


    def insert_data(self, id, fname, second, last, sum, status):
        self.c.execute('''INSERT INTO data (agent_id, client_name, client_second_name,
                            client_last_name, cost, status) VALUES (?,?,?,?,?,?)''',
                       (id, fname, second, last, sum, status))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Client's base")
    root.geometry("690x450+300+200")
    root.resizable(False, False)
    root.mainloop()