from datetime import datetime

class BrakWolnychPokoiError(Exception):
    pass

class Klient:
    def __init__(self, imie, nazwisko):
        self.imie = imie
        self.nazwisko = nazwisko

    # Getter
    @property
    def imie(self):
        return self._imie

    @imie.setter
    def imie(self, wartosc):
        if not wartosc.strip():
            raise ValueError("Imię nie może być puste!")
        self._imie = wartosc.capitalize()

    @property
    def nazwisko(self):
        return self._nazwisko

    @nazwisko.setter
    def nazwisko(self, wartosc):
        if not wartosc.strip():
            raise ValueError("Nazwisko nie może być puste!")
        self._nazwisko = wartosc.capitalize()

# klasa bazowa
class Pokoj:
    def __init__(self, numer, pojemnosc, cena_podstawowa):
        self.numer = numer
        self.pojemnosc = pojemnosc  
        self.cena_podstawowa = cena_podstawowa

    # Enkapsulacja pojemności
    @property
    def pojemnosc(self):
        return self._pojemnosc

    @pojemnosc.setter
    def pojemnosc(self, wartosc):
        if wartosc <= 0:
            raise ValueError("Pojemność pokoju musi być większa od zera.")
        self._pojemnosc = wartosc

    # Enkapsulacja ceny
    @property
    def cena_podstawowa(self):
        return self._cena_podstawowa

    @cena_podstawowa.setter
    def cena_podstawowa(self, nowa_cena):
        if nowa_cena < 0:
            raise ValueError("Cena podstawowa nie może być ujemna.")
        self._cena_podstawowa = nowa_cena

    def oblicz_cene_za_dobe(self):
        return self.cena_podstawowa

    def to_dict(self):
        return {"typ": "Pokoj", "numer": self.numer, "pojemnosc": self.pojemnosc, "cena": self.cena_podstawowa}

class Apartament(Pokoj):
    def __init__(self, numer, pojemnosc, cena_podstawowa, udogodnienia):
        super().__init__(numer, pojemnosc, cena_podstawowa)
        self.udogodnienia = udogodnienia

    def oblicz_cene_za_dobe(self):
        mnoznik_luksusu = 1.3
        oplata_serwisowa = 100.0

        return (self.cena_podstawowa * mnoznik_luksusu) + oplata_serwisowa

    def to_dict(self):
        return {"typ": "Apartament", "numer": self.numer, "pojemnosc": self.pojemnosc, 
                "cena": self.cena_podstawowa, "udogodnienia": self.udogodnienia}

class Rezerwacja:
    def __init__(self, klient: Klient, pokoj: Pokoj, data_od: datetime, data_do: datetime):
        self.klient = klient
        self.pokoj = pokoj
        self.data_od = data_od
        self.data_do = data_do

    def oblicz_koszt_calkowity(self):
        liczba_dni = (self.data_do - self.data_od).days
        return liczba_dni * self.pokoj.oblicz_cene_za_dobe()

    def to_dict(self):
        return {
            "klient": {"imie": self.klient.imie, "nazwisko": self.klient.nazwisko},
            "numer_pokoju": self.pokoj.numer,
            "data_od": self.data_od.strftime("%Y-%m-%d"),
            "data_do": self.data_do.strftime("%Y-%m-%d")
        }