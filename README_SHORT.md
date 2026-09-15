# Mojanova - kratka verzija za predaju profesoru

Mojanova je Flask e-commerce aplikacija razvijena za prodaju proizvoda sa korisničkim nalogom, admin panelom, korpom i checkout procesom.

## Funkcionalnosti

- korisnička registracija i login
- admin i korisnički role
- katalog proizvoda po kategorijama
- dodavanje u korpu i pregled korpe
- checkout i kreiranje porudžbine
- admin panel za upravljanje proizvodima i porudžbinama
- Bootstrap responzivni interfejs

## Tehnologije

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- Bootstrap 5
- SQLite (podrazumevano)
- MySQL podrška kroz DATABASE_URL

## Pokretanje

```bash
source venv/bin/activate
flask --app run run --debug
```

Aplikacija radi na:

```text
http://127.0.0.1:5000
```

## Baza

Podrazumevano se koristi SQLite:

```env
DATABASE_URL=sqlite:////home/sv/Desktop/mojanova/instance/app.db
```

Za MySQL se menja u:

```env
DATABASE_URL=mysql+pymysql://mojanova:mojanova123@localhost:3306/mojanova
```

## Napomena o korisničkim porukama

- registracija: `Welcome, {username}! Your account has been created.`
- login: `Welcome, {username}!`
- logout: `You have been logged out.`

## Zaključak

Projekat je funkcionalan, modularan i spreman za predaju i dalji razvoj. U osnovi je implementiran end-to-end e-commerce flow sa autentifikacijom i admin upravljanjem.
