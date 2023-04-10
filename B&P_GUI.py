import time
import tkinter as tk
from tkinter import ttk, messagebox

import Product as pr
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

        #seznam produktov dodanih s strani uporabnika
        self.dict_produktov = {}
        self.id = 0
        self.product_id=0
        self.current_sel_id = None


    #nastavi vse potrebne elemente grafičnega vmesnika
    def setup_widgets(self):
        self.dodaten_napajalnik = tk.BooleanVar()
        self.eu_power_cable = tk.BooleanVar()
        self.stack_cable = tk.BooleanVar()
        self.option_menu_list = ["Izberi opcijo", "Cisco Catalyst 9200 serija", "Dostopne točke serija 1000"]
        self.option_menu_var = tk.StringVar(value= self.option_menu_list[1])


        # Ustvari okvir za izbiro specifikacije
        self.check_specifications = ttk.LabelFrame(self, text="Izberi specifikacijo", padding=(20, 10))
        self.check_specifications.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # Chech Buttoni za izbiro specifikacije
        self.check_1 = ttk.Checkbutton(self.check_specifications, variable=self.dodaten_napajalnik, text = "Dodaten napajalnik")
        self.check_2 = ttk.Checkbutton(self.check_specifications, variable=self.eu_power_cable, text="EU napajalni kabel")
        self.check_3 = ttk.Checkbutton(self.check_specifications, variable=self.stack_cable, text="Stack kabli")

        #Dodajanje v grid za izbiro specifikacije
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        #gumb izbriši
        self.delete_button = ttk.Button(self.check_specifications, text="Izbriši izbran produkt", command=self.delete_product)
        self.delete_button.grid(row=3, column=0, padx=5, pady=10)

        # Panedwindow - za izbiro stikal
        paned = ttk.PanedWindow(self)
        paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        pane_1 = ttk.Frame(paned, padding=5)
        paned.add(pane_1, weight=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(pane_1)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview_data = ttk.Treeview(
            pane_1,
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview_data.pack(expand=True, fill="both")
        scrollbar.config(command=self.treeview_data.yview)

        # Treeview columns
        self.treeview_data.column("#0", anchor="w", width=120)
        self.treeview_data.column(1, anchor="w", width=120)
        self.treeview_data.column(2, anchor="w", width=120)

        # Treeview headings
        self.treeview_data.heading("#0", text="Naprava", anchor="center")
        self.treeview_data.heading(1, text="Column 2", anchor="center")
        self.treeview_data.heading(2, text="Column 3", anchor="center")

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
            self.treeview_data.insert(parent=item[0], index="end", iid=item[1], text=item[2], values=item[3])
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview_data.item(item[1], open=True)  # Open parents

        # Select and scroll
        self.treeview_data.selection_set(10)
        self.treeview_data.see(7)
        self.treeview_data.bind( "<ButtonRelease-1>", self.selectItem) #izpiše takoj, ko kliknemo v tabeli s podatki


        #Paned za naprave, ki jih je uporavnik izbral
        #Paned za naprave, ki jih je uporavnik izbral
        #Paned za naprave, ki jih je uporavnik izbral
        #Paned za naprave, ki jih je uporavnik izbral

        # Panedwindow - za izbiro stikal
        paned_selected = ttk.PanedWindow(self)
        paned_selected.grid(row=0, column=0, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        pane_1_selected = ttk.Frame(paned_selected, padding=5)
        paned_selected.add(pane_1_selected, weight=1)

        # Scrollbar
        scrollbar_selected = ttk.Scrollbar(pane_1_selected)
        scrollbar_selected.pack(side="right", fill="y")

        # Treeview
        self.treeview_data_selected = ttk.Treeview(
            pane_1_selected,
            selectmode="browse",
            yscrollcommand=scrollbar_selected.set,
            columns=(1, 2),
            height=10,
        )
        self.treeview_data_selected.pack(expand=True, fill="both")
        scrollbar_selected.config(command=self.treeview_data_selected.yview)

        # Treeview columns
        self.treeview_data_selected.column("#0", anchor="w", width=120)
        self.treeview_data_selected.column(1, anchor="w", width=120)
        self.treeview_data_selected.column(2, anchor="w", width=120)

        # Treeview headings
        self.treeview_data_selected.heading("#0", text="Izbrane naprave", anchor="center")
        self.treeview_data_selected.heading(1, text="Stolpec 2", anchor="center")
        self.treeview_data_selected.heading(2, text="Stolpec 3", anchor="center")

        # Select and scroll
        self.treeview_data_selected.bind("<ButtonRelease-1>", self.selected_item_on_selection)  # izpiše takoj, ko kliknemo. to je za že izbrane


    #dobim element iz Treeview-a podatkov, katerega smo kliknili
    def selectItem(self, a):
        curItem = self.treeview_data.focus()
        izbran_produkt = self.treeview_data.item(curItem)["text"]#dobim slovar
        print(izbran_produkt)
        self.product_id+=1

        new_sel_product = pr.Product(izbran_produkt,self.product_id)
        self.dict_produktov[self.product_id] = new_sel_product
        self.update_selected_table()

    #Vedno na novo izpiše tabelo izbranih produktov iz sez_produktov()
    def update_selected_table(self):
        self.treeview_data_selected.delete(*self.treeview_data_selected.get_children()) #zbrisemo celotni treeview
        for key in self.dict_produktov:
            product = self.dict_produktov[key]
            terka = ("EU napajalni kabel", "Dodaten napajalnik", "asd")
            self.treeview_data_selected.insert(parent="", index="end", iid=product.id, text=product.ime_produkta, values=terka)

    #Tabela od že izbranih produktov. Se kliče ko kliknemo na izbrano vrstico
    def selected_item_on_selection(self,event): #getrow()
        rowid = self.treeview_data_selected.identify_row(event.y)
        print(rowid)
        self.update_specs() #update kličemo preden se se prikaže novi kliknjen produkt. Zato, da vemo kateri produkt poubdejtat, preden se zamenja
        try:
            self.current_sel_id = int(rowid)
            self.show_specs()
        except ValueError as e:
            print()
        except KeyError as e:
            print()
        except Exception as e:
            print()

    #takoj ko kliknemo na produkt, se prikažejo lastnosti produkta na chechboxih
    def show_specs(self):
        product = self.dict_produktov[self.current_sel_id]
        self.dodaten_napajalnik.set(product.dodaten_napajalnik)
        self.eu_power_cable.set(product.eu_napajalni_kabel)
        self.stack_cable.set(product.dodatni_stack_kabli)

    #Ko imamo izbrano neko vrstico in pritisnemo gumb "Izbriši" nam izbriše produkt iz Tabele izbranih produktov
    def delete_product(self):
        if self.current_sel_id  in self.dict_produktov:
            ime = self.dict_produktov[self.current_sel_id].ime_produkta
            if messagebox.askyesno("Potrdi izbris izbranega produkta", 'Ali si prepričan, da želiš izbrisati izbrani prodkut {}?'.format(ime)):
                del self.dict_produktov[self.current_sel_id]
                self.update_selected_table()
                self.current_sel_id = None #ko pobrišemo izbrano vrstico, potem trenutno nimamo več izbrane vrstice

    def update_specs(self):
        if self.current_sel_id != None:
            product = self.dict_produktov[self.current_sel_id]
            product.dodaten_napajalnik = self.dodaten_napajalnik.get()
            product.eu_napajalni_kabel = self.eu_power_cable.get()
            product.dodatni_stack_kabli = self.stack_cable.get()




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


    #https://www.youtube.com/watch?v=67hNu3A4tts - nastavljanje checkbox-ov
    #https://www.youtube.com/watch?v=i4qLI9lmkqw&t=0s - add, edit, remove čas 27:00