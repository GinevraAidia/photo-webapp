# Piano: photo-app — Eventi di ricordi fotografici

## Obiettivo
Web app dove ogni utente crea **eventi** (cartelle) contenenti **foto con descrizione**. Gli eventi sono:
- **Privati (default)**: visibili solo al proprietario e alle persone invitate via email.
- **Pubblici**: visibili a tutti gli utenti autenticati.
Reazioni emoji sulle foto. Niente commenti. Niente registrazione pubblica (account creati da superuser in Django admin).

## Stack esistente (da mantenere)
- Backend: Django 6.1.1 + DRF, Docker (`backend/Dockerfile.dev|prod`), gunicorn in prod
- Frontend: Vue 3 + TypeScript + Vite, pinia e vue-router già in `package.json`, nginx in prod (`frontend/nginx.conf` con proxy `/api/` → `backend:8000`)
- DB: PostgreSQL 18 nei compose (dev + prod); `settings.py` usa ancora SQLite → da collegare

## Decisioni prese con l'utente
1. Condivisione eventi privati via **email dell'invitato**; utenti non registrati ricevono la mail ma **non accedono finché un admin non crea il loro account** (matching per email). Ricerca utenti: posticipata.
2. **Django admin crea gli utenti**; login nell'app Vue via JWT.
3. Regola privacy: **nessun elenco partecipanti pre-esistente**; un partecipante diventa visibile agli altri solo dopo la sua **prima reazione emoji** a una foto dell'evento (le reazioni sono l'unica interazione disponibile).
4. **Tutti i partecipanti** autorizzati possono caricare foto; il proprietario può rimuovere foto e revocare condivisioni.
5. Homepage = griglia di "cartelle" con **tutti gli eventi accessibili**: pubblici + privati condivisi con l'utente. Nessuna pagina "Esplora" separata.

## Fix bloccante attuale (Pillow nel container)
Il backend gira in Docker: l'immagine installa solo i pacchetti di `backend/requirements.txt`. Pillow installato nella venv locale non esiste nel container → `fields.E210`.
1. Aggiungere `Pillow` a `backend/requirements.txt` (es. `Pillow==11.3.0`)
2. Ricreare l'immagine: `docker compose -f docker-compose.dev.yml up --build backend` (basta `docker compose restart`, senza rebuild non cambia nulla)

Correzioni sui modelli già scritti in `backend/events/models.py` (nome `Post` per le foto, accettato):
- `__str__` di `Event`, `Post`, `Reaction`, `EventShare` ritornano tuple → crash in admin; restituire stringa (es. f-string con i campi principali)
- `EventShare`: sostituire FK `user` con `email = models.EmailField()` + unique `(event, email)` — risponde al commento nel codice: si usa l'email, così un account creato dopo dall'admin (stessa email) ottiene l'accesso senza nuovi record
- `Post.uploaded_ad` → `uploaded_at` (typo, + migrazione)
- `Reaction`: confermato unique `(post, user)` = una sola reazione per utente per foto (semplificazione accettata rispetto a più emoji); rinominare la nested class `emoji` in `Emoji` per chiarezza

## Modello dati (app `events`, implementazione attuale)
- `Event`: `title`, `description?`, `owner` FK User, `visibility` (private|public, default private) — campo `date?` opzionale, rimandabile
- `EventShare`: `event` FK, `email` (lowercase), `created_at`; unique `(event, email)`. L'accesso si risolve a runtime: `User.email ∈ EventShare` (così un account creato dopo dall'admin ottiene subito accesso)
- `Post` (la foto): `event` FK, `uploader` FK User, `image` (ImageField), `description` (testo, opzionale), `uploaded_at`
- `Reaction`: `post` FK, `user` FK, `emoji` (choices da set fisso), unique `(post, user)` = una reazione per utente; POST la crea/aggiorna (toggle)

## Matrice permessi API
| Azione | Chi |
|---|---|
| Evento: creare | qualsiasi utente autenticato |
| Evento: vedere | pubblici: tutti gli autenticati; privati: owner o email in EventShare |
| Caricare foto | privati: owner + condivisi; pubblici: qualsiasi autenticato |
| Reagire | chi può vedere l'evento |
| Vedere partecipanti | solo i partecipanti "rivelati" (≥1 reazione nell'evento) + owner che vede invece l'elenco completo delle email condivise |
| Gestire condivisioni / eliminare foto evento | solo owner; uploader può eliminare le proprie foto |

## Attività backend (in ordine)
1. `settings.py`: DB Postgres via env (`DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT`, già presenti in `docker-compose.prod.yml`), `MEDIA_ROOT/MEDIA_URL`, `rest_framework` + SimpleJWT, `corsheaders` (allow `localhost:5173`), `EMAIL_*` da env (console in dev, SMTP in prod)
2. `requirements.txt`: aggiungere `djangorestframework-simplejwt`, `django-cors-headers`, `Pillow` (già presenti: `psycopg[binary]`)
3. Creare app `events` con i 4 modelli sopra + migrazioni
4. Serializers + ViewSets + router:
   - `POST /api/auth/token/`, `POST /api/auth/token/refresh/` (SimpleJWT)
   - `/api/events/` (list = solo eventi accessibili; filtri: visibility), retrieve, create, update/delete (owner)
   - `/api/events/{id}/photos/` (GET/POST multipart), `/api/photos/{id}/` (DELETE con regole sopra)
   - `/api/photos/{id}/reactions/` (POST/DELETE toggle emoji)
   - `/api/events/{id}/participants/` (solo rivelati), `/api/events/{id}/shares/` (GET/POST/DELETE, solo owner)
   - `GET /api/me/` (dati utente per il frontend)
5. Email su nuova condivisione all'indirizzo invitato (indipendente dall'esistenza dell'account)
6. Test DRF per la matrice permessi, in particolare: partecipanti nascosti finché non reagiscono, accesso via email condivisa anche per account creato dopo, eventi pubblici vs privati

## Attività frontend (in ordine)
1. Client API (`src/api/`): fetch/axios con interceptor refresh JWT, token in localStorage (MVP)
2. Store pinia `auth` (login, logout, utente corrente) + guardia rotte
3. Router: `/login`, `/` (griglia eventi), `/events/new`, `/events/:id`, `/events/:id/manage`
4. Pagine/componenti:
   - Login (email+password → JWT)
   - Home: card "cartella" per evento accessibile + bottone nuovo evento
   - Dettaglio evento: griglia foto con descrizione, upload (file+descrizione), reazioni emoji (set fisso), elenco partecipanti (solo rivelati)
   - Manage (owner): form aggiunta email, elenco email condivise con revoca
5. `npm run type-check` e `npm run build` senza errori

## Infra/Docker
1. `docker-compose.dev.yml`: passare `DB_*` al servizio backend + volume `media_data` su `backend`
2. `docker-compose.prod.yml`: volume media anche in prod; `frontend/nginx.conf`: aggiungere `location /media/` proxy a backend
3. Static admin in prod: aggiungere `whitenoise` (o servire via nginx)
4. **`.env` contiene credenziali in chiaro e testo non strutturato**: ripulirlo (solo `KEY=VALUE`), verificare che sia in `.gitignore` e ruotare le password esposte

## Validazione
1. `docker compose -f docker-compose.dev.yml up --build`; migrare, creare superuser, creare un utente normale da admin
2. Flussi manuali: login → crea evento privato → condividi email → foto + descrizioni → reazioni da secondo utente → il primo visibile tra i partecipanti solo dopo la reazione
3. Caso limite: condivisione a email senza account → nessun accesso finché l'admin non crea l'account con quella email
4. Evento pubblico visibile a un terzo utente non condiviso, con possibilità di reagire
5. Suite test backend verde; `type-check` frontend verde

## Fuori scope (per ora)
- Ricerca utenti, commenti, miniature/thumbnail, S3, registrazione pubblica, notifiche in-app, password reset via email
