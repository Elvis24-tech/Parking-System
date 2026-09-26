# Parking System — Modern Parking Management System

A functional web-based parking system developed in Python/Flask for the Data Structures and Algorithms assignment.

## Features
- Login/logout for parking operator
- Visual parking slot map with 30 slots
- Vehicle entry and slot assignment
- Automatic entry timestamp
- Active parking session tracking
- Automatic duration calculation at exit
- Client-specified KSh tariff
- Payment method recording (Cash, M-Pesa, Card)
- Receipt number generation
- Simulated exit-barrier opening after payment
- Parking history and revenue
- Dynamic SQLite database
- Responsive HTML/CSS interface
- Documented use cases, algorithms, data structures and database design

## Tariff
| Duration | Fee |
|---|---:|
| Up to 30 minutes | KSh 0 |
| Up to 2 hours | KSh 50 |
| Up to 4 hours | KSh 100 |
| Up to 6 hours | KSh 300 |
| Over 6 hours | KSh 500 |

## Project structure
```text
modern_parking_system/
├── app.py
├── requirements.txt
├── parking.db              # created automatically on first run
├── templates/
├── static/
└── docs/
    ├── ALGORITHMS.md
    ├── DATA_STRUCTURES.md
    ├── DATABASE.md
    ├── USE_CASES.md
    └── REPORT.md
```

## Run locally
### 1. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the system
```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

### Demo login
- Username: `admin`
- Password: `admin123`

**For a real deployment, change the secret key and use proper password hashing/authentication.**

## GitHub submission
```bash
git init
git add .
git commit -m "Initial ParkSmart Kenya parking system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/parksmart-kenya.git
git push -u origin main
```

Do not commit a production database containing personal information or real credentials.

## Academic documentation
See the `docs/` directory for:
- Use cases and modules
- Algorithms for each module
- Data structures and reasons for their use
- Dynamic database design
- Full project report

## Production integration ideas
The barrier is intentionally simulated for a student project. A real deployment can connect a gate controller, vehicle sensor/ANPR camera and M-Pesa payment API after appropriate hardware, credentials and security controls are configured.
