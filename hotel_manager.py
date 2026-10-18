import json
import os
from datetime import datetime
from modele import Pokoj, Apartament, Rezerwacja, Klient, BrakWolnychPokoiError

class HotelManager:
    def __init__(self, nazwa: str, plik_danych="dane_hotelu.json"):
        self.nazwa = nazwa
        self.plik_danych = plik_danych
        self._pokoje = []
        self._rezerwacje = []
        self.wczytaj_dane()

    def wczytaj_dane(self):
        if not os.path.exists(self.plik_danych):
            # Domyślne pokoje, jeśli plik nie istnieje
            self._pokoje = [
                Pokoj(101, 2, 200.0),
                Pokoj(102, 1, 150.0),
                Apartament(999, 2, 200.0, ["Jacuzzi", "Szampan"])
            ]
            self.zapisz_dane()
            return

        with open(self.plik_danych, "r", encoding="utf-8") as f:
            dane = json.load(f)
            
            # Wczytywanie pokoi
            for p in dane.get("pokoje", []):
                if p["typ"] == "Apartament":
                    self._pokoje.append(Apartament(p["numer"], p["pojemnosc"], p["cena"], p["udogodnienia"]))
                else:
                    self._pokoje.append(Pokoj(p["numer"], p["pojemnosc"], p["cena"]))

            # Wczytywanie rezerwacji
            for r in dane.get("rezerwacje", []):
                klient = Klient(r["klient"]["imie"], r["klient"]["nazwisko"])
                data_od = datetime.strptime(r["data_od"], "%Y-%m-%d")
                data_do = datetime.strptime(r["data_do"], "%Y-%m-%d")
                pokoj = next((pok for pok in self._pokoje if pok.numer == r["numer_pokoju"]), None)
                if pokoj:
                    self._rezerwacje.append(Rezerwacja(klient, pokoj, data_od, data_do))

    def zapisz_dane(self):
        dane = {
            "pokoje": [p.to_dict() for p in self._pokoje],
            "rezerwacje": [r.to_dict() for r in self._rezerwacje]
        }
        with open(self.plik_danych, "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=4)

    def _czy_pokoj_dostepny(self, pokoj: Pokoj, data_od: datetime, data_do: datetime) -> bool:
        for rez in self._rezerwacje:
            if rez.pokoj.numer == pokoj.numer:
                if max(data_od, rez.data_od) < min(data_do, rez.data_do):
                    return False
        return True

    def utworz_rezerwacje(self, imie: str, nazwisko: str, data_od_str: str, data_do_str: str, pojemnosc: int):
        data_od = datetime.strptime(data_od_str, "%Y-%m-%d")
        data_do = datetime.strptime(data_do_str, "%Y-%m-%d")
        
        if data_do <= data_od:
            raise ValueError("Data wyjazdu musi być późniejsza!")

        for pokoj in self._pokoje:
            if pokoj.pojemnosc >= pojemnosc and self._czy_pokoj_dostepny(pokoj, data_od, data_do):
                klient = Klient(imie, nazwisko)
                nowa_rez = Rezerwacja(klient, pokoj, data_od, data_do)
                self._rezerwacje.append(nowa_rez)
                self.zapisz_dane()
                return nowa_rez

        raise BrakWolnychPokoiError(f"Brak wolnych pokoi {pojemnosc}-osobowych.")

    def generuj_raport_przychodu(self):
        suma = sum(rez.oblicz_koszt_calkowity() for rez in self._rezerwacje)
        print(f"\n=== RAPORT FINANSOWY HOTELU '{self.nazwa}' ===")
        print(f"Liczba rezerwacji w systemie: {len(self._rezerwacje)}")
        print(f"Przewidywany przychód: {suma:.2f} PLN")
        print("================================================\n")