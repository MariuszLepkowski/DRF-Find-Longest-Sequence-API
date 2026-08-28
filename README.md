# DRF Find Longest Sequence API

## Opis

Prosta aplikacja oparta o Django REST Framework rozwiązująca problem wyszukiwania najdłuższej sekwencji identycznych, następujących po sobie znaków.

Przykład:

```text
11199922233475599999
```
wynikiem będzie:

```text
99999
```

ponieważ jest to najdłuższa sekwencja powtarzających się znaków.

---
Aplikacja udostępnia dwa sposoby dostarczenia danych:

-POST - ciąg przekazywany bezpośrednio w żądaniu,

-GET - ciąg pobierany z zewnętrznego API.

## Podejście do rozwiązania

Projekt został podzielony na kilka prostych warstw odpowiedzialnych za różne elementy przetwarzania:

- core/services.py - logika biznesowa i algorytm wyszukiwania najdłuższej sekwencji.
- core/clients.py - komunikacja z zewnętrznym API oraz obsługa błędów na poziomie klienta HTTP.
- core/serializers.py - walidacja danych wejściowych i struktura odpowiedzi API.
- core/views.py - obsługa żądań HTTP i połączenie poszczególnych elementów.
- core/tests.py - testy logiki biznesowej, klienta API oraz endpointów.

Taki podział pozwala testować poszczególne elementy niezależnie, bez wprowadzania dodatkowych warstw niewymaganych przez skalę zadania.

---

## Endpoint

### POST /api/process/

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

### GET /api/process/

Pobiera dane z zewnętrznego API wskazanego przez zmienną środowiskową:

```env
EXTERNAL_API_URL
```

Następnie analizuje otrzymany ciąg i zwraca wynik w tej samej strukturze co endpoint POST.
W przypadku problemu z komunikacją z zewnętrznym API endpoint zwraca:
```text
502 Bad Gateway
```

---

## Instalacja

```bash
uv sync
```

Aktywacja środowiska:

```bash
source .venv/bin/activate
```
---

### Konfiguracja zmiennych środowiskowych

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

Na potrzeby demonstracji projektu można użyć przygotowanego webhooka:
https://webhook.site/372c2317-2fdc-42ed-a0da-5f236f00fc94

SECRET_KEY można ustawić na dowolną wartość przeznaczoną do lokalnego środowiska demonstracyjnego.

Plik .env nie powinien być commitowany do repozytorium.

---

### Migracje

```bash
python manage.py migrate
```

---

### Uruchomienie aplikacji

```bash
python manage.py runserver
```

Domyślnie:

```text
http://127.0.0.1:8000/api/process/
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
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── clients.py       # komunikacja z zewnętrznymi API
│   ├── models.py
│   ├── serializers.py   # walidacja danych i struktura odpowiedzi
│   ├── services.py      # logika biznesowa i algorytm
│   ├── views.py         # endpointy HTTP
│   ├── urls.py          # routing aplikacji
│   └── tests.py         # testy
│
├── .env.example
├── .gitignore
├── manage.py
├── pyproject.toml
└── README.md
```
Odpowiedzialność poszczególnych warstw:
* views.py - obsługa żądań HTTP oraz połączenie poszczególnych elementów.
* serializers.py - walidacja danych wejściowych oraz definiowanie struktury odpowiedzi.
* clients.py - komunikacja z zewnętrznymi API i obsługa błędów na poziomie klienta HTTP.
* services.py - właściwa logika biznesowa i rozwiązanie problemu rekrutacyjnego.
* tests.py - testy jednostkowe logiki oraz testy integracyjne endpointów i komunikacji z klientem API.


## Uruchamianie testów
```bash
pytest
```
## Testowane scenariusze

* poprawne wyszukiwanie najdłuższej sekwencji,
* pojedynczy znak,
* brak powtarzających się znaków,
* cały ciąg składający się z jednego znaku,
* pusty ciąg,
* wartość `None`,
* poprawna obsługa endpointu POST,
* walidacja błędnych danych wejściowych,
* poprawna obsługa danych pobranych z zewnętrznego API,
* obsługa błędów komunikacji z zewnętrznym API.

Zapytania do zewnętrznego API są mockowane w testach, dzięki czemu testy nie wymagają dostępu do rzeczywistego zewnętrznego serwera.
