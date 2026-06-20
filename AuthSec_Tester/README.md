# Authentication Security Tester 
A professional tool to test the security strength of login systems. It checks for common authentication vulnerabilities such as weak rate limiting, username enumeration, and poor error handling.

## Features 
- Rate Limiting Detection
- Username Enumeration Testing (Error-based)
- Response Time Analysis
- Detailed JSON Report Generation
- Colored Terminal Output
- Command Line Interface (CLI)

**Usage**
python auth_tester.py https://your-target.com  (or)
python auth_tester.py https://your-target.com --login admin/login

**Important**: Only use this tool on websites/applications you own or have explicit written permission to test.

**What It Tests**
Whether the system blocks brute-force attempts.
Whether different error messages reveal valid usernames.
How fast the application responds under load.
General authentication weaknesses.

**Sample Output** -
The tool generates a detailed auth_security_report_YYYYMMDD_HHMM.json file with all findings and recommendations.
