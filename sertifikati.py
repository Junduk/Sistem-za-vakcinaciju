from tkinter import *
from tkinter import messagebox
from vakcinisanje import *
from tkinter.ttk import Combobox
import datetime
from datetime import date


class PristupSertifikatima(Toplevel):

    def sortiranjeSertifikata(self):
        for i in range(len(self.__podaci.sertifikati)):
            for j in range(0, len(self.__podaci.sertifikati) - i - 1):
                if self.__podaci.sertifikati[j].datum.upper() > self.__podaci.sertifikati[j + 1].datum.upper():
                    temp = self.__podaci.sertifikati[j]
                    self.__podaci.sertifikati[j] = self.__podaci.sertifikati[j + 1]
                    self.__podaci.sertifikati[j + 1] = temp

    def popuni_listu(self, sertifikat):
        self.__lista_listbox.delete(0, END)
        self.sortiranjeSertifikata()
        for sertifikati in sertifikat:
            self.__lista_listbox.insert(END,
                                        "{} {} {}".format(sertifikati.gradjani.ime, sertifikati.gradjani.prezime,
                                                          sertifikati.sifra))
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED

    def popuni_labele(self, sertifikat):
        self.__labela_sifra["text"] = sertifikat.sifra
        self.__labela_datum_izdavanja["text"] = sertifikat.datumtoString
        self.__labela_gradjanin_ime["text"] = sertifikat.gradjani.ime
        self.__labela_gradjanin_prezime["text"] = sertifikat.gradjani.prezime

    def ocisti_labele(self):
        self.__labela_sifra["text"] = ""
        self.__labela_datum_izdavanja["text"] = ""
        self.__labela_gradjanin_ime["text"] = ""
        self.__labela_gradjanin_prezime["text"] = ""

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__lista_listbox.curselection():
            self.ocisti_labele()
            self.__izmena_button['state'] = DISABLED
            self.__obrisi_button['state'] = DISABLED
            return

        indeks = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(indeks)
        sertifikat = 0
        for i in self.__podaci.sertifikati:
            if str(i.gradjani.ime + " " + i.gradjani.prezime + " " + str(i.sifra)) == naziv:
                sertifikat = i
        self.popuni_labele(sertifikat)

        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def filtriranje_listbox(self, var, index, mode):
        self.ocisti_labele()
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED
        self.__lista_listbox.delete(0, END)
        text = self.__pretraga_entry.get()
        for sertifikat in self.__podaci.sertifikati:
            if text.upper() in str(sertifikat.gradjani.ime + " " + sertifikat.gradjani.prezime).upper():
                self.__lista_listbox.insert(END, "{} {} {}".format(sertifikat.gradjani.ime, sertifikat.gradjani.prezime, str(sertifikat.sifra)))

    def brisanje(self, indeks):
        break_bool = FALSE
        for i in self.__podaci.gradjani:
            if break_bool == FALSE:
                if i.jmbg == self.__podaci.sertifikati[indeks].gradjani.jmbg:
                    for k in range(len(i.listaSertifikata)):
                        if i.listaSertifikata[k].sifra == self.__podaci.sertifikati[indeks].sifra:
                            i.listaSertifikata.pop(k)
                            break_bool = TRUE
                            break
            else:
                break
        self.__podaci.sertifikati.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.sertifikati)
        self.__pretraga_entry["text"] = ""
        self.ocisti_labele()

    def izmena(self, indeks, sifraIzmene):

        class Izmena(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def izmeni(self):
                datum = self.ogranicenje_datuma()
                if not datum:
                    return

                gradjanin = self.ogranicenje_gradjanina()
                if not gradjanin:
                    return

                self.__podaci.sertifikati[indeks].datum = datum
                self.__podaci.sertifikati[indeks].gradjani = gradjanin

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_datuma(self):
                danas = date.today().strftime("%d/%m/%Y").split("/")
                danasdan = int(danas[0])
                danasmesec = int(danas[1])
                danasgodina = int(danas[2])
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina > danasgodina:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif godina == danasgodina:
                    if mesec > danasmesec:
                        messagebox.showerror("Greška", "Ponovo unesite mesec!")
                        return None
                    elif mesec == danasmesec:
                        if dan > danasdan:
                            messagebox.showerror("Greška", "Ponovo unesite dan!")
                            return None
                        else:
                            if mesec < 1 or mesec > 12:
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
                    else:
                        if mesec < 1 or mesec > 12:
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

            def ogranicenje_gradjanina(self):
                gradjanin = self.__gradjanin_combobox.get()
                if gradjanin == "":
                    messagebox.showerror("Greška", "Izaberite gradjanina!")
                    return None
                for i in self.__podaci.gradjani:
                    if gradjanin == i.ime + " " + i.prezime + " " + i.jmbg:
                        return i

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Izmena")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                dodavanje_frame = Frame(self, padx=5, pady=5)
                dodavanje_frame.pack(expand=1)

                Label(dodavanje_frame, text="Sifra:").grid(row=0, sticky=E)
                self.__sifra = StringVar(root)
                self.__sifra_entry = Entry(dodavanje_frame, width=20, textvariable=self.__sifra)
                self.__sifra_entry.grid(row=0, column=1, sticky=W)
                self.__sifra_entry.delete(0, END)
                self.__sifra_entry.insert(0, self.__podaci.sertifikati[indeks].sifra)
                self.__sifra_entry.config(state="disabled")

                Label(dodavanje_frame, text="Datum izdavanja:").grid(row=1, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=1, column=1, sticky=W)
                pomoc = str(datetime.datetime.strptime(self.__podaci.sertifikati[indeks].datum, "%Y-%m-%d %H:%M:%S") \
                            .strftime("%d/%m/%Y/%H/%M/%S")).split("/")

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=2016, increment=1, to=3000,
                                                textvariable=self.__vreme1)
                self.__godina_spinbox.grid(row=0, column=0, sticky=W)
                self.__godina_spinbox.delete(0, END)
                self.__godina_spinbox.insert(0, pomoc[2])
                self.__vreme2 = IntVar(root)
                self.__mesec_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=12,
                                               textvariable=self.__vreme2)
                self.__mesec_spinbox.grid(row=0, column=1, sticky=W)
                self.__mesec_spinbox.delete(0, END)
                self.__mesec_spinbox.insert(0, pomoc[1])
                self.__vreme3 = IntVar(root)
                self.__dan_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=31,
                                             textvariable=self.__vreme3)
                self.__dan_spinbox.grid(row=0, column=2, sticky=W)
                self.__dan_spinbox.delete(0, END)
                self.__dan_spinbox.insert(0, pomoc[0])
                self.__vreme4 = IntVar(root)
                self.__sat_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=24,
                                             textvariable=self.__vreme4)
                self.__sat_spinbox.grid(row=0, column=3, sticky=W)
                self.__sat_spinbox.delete(0, END)
                self.__sat_spinbox.insert(0, pomoc[3])
                self.__vreme5 = IntVar(root)
                self.__minut_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                               textvariable=self.__vreme5)
                self.__minut_spinbox.grid(row=0, column=4, sticky=W)
                self.__minut_spinbox.delete(0, END)
                self.__minut_spinbox.insert(0, pomoc[4])
                self.__vreme6 = IntVar(root)
                self.__sekund_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                                textvariable=self.__vreme6)
                self.__sekund_spinbox.grid(row=0, column=5, sticky=W)
                self.__sekund_spinbox.delete(0, END)
                self.__sekund_spinbox.insert(0, pomoc[5])

                Label(dodavanje_frame, text="Gradjanin:").grid(row=2, sticky=E)
                self.__gradjanin = StringVar(root)
                self.__gradjanin_combobox = Combobox(dodavanje_frame, textvariable=self.__gradjanin, width=35)
                self.__gradjanin_combobox.grid(row=2, column=1, sticky=W)
                self.__gradjanin_combobox.delete(0, END)
                self.__gradjanin_combobox.insert(0, self.__podaci.sertifikati[indeks].gradjani.ime + " "
                                                 + self.__podaci.sertifikati[indeks].gradjani.prezime + " "
                                                 + self.__podaci.sertifikati[indeks].gradjani.jmbg)
                niz2 = []
                for i in self.__podaci.gradjani:
                    niz2.append(i.ime + " " + i.prezime + " " + i.jmbg)
                self.__gradjanin_combobox['values'] = niz2

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.izmeni, text="Izmeni")
                self.__dodaj_button.grid(row=3, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=4, column=1, sticky=W)

        izmena_prozor = Izmena(self, self.__podaci)
        self.wait_window(izmena_prozor)
        if izmena_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.sertifikati)
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        self.__pretraga_entry["text"] = ""
        for x in self.__podaci.sertifikati:
            if x.sifra == sifraIzmene:
                i = self.__podaci.sertifikati.index(x)
                self.__lista_listbox.select_set(i)
                self.popuni_labele(self.__podaci.sertifikati[i])

    def dodavanje(self):

        class Dodavanje(Toplevel):
            sifraIzmene = 0
            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def dodaj(self):
                sifra = self.ogranicenje_sifre()
                global sifraIzmene
                sifraIzmene = sifra
                if not sifra:
                    return

                datum = self.ogranicenje_datuma()
                if not datum:
                    return

                gradjanin = self.ogranicenje_gradjanina()
                if not gradjanin:
                    return

                sertifikat = Sertifikat(sifra, datum, gradjanin)
                self.__podaci.sertifikati.append(sertifikat)
                for i in self.__podaci.gradjani:
                    if i.jmbg == gradjanin.jmbg:
                        i.listaSertifikata.append(sertifikat)

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_sifre(self):
                sifra = self.__sifra_entry.get()
                if len(sifra) != 8:
                    messagebox.showerror("Greška", "Sifra mora sadrzati 8 karaktera!")
                    return None
                for i in self.__podaci.sertifikati:
                    if i.sifra == sifra:
                        messagebox.showerror("Greška", "U sistemu vec postoji sertifikat sa ovom sifrom!")
                        return None
                return sifra

            def ogranicenje_datuma(self):
                danas = date.today().strftime("%d/%m/%Y").split("/")
                danasdan = int(danas[0])
                danasmesec = int(danas[1])
                danasgodina = int(danas[2])
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina > danasgodina:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif godina == danasgodina:
                    if mesec > danasmesec:
                        messagebox.showerror("Greška", "Ponovo unesite mesec!")
                        return None
                    elif mesec == danasmesec:
                        if dan > danasdan:
                            messagebox.showerror("Greška", "Ponovo unesite dan!")
                            return None
                        else:
                            if mesec < 1 or mesec > 12:
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
                    else:
                        if mesec < 1 or mesec > 12:
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

            def ogranicenje_gradjanina(self):
                gradjanin = self.__gradjanin_combobox.get()
                if gradjanin == "":
                    messagebox.showerror("Greška", "Izaberite gradjanina!")
                    return None
                for i in self.__podaci.gradjani:
                    if gradjanin == i.ime + " " + i.prezime + " " + i.jmbg:
                        return i

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Dodavanje")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                dodavanje_frame = Frame(self, padx=5, pady=5)
                dodavanje_frame.pack(expand=1)

                Label(dodavanje_frame, text="Sifra:").grid(row=0, sticky=E)
                self.__sifra = StringVar(root)
                self.__sifra_entry = Entry(dodavanje_frame, width=20, textvariable=self.__sifra)
                self.__sifra_entry.grid(row=0, column=1, sticky=W)

                Label(dodavanje_frame, text="Datum izdavanja:").grid(row=1, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=1, column=1, sticky=W)

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=2016, increment=1, to=3000,
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

                Label(dodavanje_frame, text="Gradjanin:").grid(row=2, sticky=E)
                self.__gradjanin = StringVar(root)
                self.__gradjanin_combobox = Combobox(dodavanje_frame, textvariable=self.__gradjanin, width=35)
                self.__gradjanin_combobox.grid(row=2, column=1, sticky=W)
                niz2 = []
                for i in self.__podaci.gradjani:
                    niz2.append(i.ime + " " + i.prezime + " " + i.jmbg)
                self.__gradjanin_combobox['values'] = niz2

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.dodaj, text="Dodaj")
                self.__dodaj_button.grid(row=3, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=4, column=1, sticky=W)

        dodavanje_prozor = Dodavanje(self, self.__podaci)
        self.wait_window(dodavanje_prozor)
        if dodavanje_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.sertifikati)
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        self.__pretraga_entry["text"] = ""
        global sifraIzmene
        for x in self.__podaci.sertifikati:
            if x.sifra == sifraIzmene:
                i = self.__podaci.sertifikati.index(x)
                self.__lista_listbox.select_set(i)
                self.popuni_labele(self.__podaci.sertifikati[i])

    def __init__(self, root, podaci):
        super().__init__(root)
        self.__podaci = podaci
        self.__otkazano = True

        self.title("Digitalni sertifikati")
        self.minsize(400, 200)
        self.geometry('+350+100')
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        sertifikati_frame = Frame(self, padx=5, pady=5)
        sertifikati_frame.pack(expand=1)

        self.__dodaj_button = Button(sertifikati_frame, width=10, command=self.indeksiranje, text="Dodaj")
        self.__dodaj_button.grid(row=0, column=1, sticky=W)

        self.__izmena_button = Button(sertifikati_frame, width=10, command=self.indeksiranje1, text="Izmeni")
        self.__izmena_button.grid(row=1, column=1, sticky=W)

        self.__obrisi_button = Button(sertifikati_frame, width=10, command=self.indeksiranje2, text="Obrisi")
        self.__obrisi_button.grid(row=2, column=1, sticky=W)

        self.__pretraga = StringVar(root)
        self.__pretraga.trace_add("write", self.filtriranje_listbox)
        self.__pretraga_entry = Entry(sertifikati_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.grid(row=3, column=1, sticky=W)

        self.__lista_listbox = Listbox(sertifikati_frame, activestyle="none", exportselection=False, width=35)
        self.__lista_listbox.grid(row=4, column=1, sticky=W)

        Label(sertifikati_frame, text="Sifra:").grid(row=5, sticky=E)
        self.__labela_sifra = Label(sertifikati_frame, text="")
        self.__labela_sifra.grid(row=5, column=1, sticky=W)
        Label(sertifikati_frame, text="Datum izdavanja sertifikata:").grid(row=6, sticky=E)
        self.__labela_datum_izdavanja = Label(sertifikati_frame, text="")
        self.__labela_datum_izdavanja.grid(row=6, column=1, sticky=W)
        Label(sertifikati_frame, text="Ime gradjanina:").grid(row=7, sticky=E)
        self.__labela_gradjanin_ime = Label(sertifikati_frame, text="")
        self.__labela_gradjanin_ime.grid(row=7, column=1, sticky=W)
        Label(sertifikati_frame, text="Prezime gradjanina:").grid(row=8, sticky=E)
        self.__labela_gradjanin_prezime = Label(sertifikati_frame, text="")
        self.__labela_gradjanin_prezime.grid(row=8, column=1, sticky=W)

        self.popuni_listu(self.__podaci.sertifikati)
        self.__lista_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_u_listbox)

        self.transient(root)
        # prozor se ne pojavljuje u taskbar-u, već samo njegov roditelj
        self.focus_force()
        # programski izazvani događaji
        self.grab_set()  # modalni

    def indeksiranje(self):
        if len(self.__podaci.gradjani) == 0:
            messagebox.showerror("Greška", "Dodajte gradjanina u sistem!")
            return None
        else:
            self.dodavanje()

    def indeksiranje1(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.sertifikati:
            if naziv == str(i.gradjani.ime + " " + i.gradjani.prezime + " " + str(i.sifra)):
                indeks = self.__podaci.sertifikati.index(i)
        self.izmena(indeks, self.__podaci.sertifikati[indeks].sifra)

    def indeksiranje2(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.sertifikati:
            if naziv == str(i.gradjani.ime + " " + i.gradjani.prezime + " " + str(i.sifra)):
                indeks = self.__podaci.sertifikati.index(i)
        odgovor = messagebox.askokcancel("Brisanje sertifikata",
                                         "Brisanjem sertifikata brisete i sve podatke vezane za njega. Da li ste sigurni da zelite da izbrisete sertifikat?",
                                         icon="warning")
        if odgovor:
            self.brisanje(indeks)

    @property
    def otkazano(self):
        return self.__otkazano