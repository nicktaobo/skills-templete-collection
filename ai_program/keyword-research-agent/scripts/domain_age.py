#!/usr/bin/env python3
"""Check domain registration age via WHOIS and web archive."""
import subprocess, json, sys, re

def check_domain(domain):
    age_info = "unknown"
    
    # Try WHOIS for creation date
    try:
        r = subprocess.run(["whois", domain], capture_output=True, text=True, timeout=10)
        for pattern in [r"Creation Date:\s*(.+)", r"created:\s*(.+)", r"Registered on:\s*(.+)", r"Registry Domain ID.*Creation Date:\s*(.+)"]:
            m = re.search(pattern, r.stdout, re.IGNORECASE)
            if m:
                age_info = m.group(1).strip()[:30]
                break
    except Exception:
        pass
    
    # Fallback: web archive first snapshot
    if age_info == "unknown":
        try:
            r = subprocess.run(
                ["curl", "-s", f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json&limit=1&fl=timestamp"],
                capture_output=True, text=True, timeout=10
            )
            data = json.loads(r.stdout)
            if len(data) > 1:
                age_info = f"first archive: {data[1][0][:8]}"
        except Exception:
            pass
    
    return age_info

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: domain_age.py <domain1> [domain2] ...")
        sys.exit(1)
    
    for domain in sys.argv[1:]:
        age = check_domain(domain)
        print(f"{domain}: {age}")
        sys.stdout.flush()
