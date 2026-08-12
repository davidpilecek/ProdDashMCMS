## Setup on a new Windows PC

### Prerequisites

- Git
- Node.js LTS
- pnpm
- Python 3.x

### Clone

git clone <repository>
cd ProductionDashboard

### Backend

cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

### Frontend

cd ..\frontend

pnpm install

### Configure API

Copy .env.example to .env

### Run backend

cd ..\backend
.\.venv\Scripts\Activate.ps1

python -m waitress --listen=127.0.0.1:5000 app:app

### Run frontend

cd ..\frontend

pnpm dev