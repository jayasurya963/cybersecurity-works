import requests
import time
import json
from datetime import datetime
from colorama import init, Fore, Style
from tqdm import tqdm
import argparse

init(autoreset=True)

class AuthSecurityTester:
    def __init__(self, base_url, login_endpoint):
        self.base_url = base_url.rstrip('/')
        self.login_url = f"{self.base_url}/{login_endpoint.lstrip('/')}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": self.base_url,
            "login_endpoint": self.login_url,
            "rate_limiting": {},
            "username_enumeration": {},
            "response_analysis": {},
            "recommendations": []
        }

    def test_login(self, username, password):
        data = {"username": username, "password": password}   # Change keys if your target uses email/password
        start = time.time()
        try:
            response = self.session.post(self.login_url, data=data, timeout=15, allow_redirects=True)
            duration = time.time() - start

            return {
                "status_code": response.status_code,
                "text": response.text[:800],
                "duration": round(duration, 3),
                "redirect": response.url
            }
        except Exception as e:
            return {"error": str(e)}

    def check_rate_limiting(self, attempts=20):
        print(f"{Fore.CYAN}[*] Testing Rate Limiting ({attempts} rapid attempts)...")
        blocked = False
        times = []

        for i in tqdm(range(attempts), desc="Rate Limit Test"):
            result = self.test_login("testuser", "wrongpass123")
            times.append(result.get("duration", 0))
            time.sleep(0.2)

            if result.get("status_code") == 429 or "too many" in result.get("text", "").lower():
                blocked = True
                break

        self.results["rate_limiting"] = {
            "tested_attempts": attempts,
            "blocked": blocked,
            "avg_response_time": round(sum(times)/len(times), 3) if times else 0
        }

        if blocked:
            print(f"{Fore.GREEN}[+] Rate limiting detected!")
        else:
            self.results["recommendations"].append("No rate limiting detected - HIGH RISK")

    def check_username_enumeration(self):
        print(f"{Fore.CYAN}[*] Testing for Username Enumeration...")
        test_users = ["admin", "administrator", "user", "test", "nonexistentuserxyz12345"]
        responses = {}

        for user in test_users:
            result = self.test_login(user, "randomwrongpassword123!")
            key = result.get("text", "").lower()
            responses[user] = {
                "status": result.get("status_code"),
                "contains_invalid": "invalid" in key or "incorrect" in key,
                "contains_exists": any(x in key for x in ["exist", "found", "valid"])
            }
            time.sleep(0.6)

        self.results["username_enumeration"] = responses
        print(f"{Fore.YELLOW}[!] Check if error messages differ between existing and non-existing users.")

    def run_full_test(self):
        print(f"\n{Fore.MAGENTA}=== Authentication Security Tester v2.0 ===\n")
        print(f"Target: {self.base_url}\n")

        self.check_rate_limiting()
        self.check_username_enumeration()

        print(f"\n{Fore.GREEN}=== Testing Completed ===\n")
        self.generate_report()

    def generate_report(self):
        filename = f"auth_security_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)

        print(f"{Fore.GREEN}[+] Detailed report saved: {filename}")
        print(f"{Fore.CYAN}Review the report carefully before making conclusions.")

# ====================== CLI ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Authentication Security Tester")
    parser.add_argument("url", help="Base URL of the target (e.g. https://example.com)")
    parser.add_argument("-l", "--login", default="login", help="Login endpoint (default: login)")
    args = parser.parse_args()

    tester = AuthSecurityTester(args.url, args.login)
    tester.run_full_test()