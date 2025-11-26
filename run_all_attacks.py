from scapy.all import *
import time

print("="*60)
print("🔥 LAUNCHING ALL 3 ATTACKS")
print("="*60)

# ATTACK 1: PORT SCAN
print("\n🔴 ATTACK 1: PORT SCAN")
print("[*] Target: 127.0.0.53")
print("[*] Scanning 25 ports...\n")

for p in range(8000, 8025):
    send(IP(dst="127.0.0.53")/TCP(dport=p, flags="S"), verbose=0)
    if p % 5 == 0:
        print(f"[+] Scanned {p-7999} ports")
    time.sleep(0.05)

print("✓ Port scan complete!\n")
print("[*] Waiting 5 seconds...\n")
time.sleep(5)

# ATTACK 2: DDOS
print("🟡 ATTACK 2: DDOS")
print("[*] Target: 127.0.0.54:80")
print("[*] Sending 120 requests...\n")

for i in range(120):
    send(IP(dst="127.0.0.54")/TCP(dport=80, flags="S"), verbose=0)
    if i % 20 == 0:
        print(f"[+] Sent {i} requests")
    time.sleep(0.02)

print("✓ DDoS complete!\n")
print("[*] Waiting 5 seconds...\n")
time.sleep(5)

# ATTACK 3: BRUTE FORCE
print("🟠 ATTACK 3: BRUTE FORCE")
print("[*] Target: 127.0.0.55:22")
print("[*] Attempting 8 logins...\n")

for i in range(8):
    send(IP(dst="127.0.0.55")/TCP(dport=22, flags="S"), verbose=0)
    print(f"[+] Attempt {i+1}/8")
    time.sleep(0.3)

print("✓ Brute force complete!\n")

print("="*60)
print("✅ ALL ATTACKS COMPLETED!")
print("="*60)
print("\n📊 Check dashboard: http://localhost:5002")
print("🔍 Check logs: cat logs/attacks.log")
print("🛡️  Check blocks: sudo iptables -L ADAPTIVE_FW -n -v\n")