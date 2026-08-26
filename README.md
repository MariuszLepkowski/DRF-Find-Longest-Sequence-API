# DRF Find Longest Sequence API

## Opis

Prosta aplikacja oparta o Django REST Framework rozwiązująca problem wyszukiwania najdłuższej sekwencji identycznych, następujących po sobie znaków.

Przykład:

Dla ciągu:

```text
11199922233475599999
```

wynikiem będzie:

```text
99999
```

ponieważ jest to najdłuższa sekwencja powtarzających się znaków.

---

## Podejście do rozwiązania

Logika wyszukiwania została wydzielona do warstwy serwisowej (`core/services.py`), dzięki czemu pozostaje niezależna od Django REST Framework i może być testowana w izolacji.

Algorytm wykonuje pojedyncze przejście po ciągu wejściowym (single-pass scan).

### Złożoność

* Czasowa: **O(N)**
* Pamięciowa: **O(1)**

---

## Endpoint

### POST

Przetwarza ciąg przekazany w żądaniu.

**Request**

```json
{
  "raw_sequence": "11199922233475599999"
}
```

**Response**

```json
{
  "input_sequence": "11199922233475599999",
  "longest_sequence": "99999",
  "length": 5
}
```

---

### GET

Pobiera dane z zewnętrznego API wskazanego przez zmienną środowiskową:

```env
EXTERNAL_API_URL
```

Następnie analizuje otrzymany ciąg i zwraca wynik w tej samej strukturze co endpoint POST.

---

## Konfiguracja

### 1. Utworzenie środowiska wirtualnego

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

### 2. Instalacja zależności

```bash
pip install -r requirements.txt
```

---

### 3. Konfiguracja zmiennych środowiskowych

Utwórz plik:

```text
.env
```

na podstawie:

```text
.env.example
```

Przykład:

```env
SECRET_KEY=your-secret-key
EXTERNAL_API_URL=https://twoj-webhook-site-url
```

W przypadku uruchamiania tego projektu na potrzeby demonstracyjne w miejsce EXTERNAL_API_URL wklej adres webhooka, który przygotowałem w celach demonstracyjnych:
https://webhook.site/372c2317-2fdc-42ed-a0da-5f236f00fc94

---

### 4. Migracje

```bash
python manage.py migrate
```

---

### 5. Uruchomienie aplikacji

```bash
python manage.py runserver
```

Domyślnie:

```text
http://127.0.0.1:8000/api/process/
```

---

## Uruchamianie testów

```bash
pytest
```

---

## Formatowanie i statyczna analiza kodu

Sprawdzenie kodu:

```bash
ruff check .
```

Automatyczne poprawki:

```bash
ruff check . --fix
```

Formatowanie:

```bash
ruff format .
```

---

## Struktura projektu

```text
drf-find-longest-sequence/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── core/
│   ├── services.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── .env.example
├── manage.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Testowane scenariusze

* poprawne wyszukiwanie najdłuższej sekwencji,
* pojedynczy znak,
* brak powtórzeń,
* cały ciąg składający się z jednego znaku,
* pusty ciąg,
* wartość `None`,
* poprawna obsługa endpointu POST,
* walidacja błędnych danych wejściowych,
* poprawna obsługa danych pobranych z zewnętrznego API,
* obsługa błędów komunikacji z zewnętrznym API.
