
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import sys
import random

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

    def szobak_listaja(self):
        print("Szobák listája:")
        for szoba in self.szobak:
            print(f"Szobaszám: {szoba.szobaszam}, Ár: {szoba.ar} Ft/éj")

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class SzobaFoglalasRendszer:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = []


    def foglalas(self, szobaszam, datum):
        szoba = next((sz for sz in self.szalloda.szobak if sz.szobaszam == szobaszam), None)
        if any(f.szoba == szoba and f.datum == datum for f in self.foglalasok):
            return "Ez a szoba már foglalt ezen a napon.\nKérjük válasszon egy másik szobát!\n"

        if datum < datetime.now().date():
            return "Kérjük az aktuális vagy jővőbeli napot válasszon a foglalásra!\n"
        
        self.foglalasok.append(Foglalas(szoba, datum))
        return f"\nKöszönjük a foglalását!\nA foglalás részletei:\nIdőpont: {datum}   Ár: {szoba.ar} Ft\nVárjuk szeretettel!"
    

    def foglalas_lemondas(self, szobaszam, datum):
        foglalas = next((f for f in self.foglalasok if f.szoba.szobaszam == szobaszam and f.datum == datum), None)
        if not foglalas:
            return "Nincs ilyen foglalás."

        self.foglalasok.remove(foglalas)
        return f"\nFoglalás sikeresen lemondva.\nLemondott foglalási információk: \nSzobaszám: {szobaszam}, Dátum: {datum.strftime('%Y-%m-%d')}"


    def foglalasok_listaja(self):
        return '\n'.join(f"Szobaszám: {f.szoba.szobaszam}, Dátum: {f.datum}" for f in self.foglalasok)
    

szalloda = Szalloda("Hunor Hotel")
szalloda.szoba_hozzaad(EgyagyasSzoba(101, 50000))
szalloda.szoba_hozzaad(EgyagyasSzoba(103, 55000))
szalloda.szoba_hozzaad(EgyagyasSzoba(105, 55000))
szalloda.szoba_hozzaad(KetagyasSzoba(102, 85000))
szalloda.szoba_hozzaad(KetagyasSzoba(104, 85000))
szalloda.szoba_hozzaad(KetagyasSzoba(106, 90000))
szalloda.szoba_hozzaad(KetagyasSzoba(201, 120000))

rendszer = SzobaFoglalasRendszer(szalloda)

today = datetime.now().date()
num_days = 10 
num_bookings = 15

for _ in range(num_bookings):
    random_room = random.choice(szalloda.szobak) 
    random_day = random.randint(0, num_days)
    rendszer.foglalas(random_room.szobaszam, today + timedelta(days=random_day))


def user_interface():
    print("\nÜdvözöljük a Hunor Hotel szobafoglaló rendszerben!")
    
    while True:
        print("\nVálasszon az alábbi opciók közül:")
        print("1. Szoba foglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Szobák listázása")
        print("0. Kilépésés a foglaló rendszerből\n")
        choice = input("Kérem adja meg a kívánt opció számát: ")
        if choice == "1":
            while True:
                szobaszam = int(input("Adjon meg egy szobaszámot: "))
                szoba = next((sz for sz in rendszer.szalloda.szobak if sz.szobaszam == szobaszam), None)
                if szoba is None:
                    print("Nincs ilyen szoba a szállodában.")
                    rendszer.szalloda.szobak_listaja()
                else:
                    break 
            while True:
                datum_str = input("Adja meg a dátumot (éééé-hh-nn formátumban): ")
                try:
                    datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                    if datum < datetime.now().date():
                        raise ValueError("Kérjük az aktuális vagy jővőbeli napot válasszon a foglalásra!")
                    break
                except ValueError as e:
                    print(str(e))
            if choice == "1":
                print(rendszer.foglalas(szobaszam, datum))


        elif choice == "2":
                print(rendszer.foglalas_lemondas(szobaszam, datum))


        elif choice == "3":
            print("Foglalások listája:")
            print(rendszer.foglalasok_listaja())


        elif choice == "4":
            rendszer.szalloda.szobak_listaja()


        elif choice == "0":
            print("Köszönjük, hogy használta a rendszerünket. Viszont látásra!")
            break
        else:
            print("Érvénytelen választás, kérem próbálja újra.")


user_interface()
