# Umlaramigro 🐾

[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![React Router](https://img.shields.io/badge/React_Router-7-CA4245?logo=reactrouter&logoColor=white)](https://reactrouter.com/)
[![Material UI](https://img.shields.io/badge/MUI-7-007FFF?logo=mui&logoColor=white)](https://mui.com/)
[![Redux Toolkit](https://img.shields.io/badge/Redux_Toolkit-2.x-764ABC?logo=redux&logoColor=white)](https://redux-toolkit.js.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Locust](https://img.shields.io/badge/Locust-load_tests-47A248)](https://locust.io/)

> **Umlaramigro** — "um lar, amigo" — is a full-stack pet adoption platform. Organizations list pets looking for a home, adopters browse and register interest, and everything runs on a modern React + Python stack.

## ✨ Features

- 🐕 Pet catalog with reusable cards and filters
- 🏢 Organization profiles managing their listed pets
- 💌 Adoption interest forms submitted by visitors
- 🔐 JWT authentication (login/register flows)
- ⚡ Global state management with Redux Toolkit
- 🧪 Load testing with Locust to validate API performance

## 🧱 Tech Stack

### Frontend (`frontend/`)

| Technology | Purpose |
|---|---|
| React 19 + React Router 7 | SPA framework and routing |
| TypeScript | Type safety across the app |
| Material UI (MUI) 7 | Component library |
| Redux Toolkit | Auth and pets global state |
| react-hook-form | Form handling and validation |
| Axios | HTTP client with interceptors |

### Backend (`backend/`)

| Technology | Purpose |
|---|---|
| Python + FastAPI | REST API |
| SQLAlchemy + PostgreSQL | Persistence layer |
| Pytest | Automated test suite |
| Locust | Load and performance testing |
| Docker + docker-compose | Containerized development |

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/   # Reusable UI (Header, PetCard, NavLink, Alert…)
│   ├── services/     # API layer (auth, pets, organizations, interest forms)
│   ├── stores/       # Redux slices (auth, pets)
│   └── types/        # Shared TypeScript types
backend/
├── app/              # FastAPI application
├── tests/            # pytest suite
└── locustfile.py     # Load testing scenarios
```

## 🚀 Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env      # configure database credentials
make migrate              # or: alembic upgrade head
make run                  # or: python run.py
```

### Frontend

```bash
cd frontend/umlaramigo
npm install
npm run dev
```

### Full stack with Docker

```bash
docker compose up --build
```

## 🧪 Testing & Load Testing

```bash
# Backend unit/integration tests
cd backend && pytest

# Load test the API (check locustfile.py for scenarios)
locust -f locustfile.py --host http://localhost:8000
```

Then open `http://localhost:8089` to configure and run your load test through the Locust web UI.

## 📜 License

MIT

---

⭐ Star this repo to support pet adoption through technology!
