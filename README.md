# 🌸 VocabHero

VocabHero je webová aplikace pro procvičování anglické slovní zásoby skrze herní režimy inspirované jazykovými aplikacemi a moderní estetikou.  
Projekt vznikl jako závěrečná školní práce a kombinuje pastelový, dreamy vibe s rychlým a přehledným UI.

---

## ✨ Funkce

- 🎮 **Hero Mode** – intenzivní časovaná výzva s progresivní obtížností  
- 📖 **Practice Mode** – procvičování podle úrovně, kategorie nebo náhodného remixu  
- 🗂️ **Detail slovíčka** – karta obsahující překlad, alternativní překlady, kategorii a obtížnost  
- 🛠️ **Admin Tools** – přidávání, úprava a mazání slovíček (role admin)  
- 👤 **Contributor Role** – omezený účet umožňující přidávání slovíček bez přístupu do administrace  
- 🎨 **Jednotný design** – pastelový, jemný vizuál 
- 🔒 **Autentizace a oprávnění** – login systém se správou uživatelů  
- 🐳 **Docker + PostgreSQL** – jednoduše spustitelné prostředí přes Docker Compose  

---

## 🛠️ Použité technologie

- **Python / Django** – backend, views, šablony  
- **PostgreSQL** – databáze (Docker)  
- **HTML, CSS, JavaScript** – frontend  
- **Google Fonts – Quicksand** – typografie aplikace  
- **Docker & Docker Compose** – deployment-ready vývojové prostředí  

---

## 🐳 Spuštění přes Docker

### 1️⃣ Naklonuj repozitář
```bash
git clone https://github.com/uzivatel/vocabhero.git
cd vocabhero
```
---

### 2️⃣ Vytvoření `.env` souboru
Projekt používá konfigurační proměnné uložené v `.env` souboru.

<<<<<<< HEAD
```env
POSTGRES_DB=vocabhero
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
=======
1. V kořenovém adresáři projektu vytvoř soubor `.env`
2. Zkopíruj obsah souboru `.env.example`
3. Případně uprav hodnoty podle potřeby
>>>>>>> 731211d (Uprava env + readme)
---

## 3️⃣ Spuštění aplikace

```bash
docker compose up --build
```
---

Aplikace poběží na adrese:  
➡️ **http://localhost:8000**

## 📚 Zdroje

- **Django Documentation** – https://docs.djangoproject.com/
- **PostgreSQL Docs** – https://www.postgresql.org/docs/
- **Docker Docs** – https://docs.docker.com/
