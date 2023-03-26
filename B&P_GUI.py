import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from os import path



class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # naredimo aplikacijo responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.izbrana_serija = ""
        self.izbran_produkt = ""

        # naredimo wigete
        self.setup_widgets()


    #nastavi vse potrebne elemente grafičnega vmesnika
    def setup_widgets(self):
        self.dodaten_napajalnik = tk.BooleanVar()
        self.eu_power_cable = tk.BooleanVar()
        self.stack_cable = tk.BooleanVar()
        self.option_menu_list = ["Izberi opcijo", "Cisco Catalyst 9200 serija", "Dostopne točke serija 1000"]
        self.option_menu_var = tk.StringVar(value= self.option_menu_list[1])

        # Ustvari okvir za Checkbuttons
        self.select_product_frame = ttk.LabelFrame(self, text="Izbira stikala", padding=(20, 10))
        self.select_product_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # Menu for the Menubutton
        self.menu = tk.Menu(self)
        self.menu.add_command(label="Cisco Cataylist serija 9000")
        self.menu.add_command(label="Menu item 2")
        self.menu.add_separator()
        self.menu.add_command(label="Dostopne točke")
        self.menu.add_command(label="Menu item 4")


        self.check_specifications = ttk.LabelFrame(self, text="Izberi specifikacijo", padding=(20, 10))
        self.check_specifications.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # Option button
        self.menubutton = ttk.OptionMenu(self.select_product_frame, self.option_menu_var, *self.option_menu_list, command=lambda m="da" : self.display_selected(m))
        self.menubutton.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.check_1 = ttk.Checkbutton(self.check_specifications, variable=self.dodaten_napajalnik, text = "Dodaten napajalnik")
        self.check_2 = ttk.Checkbutton(self.check_specifications, variable=self.eu_power_cable, text="EU napajalni kabel")
        self.check_3 = ttk.Checkbutton(self.check_specifications, variable=self.stack_cable, text="Stack kabli")

        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_1, weight=1)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.pane_1)
        self.scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)

        # Treeview columns
        self.treeview.column("#0", anchor="w", width=120)
        self.treeview.column(1, anchor="w", width=120)
        self.treeview.column(2, anchor="w", width=120)

        # Treeview headings
        self.treeview.heading("#0", text="Column 1", anchor="center")
        self.treeview.heading(1, text="Column 2", anchor="center")
        self.treeview.heading(2, text="Column 3", anchor="center")

        # Define treeview data
        treeview_data = [
            ("", 1, "9200 Serija", ("", "")),
            (1, 2, "C9200-24T", ("Subitem 1.1", "Value 1.1")),
            (1, 3, "C9200-24P", ("Subitem 1.2", "Value 1.2")),
            (1, 4, "C9200-24PB", ("Subitem 1.3", "Value 1.3")),
            (1, 5, "C9200-24PXG", ("Subitem 1.4", "Value 1.4")),
            (1, 6, "C9200-48T", ("Subitem 1.4", "Value 1.4")),
            ("", 6+1, "Parent", ("Item 2", "Value 2")),
            (6, 7+1, "Child", ("Subitem 2.1", "Value 2.1")),
            (6, 8+1, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (8, 9+1, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (8, 10+1, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (8, 11+1, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (6, 12+1, "Child", ("Subitem 2.3", "Value 2.3")),
            (6, 13+1, "Child", ("Subitem 2.4", "Value 2.4")),
            ("", 14+1, "Dostopne točke", ("", "")),
            (14+1, 15+1, "Child", ("Subitem 3.1", "Value 3.1")),
            (14+1, 16+1, "Child", ("Subitem 3.2", "Value 3.2")),
            (14+1, 17+1, "Child", ("Subitem 3.3", "Value 3.3")),
            (14+1, 18+1, "Child", ("Subitem 3.4", "Value 3.4")),
            ("", 19+1, "Parent", ("Item 4", "Value 4")),
        ]

        # Insert treeview data
        for item in treeview_data:
            self.treeview.insert(
                parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
            )
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview.item(item[1], open=True)  # Open parents

        # Select and scroll
        self.treeview.selection_set(10)
        self.treeview.see(7)
        self.treeview.bind( "<ButtonRelease-1>", self.selectItem) #izbiše takoj, ko kliknemo



    #Izpiše in vrne izbrano opciji pri "optionmenu"
    def display_selected(self,m):
        self.izbrana_serija = self.option_menu_var.get()
        print(self.izbrana_serija)


    def selectItem(self, a):
        curItem = self.treeview.focus()
        self.izbran_produkt = self.treeview.item(curItem)["text"]#dobim slovar
        print(self.izbran_produkt)
        self.add_selected_product(self.izbran_produkt)

    def add_selected_product(self, izbran_produkt):
        self.check_1 = ttk.Checkbutton(self.check_specifications, variable=self.dodaten_napajalnik, text="Dodaten napajalnik")
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    AppGUI = App(root)
    AppGUI.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()