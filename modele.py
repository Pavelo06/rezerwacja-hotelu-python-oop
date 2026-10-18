from datetime import datetime

# Własny wyjątek
class BrakWolnychPokoiError(Exception):
    pass

class Klient:
    def __init__(self, imie: str, nazwisko: str):
        self.imie = imie
        self.nazwisko = nazwisko

# Klasa bazowa
class Pokoj:
    def __init__(self, numer: int, pojemnosc: int, cena_podstawowa: float):
        self.numer = numer
        self.pojemnosc = pojemnosc
        self._cena_podstawowa = cena_podstawowa

    def oblicz_cene_za_dobe(self) -> float:
        return self._cena_podstawowa

    # Zapis
    def to_dict(self):
        return {"typ": "Pokoj", "numer": self.numer, "pojemnosc": self.pojemnosc, "cena": self._cena_podstawowa}

class Apartament(Pokoj):
    def __init__(self, numer: int, pojemnosc: int, cena_podstawowa: float, udogodnienia: list):
        super().__init__(numer, pojemnosc, cena_podstawowa) # Wywołuje konstruktor klasy 'Pokoj'
        self.udogodnienia = udogodnienia

    def oblicz_cene_za_dobe(self) -> float:
        mnoznik_luksusu = 1.3
        oplata_serwisowa = 100.0
        return (self._cena_podstawowa * mnoznik_luksusu) + oplata_serwisowa

    def to_dict(self):
        return {"typ": "Apartament", "numer": self.numer, "pojemnosc": self.pojemnosc, 
                "cena": self._cena_podstawowa, "udogodnienia": self.udogodnienia}

class Rezerwacja:
    def __init__(self, klient: Klient, pokoj: Pokoj, data_od: datetime, data_do: datetime):
        self.klient = klient
        self.pokoj = pokoj
        self.data_od = data_od
        self.data_do = data_do

    def oblicz_koszt_calkowity(self) -> float:
        liczba_dni = (self.data_do - self.data_od).days
        return liczba_dni * self.pokoj.oblicz_cene_za_dobe()

    def to_dict(self):
        return {
            "klient": {"imie": self.klient.imie, "nazwisko": self.klient.nazwisko},
            "numer_pokoju": self.pokoj.numer,
            "data_od": self.data_od.strftime("%Y-%m-%d"),
            "data_do": self.data_do.strftime("%Y-%m-%d")
        }