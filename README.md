# INTURI Portal — Backend

FastAPI + PostgreSQL + Alembic backend for the INTURI MLA constituency portal,
matched to the React frontend at `mla-inr.netlify.app`.

Every module here maps to a real dashboard component in the frontend:
Schemes ↔ `BeneficiariesForm.jsx`, CMRF ↔ `CmrFundsForm.js`, Development ↔
`DevelopmentForm.js`, Media ↔ `Mp3Form.js`/`Mp4Form.js`, Gallery, Achievements,
Contact, and Voters.

This exact scaffold has been run end-to-end against a live PostgreSQL 16
instance: migrations applied cleanly, admin auth, CRUD, file uploads, and
public/admin route separation were all tested with real requests.

## 1. Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Database

```sql
CREATE DATABASE inturi_db;
CREATE USER inturi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE inturi_db TO inturi_user;
```

## 3. Configure

```bash
cp .env.example .env
```
Edit `.env`:
- `DATABASE_URL` — your Postgres connection string
- `SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_hex(32))"`
- `BACKEND_CORS_ORIGINS` — must include your frontend's real origin
- `FIRST_ADMIN_EMAIL` / `FIRST_ADMIN_PASSWORD` — your real admin login

## 4. Migrate

```bash
alembic upgrade head
```
This applies `alembic/versions/656fb90956b1_initial_schema.py`, which creates
all 13 tables (already generated and tested against a real Postgres instance).

If you change any model afterward, generate a new migration instead of
editing this one:
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

## 5. Seed the first admin

```bash
python -m app.db.init_db
```
Replaces the frontend's hardcoded `admin@gmail.com` / `admin123`.

## 6. Run

```bash
uvicorn app.main:app --reload --port 8000
```
Swagger UI: http://localhost:8000/docs

## 7. Test

```bash
pytest
```

## Auth flow

`POST /api/v1/auth/login` (OAuth2 password form: `username` = email,
`password`) returns a JWT. Send it as `Authorization: Bearer <token>` on
every admin (write) request. Public GET routes (schemes, development,
gallery, achievements, media, voter stats) need no token.

## File uploads

`POST /api/v1/uploads/{kind}` where `kind` is `image`, `video`, or `audio`
(admin only, multipart form field `file`). Returns `{"url": "/media/..."}` —
store that URL on the parent record (e.g. `Scheme.thumbnail_url`). Files are
served back at that same `/media/...` path.

## Production notes

- Run behind `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`
- Use managed Postgres, not self-hosted, for a public-facing site
- Run `alembic upgrade head` as a deploy step
- Set `BACKEND_CORS_ORIGINS` to your real domain only
- Swap `app/services/file_storage.py`'s local-disk logic for S3/Cloud
  Storage before deploying to a host with ephemeral disk
- CMRF beneficiary Aadhaar numbers are stored as last-4-digits only by
  design (`aadhaar_last4`) — the full number is accepted on input and
  discarded, never persisted
