from flask import Flask, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
def data():
    d = {'packets': 0, 'threats': 0, 'rules': 0, 'ps': 0, 'dd': 0, 'bf': 0, 'logs': []}
    
    # Read logs
    if os.path.exists('logs/attacks.log'):
        with open('logs/attacks.log') as f:
            atks = [l.strip() for l in f if l.strip()]
            d['threats'] = len(atks)
            d['logs'] = atks[-10:]
            
            for a in atks:
                if 'PORT_SCAN' in a: d['ps'] += 1
                elif 'DDOS' in a: d['dd'] += 1
                elif 'BRUTE_FORCE' in a: d['bf'] += 1
    
    # Read iptables
    r = subprocess.run(['sudo', 'iptables', '-L', 'ADAPTIVE_FW', '-n', '-v'],
                      capture_output=True, text=True)
    for line in r.stdout.split('\n'):
        if 'DROP' in line:
            p = line.split()
            if len(p) >= 8 and p[0].isdigit():
                d['packets'] += int(p[0])
                d['rules'] += 1
    
    return jsonify(d)

if __name__ == '__main__':
    print("="*60)
    print("📊 DASHBOARD ACTIVE")
    print("="*60)
    print("🌐 URL: http://localhost:5002")
    print("🔄 Auto-refreshes every 2 seconds")
    print("="*60)
    app.run(host='0.0.0.0', port=5002)