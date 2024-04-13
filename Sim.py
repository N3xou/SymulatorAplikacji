import cx_Oracle
import random
import string
from datetime import datetime, timedelta

# Ustawienia połączenia z bazą danych Oracle
try:
    dsn_tns = cx_Oracle.makedsn('217.173.198.135', '1521', service_name='tpdb')
    connection = cx_Oracle.connect(user='s102491', password='dnassbaum1!', dsn=dsn_tns)

    print("Polaczono z SQLDeveloper :)")
except:
    print("Cos poszlo nie tak... :(")

cursor = connection.cursor()

def get_klient_ids(cursor):
    cursor.execute("SELECT klientid FROM klient")
    klient_ids = [row[0] for row in cursor.fetchall()]
    return klient_ids
def get_kategorie(cursor):
    # is this not equal ??
    cursor.execute("Select kategoriaid from kategoria_modelu")
    kategorie = [row[0] for row in cursor.fetchall()]
    return kategorie
def get_zamowienia(cursor):
    cursor.execute("Select zamowienieid from zamowienie")
    zamowienia = [row[0] for row in cursor.fetchall()]
    return zamowienia

def get_model_ids(cursor):
    cursor.execute("SELECT modelid FROM model_samolotu")
    model_ids = [row[0] for row in cursor.fetchall()]
    return model_ids
def InsertRandomKlient(howMany, cursor):
    names = ['Adam', 'Barbara', 'Celina', 'Dariusz', 'Ewa', 'Filip', 'Gabriela', 'Henryk', 'Izabela', 'Jan']
    surnames = ['Kowalski', 'Nowak', 'Mazur', 'Wójcik', 'Krawczyk', 'Lewandowski', 'Piotrowski', 'Szymański', 'Woźniak']
    email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com']
    registrationDate = datetime.now().strftime('%Y-%m-%d')

    cursor.execute("SELECT klientid FROM klient ")
    rows = cursor.fetchall()

    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        Imie = random.choice(names)
        Nazwisko = random.choice(surnames)
        num = random.randint(1, 5000)
        email = f"{Imie.lower()}.{Nazwisko.lower()}{num}@{random.choice(email_domains)}"
        phone = ''.join(random.choices('0123456789', k=9))
        cursor.execute(
            """
            INSERT INTO Klient 
            (klientid, imie, nazwisko,email,numer_telefonu,data_rejestracji) 
            VALUES 
            (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'))
            """,
            (i, Imie, Nazwisko, email, phone, registrationDate))


def InsertRandomAdres(howMany, cursor, klient_ids):
    ulice = ['Krakowska', 'Warszawska', 'Gdańska', 'Poznańska', 'Łódzka', 'Szewska', 'Sienkiewicza', 'Narutowicza',
             'Piłsudskiego', 'Słowackiego']
    miasta = ['Kraków', 'Warszawa', 'Gdańsk', 'Poznań', 'Łódź', 'Wrocław', 'Szczecin', 'Bydgoszcz', 'Katowice',
              'Białystok']
    kod_pocztowy = ['00-001', '01-234', '12-345', '98-765', '54-321', '65-432', '87-654', '32-109', '76-543', '43-210']

    # Check if there are clients in the database
    if not klient_ids:
        print("Cannot add address, there are no clients")
        return

    cursor.execute("SELECT adresid FROM adres")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        ulica = random.choice(ulice)
        miasto = random.choice(miasta)
        kod = random.choice(kod_pocztowy)

        # Ensure the foreign key klient_klientid exists
        klient_klientid = random.choice(klient_ids)

        cursor.execute(
            """
            INSERT INTO adres 
            (adresid, ulica, miasto, kod_pocztowy, klient_klientid) 
            VALUES 
            (:1, :2, :3, :4, :5)
            """,
            (i, ulica, miasto, kod, klient_klientid))

def InsertRandomKategoriaModelu(howMany, cursor):
    nazwy_kategorii = ['Elektryczne', 'Spalinowe', 'Odrzutowe', 'Drewniane', 'Z tworzyw sztucznych', 'Z włókna węglowego', 'Szybowce', 'Szkoleniowe', 'Wojskowe']
    opisy_kategorii = [
        'Samoloty napędzane silnikiem elektrycznym.',
        'Samoloty napędzane silnikiem spalinowym.',
        'Samoloty odrzutowe zasilane turbinami lub silnikami elektrycznymi.',
        'Samoloty wykonane głównie z drewna.',
        'Samoloty wykonane z tworzyw sztucznych, takich jak plastik.',
        'Samoloty wykonane z lekkiego, ale wytrzymałego włókna węglowego.',
        'Samoloty zdolne do lotu bez użycia silnika, wykorzystujące wyłącznie energię termiczną.',
        'Samoloty przeznaczone głównie do szkolenia pilotów.',
        'Samoloty wojskowe, takie jak myśliwce, bombowce, i inne, wykorzystywane w celach militarystycznych.'
    ]

    cursor.execute("SELECT kategoriaid FROM kategoria_modelu")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        nazwa_kategorii = random.choice(nazwy_kategorii)
        opis_kategorii = random.choice(opisy_kategorii)

        cursor.execute(
            """
            INSERT INTO kategoria_modelu 
            (kategoriaid, nazwa_kategorii, opis_kategorii) 
            VALUES 
            (:1, :2, :3)
            """,
            (i, nazwa_kategorii, opis_kategorii))
def InsertRandomKodRabatowy(howMany, cursor):

    Status = ['True', 'False']
    start_date = datetime.now() + timedelta(days=3)
    end_date = datetime.now() + timedelta(weeks=2)
    def generate_random_code():
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return letters + numbers

    cursor.execute("SELECT kodrabatowyid FROM kodrabatowy")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        wartosc_rabatu =  random.randint(5,100)
        data_waznosci = random.choice([start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(howMany)])
        status = random.choice(Status)
        kod = generate_random_code()
        cursor.execute(
            """
            INSERT INTO kodrabatowy 
            (kodrabatowyid,wartosc_rabatu, data_waznosci,status_aktywny,kod) 
            VALUES 
            (:1, :2, :3, :4, :5)
            """,
            (i, wartosc_rabatu, data_waznosci, status, kod))
def InsertRandomModelSamolotu(howMany, cursor, kategorie):
    if not kategorie:
        print("Cannot add model address, create a category first")
        return

    def generate_random_model_name():
        prefixes = ['Boeing', 'Airbus', 'Embraer', 'Bombardier']
        suffixes = ['300', '400', '500', '600']
        return random.choice(prefixes) + ' ' + random.choice(suffixes)


    cursor.execute("SELECT modelid FROM model_samolotu")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        nazwa_modelu = generate_random_model_name()
        cena = round(random.uniform(10000, 200000), 2)
        ilosc_w_magazynie = random.randint(1, 100)
        kategoria_modelu = random.choice(kategorie)

        cursor.execute(
            """
            INSERT INTO model_samolotu 
            (modelid, nazwa_modelu, cena, ilosc_w_magazynie, kategoria_modelu_kategoriaid) 
            VALUES 
            (:1, :2, :3, :4, :5)
            """,
            (i, nazwa_modelu, cena, ilosc_w_magazynie, kategoria_modelu))

def InsertRandomZamowienie(howMany, cursor, klient_ids):
    if not klient_ids:
        print("Cannot add orders, create clients first")
        return

    statuses = ['Processing', 'Shipped', 'Delivered', 'Cancelled']
    payment_statuses = ['Pending', 'Paid', 'Failed']
    metody_platnosci = ['Credit Card', 'PayPal', 'Bank Transfer']
    cursor.execute("SELECT zamowienieid FROM zamowienie")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        data_zamowienia = datetime.now() - timedelta(days=random.randint(1, 30))
        status_zamowienia = random.choice(statuses)
        status_platnosci = random.choice(payment_statuses)
        kwota_zamowienia = round(random.uniform(10, 5000), 2)
        metoda_platnosci = random.choice(metody_platnosci)
        klientid = random.choice(klient_ids)

        cursor.execute(
            """
            INSERT INTO zamowienie 
            (zamowienieid, data_zamowienia, status_zamowienia, status_platnosci, kwota_zamowienia,
             metoda_platnosci, klientid) 
            VALUES 
            (:1, :2, :3, :4, :5, :6, :7)
            """,
            (i + 1, data_zamowienia, status_zamowienia, status_platnosci, kwota_zamowienia,
             metoda_platnosci, klientid))

def InsertRandomZamowienieProdukt(howMany, cursor, zamowienie_ids, produkt_ids):
    if not zamowienie_ids:
        print("Cannot add order products, create orders first")
        return
    if not produkt_ids:
        print("Cannot add order products, create products first")
        return

    cursor.execute("SELECT zamowienieproduktid FROM zamowienieprodukt")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        zamowienieid = random.choice(zamowienie_ids)
        produktid = random.choice(produkt_ids)
        ilosc = random.randint(1, 10)

        cursor.execute(
            """
            INSERT INTO zamowienieprodukt 
            (zamowienieproduktid, zamowienieid, produktid, ilosc) 
            VALUES 
            (:1, :2, :3, :4)
            """,
            (i + 1, zamowienieid, produktid, ilosc))

def InsertRandomPrzesylka(howMany, cursor, zamowienie_ids):
    if not zamowienie_ids:
        print("Cannot add shipments, create orders first")
        return

    statuses = ['Processing', 'Shipped', 'Delivered', 'Cancelled']

    cursor.execute("SELECT przesylkaid FROM przesylka")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        data_wysylki = datetime.now() - timedelta(days=random.randint(1, 30))
        status_przesylki = random.choice(statuses)
        zamowienieid = random.choice(zamowienie_ids)

        cursor.execute(
            """
            INSERT INTO przesylka 
            (przesylkaid, data_wysylki, status_przesylki, zamowienieid) 
            VALUES 
            (:1, :2, :3, :4)
            """,
            (i + 1, data_wysylki, status_przesylki, zamowienieid))

def InsertRandomRecenzja(howMany, cursor, produkt_ids, klient_ids):
    if not produkt_ids:
        print("Cannot add reviews, create products first")
        return
    if not klient_ids:
        print("Cannot add reviews, create clients first")
        return

    cursor.execute("SELECT recenzjaid FROM recenzja")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        ocena = random.randint(1, 5)
        komentarz = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        data_dodania = datetime.now() - timedelta(days=random.randint(1, 30))
        produktid = random.choice(produkt_ids)
        klientid = random.choice(klient_ids)

        cursor.execute(
            """
            INSERT INTO recenzja 
            (recenzjaid, ocena, komentarz, data_dodania, produktid, klientid) 
            VALUES 
            (:1, :2, :3, :4, :5, :6)
            """,
            (i + 1, ocena, komentarz, data_dodania, produktid, klientid))
def InsertRandomReklamacje(howMany, cursor, klient_ids):
    if not klient_ids:
        print("Cannot add complaints, create clients first")
        return

    statuses = ['Pending', 'In Progress', 'Resolved', 'Cancelled']
    resolutions = ['Replacement', 'Refund', 'Compensation', 'Apology']

    cursor.execute("SELECT reklamacjaid FROM reklamacje")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        data_zlozenia = datetime.now() - timedelta(days=random.randint(1, 30))
        status_reklamacji = random.choice(statuses)
        rozpatrzenie = random.choice(resolutions)
        klient_klientid = random.choice(klient_ids)

        cursor.execute(
            """
            INSERT INTO reklamacje 
            (reklamacjaid, data_zlozenia, status_reklamacji, rozpatrzenie, klient_klientid) 
            VALUES 
            (:1, :2, :3, :4, :5)
            """,
            (i + 1, data_zlozenia, status_reklamacji, rozpatrzenie, klient_klientid))

def InsertRandomKontrolaJakosci(howMany, cursor, produkt_ids):
    if not produkt_ids:
        print("Cannot add quality controls, create products first")
        return

    results = ['Pass', 'Fail', 'Needs Improvement', 'Pending']

    cursor.execute("SELECT kontrolajakosciid FROM kontrolajakosci")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        data_kontroli = datetime.now() - timedelta(days=random.randint(1, 30))
        wynik_kontroli = random.choice(results)
        produktid = random.choice(produkt_ids)

        cursor.execute(
            """
            INSERT INTO kontrolajakosci 
            (kontrolajakosciid, data_kontroli, wynik_kontroli, produktid) 
            VALUES 
            (:1, :2, :3, :4)
            """,
            (i + 1, data_kontroli, wynik_kontroli, produktid))
def InsertRandomFaktura(howMany, cursor, zamowienie_ids):
    if not zamowienie_ids:
        print("Cannot add invoices, create orders first")
        return

    cursor.execute("SELECT fakturaid FROM faktura")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        numer_faktury = random.randint(5, 9999)
        data_wystawienia = datetime.now() - timedelta(days=random.randint(1, 30))
        kwota = round(random.uniform(100, 10000), 2)
        zamowienie_zamowienieid = random.choice(zamowienie_ids)

        cursor.execute(
            """
            INSERT INTO faktura 
            (fakturaid, numer_faktury, data_wystawienia, kwota, zamowienie_zamowienieid) 
            VALUES 
            (:1, :2, :3, :4, :5)
            """,
            (i + 1, numer_faktury, data_wystawienia, kwota, zamowienie_zamowienieid))

#######################################################
howMany = int(input(" 0 - Dodaj rekordy do wszystkich tabel \n" " 1 - Dodaj rekordy do jednej tabeli \n"))

klient_ids = get_klient_ids(cursor)
kategorie = get_kategorie(cursor)
zamowienia = get_zamowienia(cursor)
produkt_ids = get_model_ids(cursor)
if howMany == 0:
    howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać: "))
    InsertRandomKlient(howMany, cursor)
    connection.commit()
    klient_ids = get_klient_ids(cursor)

    InsertRandomAdres(howMany, cursor, klient_ids)

    InsertRandomKodRabatowy(howMany, cursor)

    InsertRandomKategoriaModelu(howMany, cursor)
    connection.commit()
    kategorie = get_kategorie(cursor)
    InsertRandomModelSamolotu(howMany, cursor, kategorie)

    InsertRandomZamowienie(howMany, cursor, klient_ids)
    connection.commit()
    zamowienia = get_zamowienia(cursor)

    InsertRandomZamowienieProdukt(howMany, cursor, zamowienia, klient_ids)
    connection.commit()
    produkt_ids = get_model_ids(cursor)

    InsertRandomPrzesylka(howMany, cursor, zamowienia)

    InsertRandomRecenzja(howMany, cursor, produkt_ids, klient_ids)

    InsertRandomReklamacje(howMany, cursor, klient_ids)

    InsertRandomKontrolaJakosci(howMany, cursor, produkt_ids)

    InsertRandomFaktura(howMany, cursor, zamowienia)

elif howMany == 1:
    howMany = int(input("Wybierz tabelę: \n"
                        "1 - Klient \n"
                        "2 - Adres \n"
                        "3 - Kod rabatowy\n"
                        "4 - Kategoria modelu\n"
                        "5 - Modele samolotow\n"
                        "6 - Zamowienie\n"
                        "7 - Zamowienia products\n"
                        "8 - Przesylka\n"
                        "9 - Recenzja\n"
                        "10 - Reklamacja\n"
                        "11 - Kontrola Jakosci\n"
                        "12 - Faktura\n"))
    if howMany == 1:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomKlient(howMany, cursor)
    elif howMany == 2:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomAdres(howMany, cursor,klient_ids)
    elif howMany == 3:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomKodRabatowy(howMany, cursor)
    elif howMany == 4:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomKategoriaModelu(howMany, cursor)
    elif howMany == 5:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomModelSamolotu(howMany, cursor,kategorie)
    elif howMany == 6:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomZamowienie(howMany,cursor,klient_ids)
    elif howMany == 7:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomZamowienieProdukt(howMany,cursor,zamowienia,klient_ids)
    elif howMany == 8:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomPrzesylka(howMany, cursor, zamowienia)
    elif howMany == 9:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomRecenzja(howMany,cursor,produkt_ids,klient_ids)
    elif howMany == 10:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomReklamacje(howMany, cursor, klient_ids)
    elif howMany == 11:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomKontrolaJakosci(howMany, cursor, produkt_ids)
    elif howMany == 12:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomFaktura(howMany, cursor, zamowienia)
    else:
        print("Nie ma takiej opcji wyboru")
else:
    print("Nie ma takiej opcji wyboru")

connection.commit()
connection.close()