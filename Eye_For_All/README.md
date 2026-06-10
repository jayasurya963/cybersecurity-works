## Eye_For_All -- OSINT Dashboard
A web-based Open Source Intelligence (OSINT) dashboard built in Python with Flask. It gathers public information about domains including WHOIS data, subdomains, and Shodan intelligence.
  - Easy to Use
  - Simple web interface
  - One-click scanning
    
## Features
- **Domain Reconnaissance**
  - WHOIS information (registrar, creation/expiration dates, name servers)
  - Subdomain discovery using crt.sh
  - Shodan integration (exposed hosts, ports, and services)

## Tech Stack
- **Backend**: Python + Flask
- **Database**: SQLite + Flask-SQLAlchemy
- **External Services**:
  - crt.sh (subdomains)
  - python-whois
  - Shodan API 
- **Frontend**: HTML + CSS + Chart.js

**create your python venv 'python -m venv venv'
**create a .env file to store shodan api key
**install the dependencies from 'requirements.txt' 
 
