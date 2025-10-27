#Web_Vuln_Scanner

Web_Vuln_Scanner is a Flask-based web application for scanning and analyzing web pages. It fetches target pages, parses HTML, and performs vulnerability or content analysis. The project includes a Flask app package (app/) and a vulnScan/ directory that appears to contain a bundled Python environment or scanner modules.

Features

Web UI built with Flask

User authentication with Flask-Login

Persistent storage using Flask-SQLAlchemy

Fetch and parse pages using requests, beautifulsoup4, and lxml

Scanning modules located in vulnScan/ (contains scanner code and a bundled environment)

Project structure (detected)
Web_Scanner/
├─ app/                    # Flask application package (contains templates and static)
├─ instance/               # instance folder for config & runtime files (Flask pattern)
├─ vulnScan/               # scanner modules and a bundled virtualenv/site-packages
├─ config.py               # main configuration file
├─ requirements.txt        # pinned dependencies
├─ run.py                  # application entry point (used to start the Flask app)
└─ README.md               # <-- you can find this file here


Note: vulnScan/lib/python3.10/site-packages/ contains vendored packages (Flask, pip, etc.). This suggests the project may include a bundled environment; prefer using a fresh virtualenv for development and deployment.

Requirements

(Exact versions are in requirements.txt)

Python 3.8+ recommended

See requirements.txt (Flask==2.0.3, Flask-Login==0.5.0, Flask-SQLAlchemy==2.5.1, requests, beautifulsoup4, lxml)

Installation (recommended)

Clone the repo and change to the project directory:

git clone https://github.com/ravikumar287/Project/Web_Vuln_Scanner
cd Web_Vuln_Scanner


Create and activate a new virtual environment (do not use the provided vulnScan folder for development):

python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows PowerShell


Install dependencies:

pip install -r requirements.txt

Configuration

This project contains config.py and an instance/ folder. Use the instance/ folder for runtime configuration and secrets (Flask supports loading config from instance).

Create instance/.env or instance/config.py (do not commit secrets) with variables like:

SECRET_KEY='your-secret-key'
DATABASE_URL='sqlite:///instance/web_scanner.db'
FLASK_ENV=development


Alternatively set environment variables FLASK_APP=run.py and FLASK_ENV=development.

Database setup

If the app uses Flask-SQLAlchemy and migrations (Flask-Migrate), run:

flask db init        # if migrations not yet initialized
flask db migrate -m "Initial"
flask db upgrade


If no migrations are present, create the database by running a setup script or using the Flask shell to create tables:

flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

Running the app (development)

From the project root and with your virtualenv activated:

export FLASK_APP=run.py
export FLASK_ENV=development
flask run


Or run directly:

python run.py


Then open http://127.0.0.1:5000 in your browser.

Usage

Log in / create an account: (describe the app-specific flow here — if there is an admin seed script, document how to run it)

Add a URL to scan: go to the UI page for scans and enter the target URL

View scan results: results are stored in the database and visible in the web UI

Security & Legal

Do not scan targets without explicit permission from the owner. Unauthorized scanning can be illegal.

Keep SECRET_KEY and database credentials out of version control — use the instance/ folder or environment variables.

When deploying, use a production WSGI server (e.g., gunicorn) and a production database (Postgres, MySQL).

Developer notes

Main Flask package: app/ (look at app/__init__.py to find the factory or app creation code).

Entry point: run.py (contains if __name__ == '__main__' and likely runs the Flask app).

vulnScan/ contains scanning modules and a bundled environment. Inspect vulnScan/ for scanner plugin files and modules.

Templates and static files found at app/templates and app/static.

Tests

No explicit tests were detected at the top-level. If tests exist under a tests/ folder use:

pytest

Troubleshooting

If Flask can't find the app, export FLASK_APP=run.py or set app path explicitly.

If packages conflict with the bundled vulnScan environment, create and use a fresh virtualenv as shown above.

For DB errors, confirm DATABASE_URL is correctly set and tables are created.

