# Mojanova

Mojanova je Flask e-commerce aplikacija za prodaju proizvoda sa autentifikacijom korisnika, admin panelom, korpom i procesom poručivanja. Projekat je realizovan u Flask okruženju i koristi SQLAlchemy za modelovanje baze podataka.

## Urađeno

- registracija korisnika
- login i logout
- role-based pristup (admin / customer)
- katalog proizvoda po kategorijama
- korpa i izmena količina
- checkout i kreiranje porudžbine
- admin panel za upravljanje proizvodima i porudžbinama
- Bootstrap interfejs i responsivni dizajn
- poruke korisniku nakon registracije, logovanja i odjavljivanja

## Tehnologije

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- Bootstrap 5
- MySQL (XAMPP)

## XAMPP i MySQL setup

Za lokalni razvoj na Linux/Ubuntu-u, projekat je podešen da koristi MySQL kroz XAMPP. To znači da je aplikacija bila razvijana tako da se povezuje sa MySQL serverom, a ne samo sa SQLite-om.

### Koraci

1. Pokreni MySQL u XAMPP Control Panel-u.
2. Otvori phpMyAdmin.
3. Napravi bazu pod nazivom:

```sql
mojanova
```

4. U `.env` fajlu postavi konekciju:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/mojanova
```

Ako si koristio lozinku za root korisnika, onda:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/mojanova
```

## Pokretanje aplikacije

```bash
cd /home/sv/Desktop/mojanova
source venv/bin/activate
flask --app run run --debug
```

Aplikacija se pokreće na:

```text
http://127.0.0.1:5000
```

## Kako profesor pokreće projekat

1. Otvori XAMPP Control Panel.
2. Klikni Start pored MySQL.
3. Otvori phpMyAdmin u browseru:

```text
http://localhost/phpmyadmin
```

4. U phpMyAdmin-u kreiraj bazu pod nazivom:

```sql
mojanova
```

5. U projektu proveri da postoji fajl `.env` sa sledećom konekcijom:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/mojanova
```

Ako je root lozinka postavljena, koristi:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/mojanova
```

6. Otvori terminal u folderu projekta i aktiviraj virtuelno okruženje:

```bash
cd /home/sv/Desktop/mojanova
source venv/bin/activate
```

7. Pokreni aplikaciju:

```bash
flask --app run run --debug
```

8. U browseru otvori:

```text
http://127.0.0.1:5000/
```

9. Ako se pojavi greška `Address already in use`, to znači da je port 5000 već zauzet. U tom slučaju:
   - zaustavite prethodni Flask server, ili
   - pokrenite aplikaciju na drugom portu:

```bash
flask --app run run --debug --port 5001
```

I tada otvorite:

```text
http://127.0.0.1:5001/
```

## Napomena o bazi

Project koristi MySQL bazu u skladu sa XAMPP konfiguracijom, dok je SQLite ostavljen kao lokalni fallback za testiranje i razvoj bez aktivnog servera baze. Time je aplikacija kompatibilna sa oba pristupa, ali je za ispit i predaju najvažnija MySQL varijanta.

## Admin nalog

Admin korisnik se automatski pravi samo kada u lokalnom `.env` fajlu postaviš:

```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=izaberi-jaku-lozinku
```

Ne postavljaj ove vrednosti u javni kod niti ih objavljuj na GitHub-u.

## Objašnjenje port 5000

Port 5000 je zauzet kada već postoji pokrenut Flask server ili neki drugi proces koji koristi isti port. To nije problem sa MySQL-om. Problem je u operativnom sistemu i portovima, ne u bazi. Ukoliko port 5000 već radi, Flask ne može da startuje novu instancu na istom portu i javlja grešku `Address already in use`.

U tom slučaju treba:

- zaustaviti staru instancu, ili
- pokrenuti aplikaciju na drugom portu, npr. 5001.

Primer:

```bash
flask --app run run --debug --port 5001
```
