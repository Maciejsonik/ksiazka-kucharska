# 📖 Rodzinny Przepiśnik – Skarbnica Domowych Smaków

Elektroniczna książka kucharska stworzona z odręcznych, rodzinnych kart z przepisami (154 rękopisy). Projekt łączy nowoczesną aplikację webową (PWA z trybem 100% offline i publikacją na GitHub Pages) z eleganckim, gotowym do druku albumem PDF (A4, ~300 stron).

---

## 📂 Struktura repozytorium

```text
ksiazka-kucharska/
├── index.html                 # Powłoka aplikacji webowej (PWA)
├── style.css                  # Style, motywy (jasny/ciemny) i animacje
├── app.js                     # Wyszukiwarka, filtry, przelicznik porcji, tryb gotowania, offline cache
├── recipes.json               # Baza 144 przepisów domowych
├── manifest.json              # Konfiguracja PWA dla urządzeń mobilnych (Android/iOS)
├── sw.js                      # Service Worker (pełne buforowanie offline)
├── icons/                     # Ikony aplikacji (192px i 512px)
├── images/                    # 154 oryginalne, obrócone zdjęcia rękopisów
├── ksiazka_kucharska.pdf      # Gotowa książka PDF do druku (A4, ~300 stron)
├── generate_pdf_book.py       # Skrypt kompilujący książkę do PDF przez Headless Chrome
├── start_offline.command      # Uruchamianie lokalnego serwera na macOS (1-klik)
├── bundle_for_sharing.py      # Skrypt pakujący do dystrybucyjnego pliku .zip
├── .nojekyll                  # Flaga wyłączająca silnik Jekyll na GitHub Pages
├── .github/workflows/         # Automatyczne wdrożenie na GitHub Pages
│   └── deploy.yml
├── AGENTS.md                  # Wytyczne i instrukcje deweloperskie
└── README.md                  # Dokumentacja projektu
```

---

## 🌐 Publikacja na GitHub Pages

Repozytorium posiada gotowy workflow (`.github/workflows/deploy.yml`), który automatycznie publikuje aplikację na GitHub Pages po każdym pushu do gałęzi `main`.

### Konfiguracja krok po kroku:
1. Utwórz nowe repozytorium na swoim koncie GitHub (np. `ksiazka-kucharska`).
2. Połącz lokalne repozytorium i wyślij kod:
   ```bash
   git remote add origin https://github.com/<twoj-login>/ksiazka-kucharska.git
   git branch -M main
   git push -u origin main
   ```
3. Na GitHubie wejdź w: **Settings ➔ Pages**:
   - W sekcji **Build and deployment ➔ Source** wybierz **GitHub Actions**.
4. Po ukończeniu akcji strona będzie natychmiast dostępna pod adresem:
   `https://<twoj-login>/github.io/ksiazka-kucharska/`

Dzięki połączeniu HTTPS rodzina może zainstalować aplikację bezpośrednio na telefonach (przycisk *„📲 Zainstaluj”*).

---

## 💻 Uruchamianie lokalne (100% Offline)

### 1. Na komputerze Mac:
- Kliknij dwukrotnie plik **`start_offline.command`**.
- Skrypt uruchomi lokalny serwer i otworzy stronę w przeglądarce pod adresem `http://localhost:8080`.
- *Alternatywa:* Możesz bezpośrednio otworzyć plik `index.html` w przeglądarce.

### 2. W domowej sieci Wi-Fi:
- Uruchom `start_offline.command`. W oknie terminala pojawi się Twój adres IP (np. `http://192.168.1.120:8080`).
- Każdy domownik w tej samej sieci może otworzyć ten link na telefonie.

---

## 🖨️ Książka kucharska w PDF

- Gotowy plik: **`ksiazka_kucharska.pdf`** (~82 MB).
- Zawiera ozdobną okładkę, wstęp, spis treści oraz 144 przepisy z oryginalnymi skanami i instrukcjami.
- Ponowne wygenerowanie po edycji `recipes.json`:
  ```bash
  python3 generate_pdf_book.py
  ```

---

## ✨ Kluczowe funkcje aplikacji

- **Wyszukiwarka odporna na polskie znaki:** Wpisanie np. `zur`, `ogorkowa`, `karkowka`, `twarog` bezbłędnie znajduje przepisy.
- **Dynamiczny przelicznik porcji:** Skalowanie składników (np. 0.5x, 1x, 2x, 3x).
- **Tryb kuchenny (Kitchen Mode):** Zabezpieczenie przed wygaszaniem ekranu (Screen Wake Lock API) i duży widok krok po kroku.
- **Menedżer Offline Cache:** 1 kliknięciem pobiera wszystkie 154 zdjęcia do pamięci CacheStorage telefonu.
- **Lista zakupów i Ulubione:** Zapisywane w pamięci przeglądarki (LocalStorage).
- **Podgląd oryginału:** Kliknięcie miniaturki rękopisu otwiera powiększone, oryginalne pismo.
- **Udostępnianie:** Integracja z natywnym Web Share API (WhatsApp, SMS, kopiowanie linku).
- **Motyw jasny i ciemny:** Komfortowe czytanie w dzień i w nocy.
