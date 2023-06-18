class Product:
    def __init__(self, ime_produkta, id):
        self.id = id
        self.ime_produkta = ime_produkta
        self.kolicina = 1
        self.dodaten_napajalnik = True
        self.eu_napajalni_kabel = True
        self.dodatni_stack_kabli = False
        self.dna_lic = 5 #lahko vsebuje samo števila 3, 5, 7 kot za leta licenc
        self.console_cab = "RJ45" #lahko je: 'USB', 'RJ45 ali 'brez'
        self.network_modul = "brez" #lahko je: '4X' kot 10G, '4G' kot 1G ALI 'brez'
        self.network_licenca = True

        self.storage_module = "brez" #lahko je: "240g" ali "brez"
        self.stack_pwr_cables = "brez" #lahko je: "150cm", "30cm" ali "brez"
        self.stack_wise_cable = "3m" ##lahko je: '50cm', '1m', '3m', ali 'brez'
        self.scnd_pwr_sply = "715wac" ##lahko je: '350wac', '715wac', '1100wac', '715wdc' ali 'brez'

        #dostopne točke
        self.dna_ap = "DNAe" #lahko je: 'DNAa', 'DNAe', 'DNAoptout', ali 'brez'
        self.mb_ap = "MBuni"  #lahko je: 'MBlow', 'MBuni' ali 'brez'
        self.ceiling_clips_ap = "RAILr"  #lahko je: 'RAILr', 'RAILf', 'adapter', ali 'brez'
        self.pacaking_ap = True  #lahko je: 'True' kot SINGLE pacaking ali 'False'kot multi pacaking

        #podpora
        self.let_podpore  = 3
        self.tip_podpore = "PSRT" #lahko je: 'PSRT',

