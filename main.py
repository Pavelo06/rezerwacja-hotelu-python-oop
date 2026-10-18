from hotel_manager import HotelManager
from modele import BrakWolnychPokoiError

def start():
    hotel = HotelManager("Hotel")

    while True:
        print(f"\nWitaj w systemie {hotel.nazwa}!")
        print("1. Zaloguj jako Klient")
        print("2. Zaloguj jako Obsługa Hotelu")
        print("3. Wyjście")
        
        wybor = input("Wybierz opcję (1-3): ")

        if wybor == '1':
            print("\n--- NOWA REZERWACJA ---")
            imie = input("Podaj imię: ")
            nazwisko = input("Podaj nazwisko: ")
            osoby = int(input("Dla ilu osób potrzebujesz pokoju?: "))
            data_od = input("Data przyjazdu (YYYY-MM-DD): ")
            data_do = input("Data wyjazdu (YYYY-MM-DD): ")

            try:
                rezerwacja = hotel.utworz_rezerwacje(imie, nazwisko, data_od, data_do, osoby)
                print(f"\nSUKCES! Zarezerwowano pokój nr {rezerwacja.pokoj.numer}.")
                print(f"Kwota do zapłaty przy zameldowaniu: {rezerwacja.oblicz_koszt_calkowity():.2f} PLN")
            
            except ValueError as e:
                print(f"BŁĄD DANYCH: Upewnij się, że wpisujesz datę w formacie YYYY-MM-DD (np. 2024-05-10).")
            except BrakWolnychPokoiError as e:
                print(f"ODRZUCONO: {e}")

        elif wybor == '2':
            hotel.generuj_raport_przychodu()

        elif wybor == '3':
            print("Zamykanie systemu. Dowidzenia!")
            break
        else:
            print("Nieznana opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    start()