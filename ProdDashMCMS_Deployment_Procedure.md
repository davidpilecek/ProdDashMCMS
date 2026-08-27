# ProdDashMCMS — Deployment Procedure

This document describes the procedure for deploying a new version of **ProdDashMCMS** after making changes in development.

The basic principle is:

> **Build the application on the development PC → create a new installer → run the installer on the production PC.**

Do **not** manually replace files inside the production installation.

---

## 1. Development PC — Make and test your changes

Work normally in the development project:

```text
ProdDashMCMS/
├── backend/
├── frontend/
├── deployment/
└── ...
```

Run the application in development as usual:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
```

and:

```powershell
cd frontend
npm run dev
```

Test the changes thoroughly.

Do not modify the production `ProgramData` directory during development.

---

## 2. Update the application version

Before creating the production build, increment the application version.

For example:

```text
1.0.0
```

becomes:

```text
1.0.1
```

Update the version in the Inno Setup script:

```ini
#define MyAppVersion "1.0.1"
```

For a larger release, use an appropriate version such as `1.1.0` or `2.0.0`.

---

## 3. Build the React frontend

From the project root:

```powershell
cd frontend
npm run build
```

This creates/updates:

```text
frontend/
└── dist/
    ├── index.html
    └── assets/
        └── ...
```

This is the production frontend that PyInstaller will bundle.

Do not use `npm run dev` for the production build.

---
## 3.5. Download WinSW
go to https://github.com/winsw/winsw/releases?utm_source=chatgpt.com

download x64 version
place it in deployment/ and rename to ProdDashXCMSService.exe

in deployment/, create ProdDashXCMSService.xml

Example found in repo

## 4. Build the PyInstaller executable

Go to the project root:

```powershell
cd ..
```

Activate the backend virtual environment:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
cd ..
```

Then build:

```powershell
pyinstaller deployment\ProdDashMCMS.spec
```

PyInstaller should produce:

```text
dist/
└── ProdDashMCMS.exe
```

along with the WinSW files:

```text
dist/
├── ProdDashMCMS.exe
├── ProdDashMCMSService.exe
└── ProdDashMCMSService.xml
```

---

## 5. Test the new executable before deploying

Do not immediately create the installer.

First test the executable itself:

```powershell
cd dist
.\ProdDashMCMS.exe
```

Then open:

```text
http://127.0.0.1:5000
```

Test at least:

- Dashboard loading
- Production data
- Statistics
- Report generation
- Report logo
- Any functionality affected by your code change

If something does not work here, do not deploy it.

Stop the executable with:

```text
Ctrl+C
```

---


## Move Service files from deployment to dist

## 6. Create the production installer

Open:

```text
deployment/ProdDashMCMS.iss
```

in Inno Setup.

Make sure the version is correct:

```ini
#define MyAppVersion "1.0.1"
```

Compile the installer:

```text
Build → Compile
```

The result should be:

```text
deployment/
└── installer/
    └── ProdDashMCMSSetup.exe
```

This is the file to transfer to the production PC.

---

## 7. Transfer the installer to the production PC

Copy:

```text
ProdDashMCMSSetup.exe
```

to the production PC.

You do not need to copy:

```text
backend/
frontend/
.venv/
node_modules/
build/
```

The production PC does not need Python or Node.js installed.

---

## 8. Production PC — Stop the existing application

Before installing the update, stop the existing service.

Open **PowerShell as Administrator**.

Go to the installed application directory:

```powershell
cd "C:\Program Files\ANDRITZ\ProdDashMCMS"
```

Stop the service:

```powershell
.\ProdDashMCMSService.exe stop
```

Verify its status:

```powershell
.\ProdDashMCMSService.exe status
```

---

## 9. Run the new installer

Run:

```text
ProdDashMCMSSetup.exe
```

Allow administrator privileges if Windows requests them.

The installer should update:

```text
C:\Program Files\ANDRITZ\ProdDashMCMS\
```

with the new:

```text
ProdDashMCMS.exe
ProdDashMCMSService.exe
ProdDashMCMSService.xml
```

---

## 10. Protect the production data

Production data is stored separately from the application:

```text
C:\ProgramData\ANDRITZ\ProdDashMCMS\data\
```

An application update must not replace or delete this directory.

For example:

```text
C:\ProgramData\ANDRITZ\ProdDashMCMS\data\
├── 012026_PROD_LIST.csv
├── 012026_PROD_SEGMENT.csv
├── ...
└── 082026_PROD_LIST.csv
```

After an application update, these files should still be present.

The update changes:

```text
C:\Program Files\ANDRITZ\ProdDashMCMS\
```

but preserves:

```text
C:\ProgramData\ANDRITZ\ProdDashMCMS\data\
```

### Important

Never manually delete `ProgramData\data` unless you deliberately intend to delete production data.

---

## 11. Start the updated service

After installation:

```powershell
cd "C:\Program Files\ANDRITZ\ProdDashMCMS"
```

Start the service:

```powershell
.\ProdDashMCMSService.exe start
```

Check its status:

```powershell
.\ProdDashMCMSService.exe status
```

You want:

```text
State: Started
```

---

## 12. Test the application

Open:

```text
http://127.0.0.1:5000
```

Check:

- Dashboard loads
- Production data is available
- Statistics work
- Reports generate
- Reports contain the correct logo
- Existing production data is still present

Also test:

```text
http://127.0.0.1:5000/api/health
```

Expected response:

```json
{
    "status": "ok"
}
```

---

## 13. Test automatic startup

After confirming the update works, restart the production PC.

Do not manually start `ProdDashMCMS.exe`.

After Windows starts, open:

```text
http://127.0.0.1:5000
```

The dashboard should be available automatically.

You can also verify in:

```text
services.msc
```

that:

```text
ANDRITZ ProdDash MCMS
```

is:

```text
Running
Automatic
```

---

# Application vs. persistent data

This separation is critical for safe updates.

## Replaced during an application update

```text
C:\Program Files\ANDRITZ\ProdDashMCMS\
│
├── ProdDashMCMS.exe
├── ProdDashMCMSService.exe
└── ProdDashMCMSService.xml
```

These files represent the application.

## Preserved during an application update

```text
C:\ProgramData\ANDRITZ\ProdDashMCMS\
│
└── data\
    ├── 012026_PROD_LIST.csv
    ├── 012026_PROD_SEGMENT.csv
    ├── ...
    └── current production data
```

These files represent persistent production data.

---

# Complete update workflow

```text
┌──────────────────────────────┐
│       DEVELOPMENT PC         │
└──────────────┬───────────────┘
               │
               ▼
       Make code changes
               │
               ▼
       Test with dev setup
               │
               ▼
        npm run build
               │
               ▼
   PyInstaller ProdDashMCMS.spec
               │
               ▼
       Test ProdDashMCMS.exe
               │
               ▼
       Compile Inno Setup
               │
               ▼
     ProdDashMCMSSetup.exe
               │
               │ transfer
               ▼
┌──────────────────────────────┐
│        PRODUCTION PC         │
└──────────────┬───────────────┘
               │
               ▼
       Run installer
               │
               ▼
   Update Program Files
               │
               ▼
       Preserve ProgramData
               │
               ▼
       Install/update service
               │
               ▼
          Start service
               │
               ▼
       Test dashboard
               │
               ▼
       Restart Windows
               │
               ▼
          Verify startup
```

---

# Normal future workflow

Once the deployment is finalized, the normal development-to-production process is:

## Development PC

Build the frontend:

```powershell
cd frontend
npm run build
```

Build the executable:

```powershell
cd ..
pyinstaller deployment\ProdDashMCMS.spec
```

Test:

```powershell
cd dist
.\ProdDashMCMS.exe
```

Then compile:

```text
deployment/ProdDashMCMS.iss
```

This produces:

```text
ProdDashMCMSSetup.exe
```

## Production PC

Run:

```text
ProdDashMCMSSetup.exe
```

Then verify:

```text
http://127.0.0.1:5000
```

The production machine does not require:

- Python
- a Python virtual environment
- Node.js
- npm
- Vite
- an open terminal
- manual application startup

The Windows service starts the application automatically.
