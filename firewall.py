from scapy.all import sniff, IP, TCP
import subprocess
import time
from collections import defaultdict

# Tracking structures
ip_ports = defaultdict(set)
ip_packets = defaultdict(int)
ip_auth = defaultdict(int)
blocked = set()

# Create iptables chain
subprocess.run(['sudo', 'iptables', '-N', 'ADAPTIVE_FW'], stderr=subprocess.DEVNULL)
subprocess.run(['sudo', 'iptables', '-I', 'INPUT', '-j', 'ADAPTIVE_FW'], stderr=subprocess.DEVNULL)

log = open('logs/attacks.log', 'a')

def block(ip, atype, msg):
    if ip in blocked or ip in ['127.0.0.1', '0.0.0.0']:
        return
    
    subprocess.run(['sudo', 'iptables', '-I', 'ADAPTIVE_FW', '-s', ip, '-j', 'DROP'])
    blocked.add(ip)
    
    entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | HIGH | {atype} | {ip} | {msg}"
    log.write(entry + '\n')
    log.flush()
    
    print(f"\n{'='*60}")
    print(f"🚨 {atype} ATTACK BLOCKED!")
    print(f"   IP: {ip}")
    print(f"   Details: {msg}")
    print(f"{'='*60}\n")

def handle(pkt):
    if IP in pkt and TCP in pkt:
        # CRITICAL FIX: Monitor DESTINATION IP (where packets are going)
        dst = pkt[IP].dst
        port = pkt[TCP].dport
        
        if dst in ['127.0.0.1', '0.0.0.0']:
            return
        
        # Track all packets to this destination
        ip_ports[dst].add(port)
        ip_packets[dst] += 1
        
        # Track auth port attempts
        if port in [22, 21, 3306]:
            ip_auth[dst] += 1
        
        # DEBUG: Print tracking info
        print(f"[DEBUG] Target: {dst} | Ports: {len(ip_ports[dst])} | Packets: {ip_packets[dst]} | Auth: {ip_auth[dst]}")
        
        # Check Port Scan FIRST (many different ports)
        if len(ip_ports[dst]) >= 20 and dst not in blocked:
            block(dst, 'PORT_SCAN', f"Scanned {len(ip_ports[dst])} ports")
            return
        
        # Check Brute Force SECOND (auth ports)
        if ip_auth[dst] >= 5 and dst not in blocked:
            block(dst, 'BRUTE_FORCE', f"{ip_auth[dst]} auth attempts")
            return
        
        # Check DDoS LAST (many packets to few ports)
        if ip_packets[dst] >= 100 and len(ip_ports[dst]) <= 3 and dst not in blocked:
            block(dst, 'DDOS', f"{ip_packets[dst]} requests to {len(ip_ports[dst])} port(s)")
            return

print("="*60)
print("🛡️  ADAPTIVE FIREWALL - MONITORING TARGETS")
print("="*60)
print("✓ Port Scan: 20+ unique ports")
print("✓ DDoS: 100+ packets to ≤3 ports")
print("✓ Brute Force: 5+ auth port attempts")
print("✓ Logging: logs/attacks.log")
print("\n[*] Monitoring network traffic...\n")

sniff(iface='lo', prn=handle, store=False)