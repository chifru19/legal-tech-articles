import socket
import dns.resolver

def audit_domain(domain):
    print(f"\n--- Security Audit for: {domain} ---")
    
    # 1. Check A Record (Basic Connectivity)
    try:
        ip = socket.gethostbyname(domain)
        print(f"[✓] A Record: Found (IP: {ip})")
    except socket.gaierror:
        print(f"[X] A Record: Not found. Domain may be down.")

    # 2. Check MX Records (Email Setup)
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        print(f"[✓] MX Records: Found {len(mx_records)} mail servers.")
    except:
        print(f"[!] MX Records: Missing! Email will not work.")

    # 3. Check SPF (Email Spoofing Protection)
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        spf = [r for r in txt_records if 'v=spf1' in r.to_text()]
        if spf:
            print(f"[✓] SPF Record: Found ({spf[0].to_text()[:30]}...)")
        else:
            print(f"[!] SPF Record: MISSING. Vulnerable to spoofing!")
    except:
        print(f"[!] SPF Record: Could not verify.")

    print("--- Audit Complete ---\n")

if __name__ == "__main__":
    target = input("Enter domain to audit (e.g., google.com): ")
    audit_domain(target)
