import time
import tkinter as tk
from tkinter import ttk, messagebox

import Buildandprice_bot
import Product as pr
from threading import *
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
        self.network_lic = tk.BooleanVar()
        option_menu_list = ["Izberi opcijo", "Cisco Catalyst 9200 serija", "Dostopne točke serija 1000"]
        self.option_menu_var = tk.StringVar(value= option_menu_list[1])
        self.dna_var = tk.IntVar()
        self.console_cab_var = tk.StringVar()
        self.network_module_var = tk.StringVar()
        self.service_var = tk.StringVar()
        self.service_years_var = tk.IntVar()
        self.storage_module_var = tk.StringVar()
        self.stack_pwr_cable_var = tk.StringVar()
        self.stack_wise_var = tk.StringVar()
        self.sel_scnd_pwr_sply_var = tk.StringVar()
        self.dna_ap_var = tk.StringVar()
        self.mb_ap_var = tk.StringVar()
        self.ceiling_clips_var = tk.StringVar()
        self.ap_pacaking_var = tk.BooleanVar()


        # Ustvari okvir za izbiro specifikacije
        self.check_specifications = ttk.LabelFrame(self, text="Izberi osnovne specifikacije", padding=(5, 2.5))
        self.check_specifications.grid(row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")



        # Chech Buttoni za izbiro specifikacije
        self.check_1 = ttk.Checkbutton(self.check_specifications, variable=self.dodaten_napajalnik, text="Dodaten napajalnik", command=self.dod_napajalnik_clicked)
        self.check_2 = ttk.Checkbutton(self.check_specifications, variable=self.eu_power_cable, text="EU napajalni kabel")
        self.check_3 = ttk.Checkbutton(self.check_specifications, variable=self.stack_cable, text="Stack modul")
        self.check_4 = ttk.Checkbutton(self.check_specifications, variable=self.network_lic, text="Network licenca")

        # Console cables
        self.console_cab_usb = ttk.Radiobutton(self.check_specifications, text="Console cable USB", variable=self.console_cab_var, value="USB")
        self.console_cab_rj45 = ttk.Radiobutton(self.check_specifications, text="Console cable RJ45", variable=self.console_cab_var, value="RJ45")

        #Dodajanje v grid za izbiro specifikacije
        self.check_1.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.check_2.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        self.check_3.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
        self.check_4.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")
        self.console_cab_usb.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        self.console_cab_rj45.grid(row=3, column=1, padx=5, pady=10, sticky="nsew")

        #gumb izbriši
        self.delete_button = ttk.Button(self.check_specifications, text="Izbriši izbran produkt", command=self.delete_product)
        self.delete_button.grid(row=4, column=0, padx=0, pady=10, columnspan=4)


        # Ustvari okvir za izbiro DNA licence
        self.dna_lic_frame = ttk.LabelFrame(self, text="Izberi DNA licenco", padding=(0, 0))
        self.dna_lic_frame.grid(row=1, column=1, padx=(20, 10), pady=(0, 0), sticky="nsew")

        # DNA licence
        self.dna_3y = ttk.Radiobutton(self.dna_lic_frame, text="3 leta", variable=self.dna_var, value=3)
        self.dna_5y = ttk.Radiobutton(self.dna_lic_frame, text="5 let", variable=self.dna_var, value=5)
        self.dna_7y = ttk.Radiobutton(self.dna_lic_frame, text="7 let", variable=self.dna_var, value=7)

        # Dodajanje DNA v grid
        self.dna_3y.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.dna_5y.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        self.dna_7y.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

        # Ustvari okvir za gumb Poženi
        self.run_btn = ttk.LabelFrame(self, text="Poženi", padding=(20, 10))
        self.run_btn.grid(row=3, column=1, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # gumb izbriši
        self.delete_button = ttk.Button(self.run_btn, text="Poženi", style="Accent.TButton", command=self.run_build_n_price)
        self.delete_button.grid(row=0, column=0, padx=0, pady=10, columnspan=4)

        # Panedwindow - za izbiro stikal
        paned_selected = ttk.PanedWindow(self)
        paned_selected.grid(row=0, column=0, pady=(25, 5), sticky="nsew", rowspan=3)

        # Panedwindow - za izbiro stikal
        paned = ttk.PanedWindow(self)
        paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

        # Pane #1
        pane_1 = ttk.Frame(paned, padding=5)
        paned.add(pane_1, weight=1)

        # Notebook, pane #2
        self.pane_2 = ttk.Frame(paned, padding=5)
        paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="Izbira stikal")



        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tab_1)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        self.treeview_data = ttk.Treeview(
            self.tab_1,
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
            (1, 2, "C9200L-24P-4G-E", ("Subitem 1.1", "Value 1.1")),
            (1, 3, "C9200L-24P-4X-E", ("Subitem 1.2", "Value 1.2")),
            (1, 4, "C9200-24PB", ("Subitem 1.3", "Value 1.3")),
            (1, 5, "C9200-48P-E", ("Subitem 1.4", "Value 1.4")),
            (1, 6, "C9300-24T-E", ("Subitem 1.4", "Value 1.4")),
            ("", 6 + 1, "Parent", ("Item 2", "Value 2")),
            (6, 7 + 1, "Child", ("Subitem 2.1", "Value 2.1")),
            (6, 8 + 1, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
            (8, 9 + 1, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
            (8, 10 + 1, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
            (8, 11 + 1, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
            (6, 12 + 1, "Child", ("Subitem 2.3", "Value 2.3")),
            (6, 13 + 1, "Child", ("Subitem 2.4", "Value 2.4")),
            ("", 14 + 1, "Dostopne točke", ("", "")),
            (14 + 1, 15 + 1, "C9120AXI-E", ("Subitem 3.1", "Value 3.1")),
            (14 + 1, 16 + 1, "Child", ("Subitem 3.2", "Value 3.2")),
            (14 + 1, 17 + 1, "Child", ("Subitem 3.3", "Value 3.3")),
            (14 + 1, 18 + 1, "Child", ("Subitem 3.4", "Value 3.4")),
            ("", 19 + 1, "Parent", ("Item 4", "Value 4")),
        ]

        # Insert treeview data
        for item in treeview_data:
            self.treeview_data.insert(parent=item[0], index="end", iid=item[1], text=item[2], values=item[3])
            if item[0] == "" or item[1] in {8, 21}:
                self.treeview_data.item(item[1], open=True)  # Open parents

        # Select and scroll
        self.treeview_data.selection_set(10)
        self.treeview_data.see(7)
        self.treeview_data.bind("<ButtonRelease-1>", self.selectItem)  # izpiše takoj, ko kliknemo v tabeli s podatki

        # Paned za naprave, ki jih je uporavnik izbral
        # Paned za naprave, ki jih je uporavnik izbral
        # Paned za naprave, ki jih je uporavnik izbral
        # Paned za naprave, ki jih je uporavnik izbral



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

        # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_2.columnconfigure(index=index, weight=1)
            self.tab_2.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_2, text="Izberi service")

        self.notebook.add(self.tab_2, text="Napredno konf. produktov")


        # Ustvari okvir za izbiro Network Modula
        self.dna_lic_frame = ttk.LabelFrame(self.tab_2, text="Izberi Network Module", padding=(0, 0))
        self.dna_lic_frame.grid(row=0, column=0, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # DNA licence
        module_4x = ttk.Radiobutton(self.dna_lic_frame, text="4X - 10G", variable=self.network_module_var,value="4X")
        module_4g = ttk.Radiobutton(self.dna_lic_frame, text="4G - 1G", variable=self.network_module_var,value="4G")
        moudle_none = ttk.Radiobutton(self.dna_lic_frame, text="Brez", variable=self.network_module_var,value="brez")

        # Dodajanje DNA v grid
        module_4x.grid(row=0, column=0, padx=5, pady=10, sticky="nsew", columnspan=2)
        module_4g.grid(row=0, column=1, padx=5, pady=10, sticky="nsew", columnspan=2)
        moudle_none.grid(row=0, column=2, padx=5, pady=10, sticky="nsew", columnspan=2)

        # Ustvari okvir za izbiro Storage modula
        str_module_frame = ttk.LabelFrame(self.tab_2, text="Izberi Storage module", padding=(0, 0))
        str_module_frame.grid(row=0, column=1, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # Storage module
        str_module_240g = ttk.Radiobutton(str_module_frame, text="240G", variable=self.storage_module_var, value="240g")
        str_module_none = ttk.Radiobutton(str_module_frame, text="Brez", variable=self.storage_module_var, value="brez")

        # Dodajanje Storage module v grid
        str_module_240g.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        str_module_none.grid(row=0, column=1, padx=5, pady=10, sticky="nsew",)

        # Ustvari okvir za izbiro Stack power cables
        stack_pwr_cables_frame = ttk.LabelFrame(self.tab_2, text="Izberi Stack Power cables", padding=(0, 0))
        stack_pwr_cables_frame.grid(row=1, column=0, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # Stack power cables
        cab_150cm = ttk.Radiobutton(stack_pwr_cables_frame, text="CAB-SPWR-150CM", variable=self.stack_pwr_cable_var, value="150cm")
        cab_30cm = ttk.Radiobutton(stack_pwr_cables_frame, text="CAB-SPWR-30CM", variable=self.stack_pwr_cable_var, value="30cm")
        cab_none = ttk.Radiobutton(stack_pwr_cables_frame, text="Brez", variable=self.stack_pwr_cable_var, value="brez")

        # Dodajanje Stack power cables v grid
        cab_30cm.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        cab_150cm.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        cab_none.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        # Ustvari okvir za izbiro StackWise Cables
        stackwise_cables_frame = ttk.LabelFrame(self.tab_2, text="Izberi StackWise cables", padding=(0, 0))
        stackwise_cables_frame.grid(row=1, column=1, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # StackWise Cables
        wise_cab_50cm = ttk.Radiobutton(stackwise_cables_frame, text="STACK-50CM", variable=self.stack_wise_var, value="50cm")
        wise_cab_1m = ttk.Radiobutton(stackwise_cables_frame, text="STACK-1M", variable=self.stack_wise_var, value="1m")
        wise_cab_3m = ttk.Radiobutton(stackwise_cables_frame, text="STACK-3M", variable=self.stack_wise_var, value="3m")
        wise_cab_none = ttk.Radiobutton(stackwise_cables_frame, text="Brez", variable=self.stack_wise_var, value="brez")

        # Dodajanje StackWise Cables v grid
        wise_cab_50cm.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        wise_cab_1m.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        wise_cab_3m.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        wise_cab_none.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # Tab #3
        self.tab_3 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_3.columnconfigure(index=index, weight=1)
            self.tab_3.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_3, text="Izberi service")

        # Ustvari okvir za izbiro servica
        self.service_frame = ttk.Frame(self.tab_3, padding=(0, 0), borderwidth=0, border=0)
        self.service_frame.grid(row=0, column=0, padx=(0, 0), pady=(20, 10), sticky="nsew", columnspan=3)

        # radio button za izbiro servica
        self.prst = ttk.Radiobutton(self.service_frame, text="PRST - NBD", variable=self.service_var, value="PSRT")
        self.snt = ttk.Radiobutton(self.service_frame, text="SNT - NBD", variable=self.service_var, value="SNT")

        # Doda radio buttone za service v grid
        self.prst.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.snt.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        # radio button za izbiro let servica
        self.service_3y = ttk.Radiobutton(self.service_frame, text="3 leta", variable=self.service_years_var, value=3)
        self.service_5y = ttk.Radiobutton(self.service_frame, text="5 let", variable=self.service_years_var, value=5)
        self.service_7y = ttk.Radiobutton(self.service_frame, text="7 let", variable=self.service_years_var, value=7)

        # Doda radio buttone za let servica v grid
        self.service_3y.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.service_5y.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
        self.service_7y.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")


        # Tab #4
        self.tab_4 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_4.columnconfigure(index=index, weight=1)
            self.tab_4.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_4, text="Izberi dodaten napajalnik")
        self.notebook.hide(self.tab_4)

        # radio button za izbiro dodatnega napajalnika
        self.pwr_350_wac = ttk.Radiobutton(self.service_frame, text="PWR 350WAC", variable=self.sel_scnd_pwr_sply_var, value="350wac")
        self.pwr_715_wac = ttk.Radiobutton(self.service_frame, text="PWR 715WAC", variable=self.sel_scnd_pwr_sply_var, value="715wac")
        self.pwr_1100_wac = ttk.Radiobutton(self.service_frame, text="PWR 1100WAC", variable=self.sel_scnd_pwr_sply_var, value="1100wac")
        self.pwr_715_wdc = ttk.Radiobutton(self.service_frame, text="PWR 715WDC", variable=self.sel_scnd_pwr_sply_var, value="750wdc")
        self.pwr_none = ttk.Radiobutton(self.service_frame, text="Brez dodatnega napajalnika", variable=self.sel_scnd_pwr_sply_var, value="brez")

        # Doda radio buttone za dodatne napajalnike v grid
        self.service_3y.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.service_5y.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")
        self.service_7y.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")

        # Tab #5
        self.tab_5 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_5.columnconfigure(index=index, weight=1)
            self.tab_5.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_5, text="Specifikacije za dostopne točke")
        #self.notebook.hide(self.tab_5)

        # Ustvari okvir za izbiro DNA za dostopne točke
        dna_ap = ttk.LabelFrame(self.tab_5, text="Izberi DNA", padding=(0, 0))
        dna_ap.grid(row=0, column=0, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # radio button za izbiro DNA za dostopne točke
        dna_ap_a = ttk.Radiobutton(dna_ap, text="DNA Advantage", variable=self.dna_ap_var, value="DNAa")
        dna_ap_e = ttk.Radiobutton(dna_ap, text="DNA Essential", variable=self.dna_ap_var, value="DNAe")
        dna_ap_opt = ttk.Radiobutton(dna_ap, text="DNA OPTOUT", variable=self.dna_ap_var, value="DNAoptout")
        dna_ap_none = ttk.Radiobutton(dna_ap, text="Brez DNA", variable=self.dna_ap_var, value="brez")

        # Doda radio buttone za mounting bracket
        dna_ap_a.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        dna_ap_e.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        dna_ap_opt.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        dna_ap_none.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # Ustvari okvir za izbiro mounting bracket
        mb_ap = ttk.LabelFrame(self.tab_5, text="Izberi Mouting Bracket", padding=(0, 0))
        mb_ap.grid(row=1, column=0, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # radio button za izbiro mounting bracket
        bracket_low = ttk.Radiobutton(mb_ap, text="Low Profile MB", variable=self.mb_ap_var, value="MBlow")
        bracket_uni = ttk.Radiobutton(mb_ap, text="Universal Profile MB", variable=self.mb_ap_var, value="MBuni")
        bracket_low_none = ttk.Radiobutton(mb_ap, text="Brez MB", variable=self.mb_ap_var, value="brez")

        # Doda radio buttone za mounting bracket
        bracket_low.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        bracket_uni.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        bracket_low_none.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        # Ustvari okvir za izbiro ceiling clips
        ceiling_clips = ttk.LabelFrame(self.tab_5, text="Izberi Ceiling Grid clips", padding=(0, 0))
        ceiling_clips.grid(row=0, column=1, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # radio button za izbiro ceiling clips
        rail_r_cc = ttk.Radiobutton(ceiling_clips, text="Rail R", variable=self.ceiling_clips_var, value="RAILr")
        rail_f_cc = ttk.Radiobutton(ceiling_clips, text="Rail F", variable=self.ceiling_clips_var, value="RAILf")
        rail_adapter_cc = ttk.Radiobutton(ceiling_clips, text="Chanel Adapter", variable=self.ceiling_clips_var, value="adapter")
        rail_none_cc = ttk.Radiobutton(ceiling_clips, text="Brez Ceiling Clip-a", variable=self.ceiling_clips_var, value="brez")

        # Doda radio buttone za ceiling clips
        rail_r_cc.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        rail_f_cc.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        rail_adapter_cc.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        rail_none_cc.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        # Ustvari okvir za izbiro pakiranja
        packaging_ap = ttk.LabelFrame(self.tab_5, text="Izberi Ceiling Grid clips", padding=(0, 0))
        packaging_ap.grid(row=1, column=1, padx=(5, 5), pady=(10, 0), sticky="nsew", )

        # radio button za izbiro pakiranja
        packaging_single = ttk.Radiobutton(packaging_ap, text="Single pack", variable= self.ap_pacaking_var, value=True)
        packaging_multi = ttk.Radiobutton(packaging_ap, text="Multipack (min kol. 10)", variable= self.ap_pacaking_var, value=False)

        # Doda radio buttona za pakiranje
        packaging_single.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        packaging_multi.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

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
        self.network_lic.set(product.network_licenca)
        self.console_cab_var.set(product.console_cab)
        self.dna_var.set(product.dna_lic)
        self.network_module_var.set(product.network_modul)
        self.service_var.set(product.tip_podpore)
        self.service_years_var.set(product.let_podpore)
        self.storage_module_var.set(product.storage_module)
        self.stack_pwr_cable_var.set(product.stack_pwr_cables)
        self.stack_wise_var.set(product.stack_wise_cable)
        self.sel_scnd_pwr_sply_var.set(product.scnd_pwr_sply)
        self.dna_ap_var.set(product.dna_ap)
        self.mb_ap_var.set(product.mb_ap)
        self.ceiling_clips_var.set(product.ceiling_clips_ap)
        self.ap_pacaking_var.set(product.pacaking_ap)

        #če se je spremenil izbran produkt, se glede na to pokaže tab dodaten napajalnik
        self.dod_napajalnik_clicked()



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
            product.network_licenca = self.network_lic.get()
            product.console_cab = self.console_cab_var.get()
            product.dna_lic = self.dna_var.get()
            product.network_modul = self.network_module_var.get()
            product.tip_podpore = self.service_var.get()
            product.let_podpore = self.service_years_var.get()
            product.stack_pwr_cables = self.stack_pwr_cable_var.get()
            product.storage_module = self.storage_module_var.get()
            product.stack_wise_cable = self.stack_wise_var.get()
            product.scnd_pwr_sply = self.sel_scnd_pwr_sply_var.get()
            product.dna_ap = self.dna_ap_var.get()
            product.mb_ap = self.mb_ap_var.get()
            product.ceiling_clips_ap = self.ceiling_clips_var.get()
            product.pacaking_ap = self.ap_pacaking_var.get()

    def run_build_n_price(self):
        self.update_specs()

        t1 = Thread(target=self.run_thread())
        t1.start()
        t1.join()

    def run_thread(self):
        bot = Buildandprice_bot
        bot.main(self.dict_produktov, True)

    def dod_napajalnik_clicked(self):
        if self.dodaten_napajalnik.get():
            self.notebook.select(self.tab_4)
        else:
            self.notebook.hide(self.tab_4)



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