# Arsenal Aura

Production-ready Arsenal-themed fan app with a generator, match predictor, archive/info page, and a rule-based chat bot.

## Local Setup

### Backend (Django)
1. Create a virtual environment and install dependencies.
2. Copy `backend/.env.example` to `backend/.env` and set `DATABASE_URL` to your Neon database.
3. Run migrations and seed data.

Commands:

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver 8000
```

### Frontend (React + Vite)
1. Copy `frontend/.env.example` to `frontend/.env`.
2. Install dependencies and run.

Commands:

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints
Auth:
- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/auth/refresh`
- GET `/api/me`
- PATCH `/api/me`

Generator:
- GET `/api/generate?mode=&player=&intensity=`
- GET `/api/players`
- GET `/api/modes`

Predictor:
- GET `/api/fixtures/next`
- POST `/api/predictions`
- GET `/api/predictions/latest`
- POST `/api/predictions/{id}/check`

Info:
- GET `/api/info/honors`
- GET `/api/info/timeline`
- GET `/api/info/links`

Chat:
- POST `/api/chat`

## Deployment Notes

### Neon
1. Create a Neon project and database.
2. Copy the connection string into `DATABASE_URL` for the backend.

### Render (Backend)
1. Create a new Web Service from the `backend` folder.
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn arsenal_aura.wsgi:application`
4. Add environment variables from `backend/.env.example`.
5. Run `python manage.py migrate` and `python manage.py seed` in the Render shell once.

### Vercel (Frontend)
1. Import the `frontend` folder into Vercel.
2. Set `VITE_API_BASE_URL` to your Render backend URL.
3. Build command: `npm run build`
4. Output directory: `dist`

## Notes
- Football data is proxied through the backend to protect API keys.
- Banter Gate blocks Spurs/Chelsea selections until switched to Arsenal.
