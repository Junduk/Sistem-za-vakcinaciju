from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from vakcinisanje import *


class GlavniProzor(Tk):

    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Izlaz iz programa", "Da li ste sigurni da zelite napustiti aplikaciju?", icon="warning")
        if odgovor:
            self.destroy()

    def komanda_gradjani(self):
        gradjani_prozor = PristupGradjanima(self, self.__podaci)
        self.wait_window(gradjani_prozor)
        if gradjani_prozor.otkazano:
            return

    def popuni_listbox(self, gradjani):
        self.__listbox.delete(0, END)
        for gradjanin in gradjani:  # za svaki proizvod iz liste
            self.__listbox.insert(END, "{} {}".format(gradjanin.ime, gradjanin.prezime))
        self.ocisti_labele()

    def popuni_labele(self, osoba):
        self.__labela_jmbg["text"] = osoba.jmbg
        self.__labela_ime["text"] = osoba.ime
        self.__labela_prezime["text"] = osoba.prezime
        self.__labela_datum_rodjenja["text"] = osoba.datumRodjenja
        self.__labela_pol["text"] = osoba.pol

    def ocisti_labele(self):
        self.__labela_jmbg["text"] = ""
        self.__labela_ime["text"] = ""
        self.__labela_prezime["text"] = ""
        self.__labela_datum_rodjenja["text"] = ""
        self.__labela_pol["text"] = ""

    def azuriranje(self, event=None):
        if not self.__listbox.curselection():
            self.ocisti_labele()
            return
        indeks = self.__listbox.curselection()[0]
        gradjani = self.__podaci.gradjani[indeks]
        self.popuni_labele(gradjani)

    def __init__(self, podaci):
        super().__init__()
        self.__podaci = podaci

        self.title("Projektni zadatak")
        self.minsize(700, 400)
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        meni_bar = Menu(self)

        datoteka_menu = Menu(meni_bar, tearoff=0)
        datoteka_menu.add_command(label="Izlaz", command=self.komanda_izlaz)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_menu)

        self.__pristup_meni = Menu(meni_bar, tearoff=0)
        self.__pristup_meni.add_command(label="Gradjani", command=self.komanda_gradjani)
        self.__pristup_meni.add_command(label="Zdravstveni radnici")
        self.__pristup_meni.add_command(label="Vakcine")
        self.__pristup_meni.add_command(label="Potvrde")
        self.__pristup_meni.add_command(label="Sertifikati")
        meni_bar.add_cascade(label="Pristup", menu=self.__pristup_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.komanda_izlaz)

        # PRIKAZ LISTE OSOBA
        self.__listbox = Listbox(self, activestyle="none", exportselection=False)
        self.__listbox.pack(side=LEFT, fill=BOTH, expand=1)

        # FRAME
        frame = Frame(self, borderwidth=4, relief="ridge", padx=15, pady=15)
        frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # LABELE UNUTAR FRAME-A
        self.__labela_jmbg = Label(frame, text="dd")
        self.__labela_ime = Label(frame, text="dd")
        self.__labela_prezime = Label(frame, text="dd")
        self.__labela_datum_rodjenja = Label(frame, text="dd")
        self.__labela_pol = Label(frame, text="dd")

        Label(frame, text="JMBG:").grid(row=0, sticky=E)
        Label(frame, text="Ime:").grid(row=1, sticky=E)
        Label(frame, text="Prezime:").grid(row=2, sticky=E)
        Label(frame, text="Datum rodjenja:").grid(row=3, sticky=E)
        Label(frame, text="Pol:").grid(row=4, sticky=E)

        self.__labela_jmbg.grid(row=0, column=1, sticky=W)
        self.__labela_ime.grid(row=1, column=1, sticky=W)
        self.__labela_prezime.grid(row=2, column=1, sticky=W)
        self.__labela_datum_rodjenja.grid(row=3, column=1, sticky=W)
        self.__labela_pol.grid(row=4, column=1, sticky=W)

        # LISTA SA LEVE STRANE
        self.popuni_listbox(self.__podaci.gradjani)
        self.focus_force()
        self.__listbox.bind("<<ListboxSelect>>", self.azuriranje)


class PristupGradjanima(Toplevel):

    def popuni_listu(self, gradjani):
        self.__lista_listbox.delete(0, END)
        for gradjanin in gradjani:
            self.__lista_listbox.insert(END, "{} {}".format(gradjanin.ime, gradjanin.prezime))
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED

    def popuni_labele(self, gradjani):
        self.__labela_jmbg["text"] = gradjani.jmbg
        self.__labela_ime["text"] = gradjani.ime
        self.__labela_prezime["text"] = gradjani.prezime
        self.__labela_datum_rodjenja["text"] = gradjani.datumRodjenja
        self.__labela_pol["text"] = gradjani.pol
        self.__labela_broj_licne_karte["text"] = gradjani.brojLicneKarte
        self.__labela_lista_doza["text"] = gradjani.listaDoza
        self.__labela_lista_potvrda["text"] = gradjani.listaPotvrda
        self.__labela_sertifikat["text"] = gradjani.sertifikat

    def ocisti_labele(self):
        self.__labela_jmbg["text"] = ""
        self.__labela_ime["text"] = ""
        self.__labela_prezime["text"] = ""
        self.__labela_datum_rodjenja["text"] = ""
        self.__labela_pol["text"] = ""
        self.__labela_broj_licne_karte["text"] = ""
        self.__labela_lista_doza["text"] = ""
        self.__labela_lista_potvrda["text"] = ""
        self.__labela_sertifikat["text"] = ""

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__lista_listbox.curselection():
            self.ocisti_labele()
            self.__izmena_button['state'] = DISABLED
            self.__obrisi_button['state'] = DISABLED
            return

        indeks = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(indeks)
        gradjanin = 0
        for i in self.__podaci.gradjani:
            if str(i.ime + " " + i.prezime) == naziv:
                gradjanin = i
        self.popuni_labele(gradjanin)

        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def filtriranje_listbox(self, var, index, mode):
        self.ocisti_labele()
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED
        self.__lista_listbox.delete(0, END)
        text = self.__pretraga_entry.get()
        for gradjanin in self.__podaci.gradjani:
            if text.upper() in str(gradjanin.ime + gradjanin.prezime).upper():
                self.__lista_listbox.insert(END, "{} {}".format(gradjanin.ime, gradjanin.prezime))

    def brisanje(self, indeks):
        self.__podaci.gradjani.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.gradjani)
        self.__pretraga_entry["text"] = ""

    def izmena(self, indeks):

        class Izmena(Toplevel):
            @property
            def otkazano(self):
                return self.__otkazano

            def izmeni(self):
                ime = self.ogranicenje_ime()
                if not ime:
                    return

                prezime = self.ogranicenje_prezime()
                if not prezime:
                    return

                datumRodjenja = self.ogranicenje_datum_rodjenja()
                if not datumRodjenja:
                    return

                pol = self.ogranicenje_pol()
                if not pol:
                    return

                self.__podaci.gradjani[indeks].ime = ime
                self.__podaci.gradjani[indeks].prezime = prezime
                self.__podaci.gradjani[indeks].datumRodjenja = datumRodjenja
                self.__podaci.gradjani[indeks].pol = pol

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_ime(self):
                ime = self.__ime_entry.get()
                if len(ime) < 2:
                    messagebox.showerror("Greška", "Ime mora sadrzati bar 2 karaktera!")
                    return None
                return ime

            def ogranicenje_prezime(self):
                prezime = self.__prezime_entry.get()
                if len(prezime) < 2:
                    messagebox.showerror("Greška", "Prezime mora sadrzati bar 2 karaktera!")
                    return None
                return prezime

            def ogranicenje_datum_rodjenja(self):
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina < 1900 or godina > 2022:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif mesec < 1 or mesec > 12:
                    messagebox.showerror("Greška", "Ponovo unesite mesec!")
                    return None
                elif dan < 1 or dan > 31:
                    messagebox.showerror("Greška", "Ponovo unesite dan!")
                    return None
                elif mesec in [4, 6, 9, 11] and dan > 30:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 == 0 and mesec == 2 and dan > 29:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 != 0 and mesec == 2 and dan > 28:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif sat < 0 or sat > 24:
                    messagebox.showerror("Greška", "Ponovo unesite sat!")
                    return None
                elif minut < 0 or minut > 59:
                    messagebox.showerror("Greška", "Ponovo unesite minut!")
                    return None
                elif sekunda < 0 or sekunda > 59:
                    messagebox.showerror("Greška", "Ponovo unesite sekund!")
                    return None
                return str(datetime.datetime(godina, mesec, dan, sat, minut, sekunda))

            def ogranicenje_pol(self):
                pol = self.__pol_combobox.get()
                if pol == "":
                    messagebox.showerror("Greška", "Izaberite pol!")
                    return None
                return pol

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Izmena")
                self.minsize(400, 200)

                izmena_frame = Frame(self, padx=5, pady=5)
                izmena_frame.pack(expand=1)

                Label(izmena_frame, text="JMBG:").grid(row=0, sticky=E)
                self.__jmbg = StringVar(root)
                self.__jmbg_entry = Entry(izmena_frame, width=20, textvariable=self.__jmbg)
                self.__jmbg_entry.grid(row=0, column=1, sticky=W)
                self.__jmbg_entry.insert(0, self.__podaci.gradjani[indeks].jmbg)
                self.__jmbg_entry.config(state="disabled")

                Label(izmena_frame, text="Ime:").grid(row=1, sticky=E)
                self.__ime = StringVar(root)
                self.__ime_entry = Entry(izmena_frame, width=20, textvariable=self.__ime)
                self.__ime_entry.grid(row=1, column=1, sticky=W)

                Label(izmena_frame, text="Prezime:").grid(row=2, sticky=E)
                self.__prezime = StringVar(root)
                self.__prezime_entry = Entry(izmena_frame, width=20, textvariable=self.__prezime)
                self.__prezime_entry.grid(row=2, column=1, sticky=W)

                Label(izmena_frame, text="Datum rodjenja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(izmena_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=1900, increment=1, to=2022,
                                                textvariable=self.__vreme1)
                self.__godina_spinbox.grid(row=0, column=0, sticky=W)
                self.__vreme2 = IntVar(root)
                self.__mesec_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=12,
                                               textvariable=self.__vreme2)
                self.__mesec_spinbox.grid(row=0, column=1, sticky=W)
                self.__vreme3 = IntVar(root)
                self.__dan_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=31,
                                             textvariable=self.__vreme3)
                self.__dan_spinbox.grid(row=0, column=2, sticky=W)
                self.__vreme4 = IntVar(root)
                self.__sat_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=24,
                                             textvariable=self.__vreme4)
                self.__sat_spinbox.grid(row=0, column=3, sticky=W)
                self.__vreme5 = IntVar(root)
                self.__minut_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                               textvariable=self.__vreme5)
                self.__minut_spinbox.grid(row=0, column=4, sticky=W)
                self.__vreme6 = IntVar(root)
                self.__sekund_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                                textvariable=self.__vreme6)
                self.__sekund_spinbox.grid(row=0, column=5, sticky=W)

                Label(izmena_frame, text="Pol:").grid(row=4, sticky=E)
                self.__pol = StringVar(root)
                self.__pol_combobox = Combobox(izmena_frame, textvariable=self.__pol)
                self.__pol_combobox.grid(row=4, column=1, sticky=W)
                self.__pol_combobox['values'] = ('Zensko', 'Musko')

                Label(izmena_frame, text="Broj licne karte:").grid(row=5, sticky=E)
                self.__broj_licne_karte = StringVar(root)
                self.__broj_licne_karte_entry = Entry(izmena_frame, width=20, textvariable=self.__broj_licne_karte)
                self.__broj_licne_karte_entry.grid(row=5, column=1, sticky=W)
                self.__broj_licne_karte_entry.insert(0, self.__podaci.gradjani[indeks].brojLicneKarte)
                self.__broj_licne_karte_entry.config(state="disabled")

                self.__izmeni_button = Button(izmena_frame, width=10, command=self.izmeni, text="Izmeni")
                self.__izmeni_button.grid(row=6, column=1, sticky=W)

        izmena_prozor = Izmena(self, self.__podaci)
        self.wait_window(izmena_prozor)
        if izmena_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.gradjani)
        self.__pretraga_entry["text"] = ""

    def dodavanje(self):
        class Dodavanje(Toplevel):

            @property
            def otkazano(self):
                return self.__otkazano

            def dodaj(self):
                jmbg = self.ogranicenje_jmbg()
                if not jmbg:
                    return

                ime = self.ogranicenje_ime()
                if not ime:
                    return

                prezime = self.ogranicenje_prezime()
                if not prezime:
                    return

                datumRodjenja = self.ogranicenje_datum_rodjenja()
                if not datumRodjenja:
                    return

                pol = self.ogranicenje_pol()
                if not pol:
                    return

                brojLicneKarte = self.ogranicenje_licne_karte()
                if not brojLicneKarte:
                    return

                osoba = Osoba(jmbg, ime, prezime, datumRodjenja, pol)
                gradjanin = Gradjanin(osoba, brojLicneKarte, "", "", "")
                self.__podaci.gradjani.append(gradjanin)

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_jmbg(self):
                jmbg = self.__jmbg_entry.get()
                if len(jmbg) != 13:
                    messagebox.showerror("Greška", "JMBG mora sadrzati 13 cifara!")
                    return None
                return jmbg

            def ogranicenje_ime(self):
                ime = self.__ime_entry.get()
                if len(ime) < 2:
                    messagebox.showerror("Greška", "Ime mora sadrzati bar 2 karaktera!")
                    return None
                return ime

            def ogranicenje_prezime(self):
                prezime = self.__prezime_entry.get()
                if len(prezime) < 2:
                    messagebox.showerror("Greška", "Prezime mora sadrzati bar 2 karaktera!")
                    return None
                return prezime

            def ogranicenje_datum_rodjenja(self):
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina < 1900 or godina > 2022:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif mesec < 1 or mesec > 12:
                    messagebox.showerror("Greška", "Ponovo unesite mesec!")
                    return None
                elif dan < 1 or dan > 31:
                    messagebox.showerror("Greška", "Ponovo unesite dan!")
                    return None
                elif mesec in [4, 6, 9, 11] and dan > 30:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 == 0 and mesec == 2 and dan > 29:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 != 0 and mesec == 2 and dan > 28:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif sat < 0 or sat > 24:
                    messagebox.showerror("Greška", "Ponovo unesite sat!")
                    return None
                elif minut < 0 or minut > 59:
                    messagebox.showerror("Greška", "Ponovo unesite minut!")
                    return None
                elif sekunda < 0 or sekunda > 59:
                    messagebox.showerror("Greška", "Ponovo unesite sekund!")
                    return None
                return str(datetime.datetime(godina, mesec, dan, sat, minut, sekunda))

            def ogranicenje_pol(self):
                pol = self.__pol_combobox.get()
                if pol == "":
                    messagebox.showerror("Greška", "Izaberite pol!")
                    return None
                return pol

            def ogranicenje_licne_karte(self):
                brojLicneKarte = self.__broj_licne_karte_entry.get()
                if len(brojLicneKarte) != 10:
                    messagebox.showerror("Greška", "Izaberite broj licne karte!")
                    return None
                return brojLicneKarte

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Dodavanje")
                self.minsize(400, 200)

                dodavanje_frame = Frame(self, padx=5, pady=5)
                dodavanje_frame.pack(expand=1)

                Label(dodavanje_frame, text="JMBG:").grid(row=0, sticky=E)
                self.__jmbg = StringVar(root)
                self.__jmbg_entry = Entry(dodavanje_frame, width=20, textvariable=self.__jmbg)
                self.__jmbg_entry.grid(row=0, column=1, sticky=W)

                Label(dodavanje_frame, text="Ime:").grid(row=1, sticky=E)
                self.__ime = StringVar(root)
                self.__ime_entry = Entry(dodavanje_frame, width=20, textvariable=self.__ime)
                self.__ime_entry.grid(row=1, column=1, sticky=W)

                Label(dodavanje_frame, text="Prezime:").grid(row=2, sticky=E)
                self.__prezime = StringVar(root)
                self.__prezime_entry = Entry(dodavanje_frame, width=20, textvariable=self.__prezime)
                self.__prezime_entry.grid(row=2, column=1, sticky=W)

                Label(dodavanje_frame, text="Datum rodjenja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=1900, increment=1, to=2022,
                                                textvariable=self.__vreme1)
                self.__godina_spinbox.grid(row=0, column=0, sticky=W)
                self.__vreme2 = IntVar(root)
                self.__mesec_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=12,
                                               textvariable=self.__vreme2)
                self.__mesec_spinbox.grid(row=0, column=1, sticky=W)
                self.__vreme3 = IntVar(root)
                self.__dan_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=31,
                                             textvariable=self.__vreme3)
                self.__dan_spinbox.grid(row=0, column=2, sticky=W)
                self.__vreme4 = IntVar(root)
                self.__sat_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=24,
                                             textvariable=self.__vreme4)
                self.__sat_spinbox.grid(row=0, column=3, sticky=W)
                self.__vreme5 = IntVar(root)
                self.__minut_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                               textvariable=self.__vreme5)
                self.__minut_spinbox.grid(row=0, column=4, sticky=W)
                self.__vreme6 = IntVar(root)
                self.__sekund_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                                textvariable=self.__vreme6)
                self.__sekund_spinbox.grid(row=0, column=5, sticky=W)

                Label(dodavanje_frame, text="Pol:").grid(row=4, sticky=E)
                self.__pol = StringVar(root)
                self.__pol_combobox = Combobox(dodavanje_frame, textvariable=self.__pol)
                self.__pol_combobox.grid(row=4, column=1, sticky=W)
                self.__pol_combobox['values'] = ('Zensko', 'Musko')

                Label(dodavanje_frame, text="Broj licne karte:").grid(row=5, sticky=E)
                self.__broj_licne_karte = StringVar(root)
                self.__broj_licne_karte_entry = Entry(dodavanje_frame, width=20, textvariable=self.__broj_licne_karte)
                self.__broj_licne_karte_entry.grid(row=5, column=1, sticky=W)

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.dodaj, text="Dodaj")
                self.__dodaj_button.grid(row=6, column=1, sticky=W)

        dodavanje_prozor = Dodavanje(self, self.__podaci)
        self.wait_window(dodavanje_prozor)
        if dodavanje_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.gradjani)
        self.__pretraga_entry["text"] = ""

    def __init__(self, root, podaci):
        super().__init__(root)
        self.__podaci = podaci
        self.__otkazano = True

        self.title("Gradjani")
        self.minsize(400, 200)

        gradjanin_frame = Frame(self, padx=5, pady=5)
        gradjanin_frame.pack(expand=1)

        self.__dodaj_button = Button(gradjanin_frame, width=10, command=self.dodavanje, text="Dodaj")
        self.__dodaj_button.grid(row=0, column=1, sticky=W)

        self.__izmena_button = Button(gradjanin_frame, width=10, command=self.indeksiranje1, text="Izmeni")
        self.__izmena_button.grid(row=1, column=1, sticky=W)

        self.__obrisi_button = Button(gradjanin_frame, width=10, command=self.indeksiranje2, text="Obrisi")
        self.__obrisi_button.grid(row=2, column=1, sticky=W)

        self.__pretraga = StringVar(root)
        self.__pretraga.trace_add("write", self.filtriranje_listbox)
        self.__pretraga_entry = Entry(gradjanin_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.grid(row=3, column=1, sticky=W)

        self.__lista_listbox = Listbox(gradjanin_frame, activestyle="none", exportselection=False)
        self.__lista_listbox.grid(row=4, column=1, sticky=W)

        Label(gradjanin_frame, text="JMBG:").grid(row=5, sticky=E)
        self.__labela_jmbg = Label(gradjanin_frame, text="")
        self.__labela_jmbg.grid(row=5, column=1, sticky=W)
        Label(gradjanin_frame, text="Ime:").grid(row=6, sticky=E)
        self.__labela_ime = Label(gradjanin_frame, text="")
        self.__labela_ime.grid(row=6, column=1, sticky=W)
        Label(gradjanin_frame, text="Prezime:").grid(row=7, sticky=E)
        self.__labela_prezime = Label(gradjanin_frame, text="")
        self.__labela_prezime.grid(row=7, column=1, sticky=W)
        Label(gradjanin_frame, text="Datum rodjenja:").grid(row=8, sticky=E)
        self.__labela_datum_rodjenja = Label(gradjanin_frame, text="")
        self.__labela_datum_rodjenja.grid(row=8, column=1, sticky=W)
        Label(gradjanin_frame, text="Pol:").grid(row=9, sticky=E)
        self.__labela_pol = Label(gradjanin_frame, text="")
        self.__labela_pol.grid(row=9, column=1, sticky=W)
        Label(gradjanin_frame, text="Broj licne karte:").grid(row=10, sticky=E)
        self.__labela_broj_licne_karte = Label(gradjanin_frame, text="")
        self.__labela_broj_licne_karte.grid(row=10, column=1, sticky=W)
        Label(gradjanin_frame, text="Lista doza:").grid(row=11, sticky=E)
        self.__labela_lista_doza = Label(gradjanin_frame, text="")
        self.__labela_lista_doza.grid(row=11, column=1, sticky=W)
        Label(gradjanin_frame, text="Lista potvrda:").grid(row=12, sticky=E)
        self.__labela_lista_potvrda = Label(gradjanin_frame, text="")
        self.__labela_lista_potvrda.grid(row=12, column=1, sticky=W)
        Label(gradjanin_frame, text="Sertifikat:").grid(row=13, sticky=E)
        self.__labela_sertifikat = Label(gradjanin_frame, text="")
        self.__labela_sertifikat.grid(row=13, column=1, sticky=W)

        self.popuni_listu(self.__podaci.gradjani)
        self.__lista_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_u_listbox)

        self.transient(root)
        # prozor se ne pojavljuje u taskbar-u, već samo njegov roditelj
        self.focus_force()
        # programski izazvani događaji
        self.grab_set()  # modalni

    def indeksiranje1(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.gradjani:
            if naziv == str(i.ime + " " + i.prezime):
                indeks = self.__podaci.gradjani.index(i)
        self.izmena(indeks)

    def indeksiranje2(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.gradjani:
            if naziv == str(i.ime + " " + i.prezime):
                indeks = self.__podaci.gradjani.index(i)
        odgovor = messagebox.askokcancel("Brisanje gradjanina",
                                         "Brisanjem gradjanina brisete i sve podatke vezane za njega. Da li ste sigurni da zelite da izbrisete gradjanina?",
                                         icon="warning")
        if odgovor:
            self.brisanje(indeks)

    @property
    def otkazano(self):
        return self.__otkazano