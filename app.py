import requests
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import ipaddress, re, shutil, subprocess
from datetime import datetime

app = Flask(__name__)

JUTSU = [
 {"id":"chidori","name":"Chidori","style":"Lightning Release","icon":"⚡","description":"Network reconnaissance and port analysis.","phase":"PHASE 2","status":"ONLINE"},
 {"id":"sharingan","name":"Sharingan","style":"Eye of Insight","icon":"👁️","description":"Analyze security logs and identify suspicious activity.","phase":"PHASE 3","status":"ONLINE"},
 {"id":"byakugan","name":"Byakugan","style":"All-Seeing Eye","icon":"◉","description":"Network visibility and host discovery.","phase":"PHASE 4","status":"ONLINE"},
 {"id":"rasengan","name":"Rasengan","style":"Wind Release","icon":"🌀","description":"Authorized web security assessment.","phase":"PHASE 5","status":"ONLINE"},
 {"id":"amaterasu","name":"Amaterasu","style":"Black Flame","icon":"🔥","description":"Indicator-of-compromise and threat detection.","phase":"FUTURE","status":"ONLINE"},
 {"id":"shadow","name":"Shadow Clone","style":"Multi-Task Technique","icon":"🥷","description":"Run multiple defensive analysis tasks.","phase":"FUTURE","status":"ONLINE"}
]

PATTERNS = [
 ("Failed authentication", r"(failed password|authentication failure|login failed|invalid user|failed login)", "MEDIUM"),
 ("Successful authentication", r"(accepted password|accepted publickey|login successful|authentication successful)", "INFO"),
 ("Privilege escalation", r"(sudo:|su:|privilege escalation|became root)", "HIGH"),
 ("Account lockout", r"(account locked|too many authentication failures|locked out)", "HIGH"),
 ("Connection refused", r"(connection refused|refused connection)", "LOW")
]

def validate_ip(target):
    try: return str(ipaddress.ip_address(target.strip()))
    except ValueError: return None

@app.get("/")
def index(): return render_template("index.html", jutsu=JUTSU)

@app.post("/api/chidori")
def chidori():
    data=request.get_json(silent=True) or {}; target=validate_ip(data.get("target",""))
    if not target: return jsonify(ok=False,error="Enter a valid single IP address."),400
    if shutil.which("nmap") is None: return jsonify(ok=False,error="Nmap is not installed or not available in PATH."),500
    try: p=subprocess.run(["nmap","-T3","-F",target],capture_output=True,text=True,timeout=90,shell=False)
    except subprocess.TimeoutExpired: return jsonify(ok=False,error="Nmap scan timed out after 90 seconds."),504
    except OSError as e: return jsonify(ok=False,error=str(e)),500
    if p.returncode != 0: return jsonify(ok=False,error=p.stderr.strip() or "Nmap returned an error.",raw=p.stdout),500
    ports=[]; rx=re.compile(r"^(\d+)/(tcp|udp)\s+(\S+)\s+(.+?)\s*$")
    for line in p.stdout.splitlines():
        m=rx.match(line.strip())
        if m: ports.append({"port":m.group(1),"protocol":m.group(2),"state":m.group(3),"service":m.group(4)})
    return jsonify(ok=True,target=target,host_up=bool(re.search(r"\bHost is up\b",p.stdout,re.I)),ports=ports,raw=p.stdout)

def analyze_logs(text):
    findings=[]; failed=defaultdict(int)
    for n,raw in enumerate(text.splitlines(),1):
        line=raw.strip()
        if not line: continue
        hit=None
        for label,pat,sev in PATTERNS:
            if re.search(pat,line,re.I): hit=(label,sev); break
        if not hit: continue
        ipm=re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b",line); um=re.search(r"(?:for (?:invalid user )?|user[=: ]+)([A-Za-z0-9_.-]+)",line,re.I)
        ip=ipm.group(0) if ipm else "Unknown"; user=um.group(1) if um else "Unknown"
        if hit[0]=="Failed authentication": failed[ip]+=1
        findings.append({"line":n,"type":hit[0],"severity":hit[1],"source_ip":ip,"user":user,"message":line[:300]})
    for ip,count in failed.items():
        if ip!="Unknown" and count>=5: findings.append({"line":"-","type":"Repeated authentication failures","severity":"HIGH","source_ip":ip,"user":"Multiple/Unknown","message":f"{count} failed authentication events from {ip}. Review for possible brute-force activity."})
    counts={s:sum(x["severity"]==s for x in findings) for s in ["HIGH","MEDIUM","LOW","INFO"]}; counts["total_events"]=len(findings)
    top=sorted([{"ip":k,"count":v} for k,v in failed.items() if k!="Unknown"],key=lambda x:x["count"],reverse=True)[:10]
    return counts,findings[:100],top

@app.post("/api/sharingan")
def sharingan():
    data=request.get_json(silent=True) or {}; text=data.get("text","")
    if not isinstance(text,str) or not text.strip(): return jsonify(ok=False,error="Paste a log sample first."),400
    if len(text)>1_000_000: return jsonify(ok=False,error="Maximum log size is 1 MB."),413
    counts,findings,top=analyze_logs(text)
    return jsonify(ok=True,analyzed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),counts=counts,findings=findings,top_ips=top)

@app.post("/api/byakugan")
def byakugan():
    data=request.get_json(silent=True) or {}; target=str(data.get("target","")).strip()
    try: network=ipaddress.ip_network(target,strict=False)
    except ValueError: return jsonify(ok=False,error="Enter a valid CIDR, e.g. 192.168.1.0/24."),400
    if not network.is_private: return jsonify(ok=False,error="Byakugan only allows private/local networks."),400
    if network.num_addresses>1024: return jsonify(ok=False,error="Network too large. Maximum is 1024 addresses."),400
    if shutil.which("nmap") is None: return jsonify(ok=False,error="Nmap is not installed or not available in PATH."),500
    try: p=subprocess.run(["nmap","-sn","-T3",str(network)],capture_output=True,text=True,timeout=90,shell=False)
    except subprocess.TimeoutExpired: return jsonify(ok=False,error="Byakugan host discovery timed out after 90 seconds."),504
    except OSError as e: return jsonify(ok=False,error=str(e)),500
    raw=p.stdout or ""; raw += (("\n" if raw else "")+p.stderr) if p.stderr else ""; hosts=[]; current=None
    for line in raw.splitlines():
        m=re.search(r"^Nmap scan report for (.+)$",line.strip(),re.I)
        if m:
            if current: hosts.append(current)
            label=m.group(1).strip(); im=re.search(r"\((\d{1,3}(?:\.\d{1,3}){3})\)$",label)
            ip=im.group(1) if im else label; name=label[:label.rfind(" (")] if im else ""; current={"ip":ip,"name":name,"status":"up","latency":"—"}; continue
        if current:
            lm=re.search(r"Host is up\s*\(([^)]+)\)",line,re.I)
            if lm: current["latency"]=lm.group(1)
    if current: hosts.append(current)
    unique=[]; seen=set()
    for h in hosts:
        try: ipaddress.ip_address(h["ip"])
        except ValueError: continue
        if h["ip"] not in seen: seen.add(h["ip"]); unique.append(h)
    if p.returncode!=0: return jsonify(ok=False,error=p.stderr.strip() or "Nmap returned an error.",raw=raw,hosts=unique),500
    return jsonify(ok=True,target=str(network),hosts=unique,count=len(unique),raw=raw)

@app.post("/api/amaterasu")
def amaterasu():
    data=request.get_json(silent=True) or {}; text=str(data.get("text",""))
    if not text.strip(): return jsonify(ok=False,error="Paste logs, indicators, or text to analyze."),400
    detections=[]
    for ip in sorted(set(re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text))):
        try: addr=ipaddress.ip_address(ip)
        except ValueError: continue
        if not addr.is_private and not addr.is_loopback and not addr.is_reserved: detections.append({"type":"IPv4","indicator":ip,"severity":"MEDIUM","reason":"Public IPv4 observed; review against trusted infrastructure."})
    for h in sorted(set(re.findall(r'(?i)(?<![A-F0-9])(?:[A-F0-9]{32}|[A-F0-9]{40}|[A-F0-9]{64})(?![A-F0-9])',text))):
        typ={32:"MD5",40:"SHA-1",64:"SHA-256"}[len(h)]; detections.append({"type":typ,"indicator":h,"severity":"HIGH","reason":f"{typ} hash detected; validate with trusted threat intelligence."})
    for d in sorted(set(re.findall(r'(?i)(?<![@\w.-])(?:https?://)?(?:[a-z0-9-]+\.)+[a-z]{2,}(?::\d+)?(?:/[^\s<]*)?',text))):
        d=d.rstrip('.,;:)')
        if d.lower() not in {"example.com","example.org","example.net"}: detections.append({"type":"DOMAIN/URL","indicator":d,"severity":"MEDIUM","reason":"Domain/URL observed; verify reputation and expected use."})
    rules=[(r'(?i)(failed password|authentication failure|login failed|invalid user).{0,160}(?:\d{1,3}\.){3}\d{1,3}',"HIGH","Failed authentication activity with a source IP."),(r'(?i)(powershell|cmd\.exe|wscript|cscript).{0,180}(?:-enc|-encodedcommand|downloadstring|invoke-expression|\biex\b)',"HIGH","Suspicious encoded/download command-execution pattern."),(r'(?i)(mimikatz|sekurlsa|lsass|credential dumping)',"HIGH","Credential-access terminology detected."),(r'(?i)(port scan|nmap|masscan|scan detected)',"MEDIUM","Network scanning activity detected."),(r'(?i)(privilege escalation|sudo|administrator|root).{0,120}(success|granted|elevat)',"MEDIUM","Privilege-escalation-related activity detected.")]
    for p,s,r in rules:
        if re.search(p,text): detections.append({"type":"BEHAVIOR","indicator":"Matched security-event pattern","severity":s,"reason":r})
    seen=set(); unique=[]
    for d in detections:
        k=(d["type"],d["indicator"],d["severity"],d["reason"])
        if k not in seen: seen.add(k); unique.append(d)
    order={"HIGH":0,"MEDIUM":1,"LOW":2}; unique.sort(key=lambda x:(order.get(x["severity"],9),x["type"],x["indicator"]))
    counts={k:sum(x["severity"]==k for x in unique) for k in ["HIGH","MEDIUM","LOW"]}
    return jsonify(ok=True,count=len(unique),counts=counts,detections=unique,note="Local heuristic detection only. Validate important findings with trusted threat-intelligence sources.")

@app.post("/api/rasengan")
def rasengan():
    data=request.get_json(silent=True) or {}; target=str(data.get("target","")).strip()
    if not re.match(r"^https?://",target,re.I): return jsonify(ok=False,error="Enter a full HTTP/HTTPS URL."),400
    try:
        parsed=urlparse(target)
        if not parsed.hostname: raise ValueError()
        if parsed.port and parsed.port not in (80,443): return jsonify(ok=False,error="Only standard HTTP/HTTPS ports 80 and 443 are supported."),400
        target=parsed.geturl()
    except Exception: return jsonify(ok=False,error="Invalid target URL."),400
    try: r=requests.get(target,timeout=12,allow_redirects=True,headers={"User-Agent":"ShinobiSec-Rasengan/1.0"})
    except requests.exceptions.SSLError: return jsonify(ok=False,error="TLS/SSL validation failed for the target."),502
    except requests.exceptions.RequestException as e: return jsonify(ok=False,error=f"Unable to connect to target: {e}"),502
    h={k.lower():v for k,v in r.headers.items()}; findings=[]
    def finding(sev,title,detail): findings.append({"severity":sev,"check":title,"detail":detail})
    finding("INFO","HTTP status",f"Target returned HTTP {r.status_code}.")
    if r.url!=target: finding("INFO","Redirect","Target redirected to the final URL: "+r.url)
    for key,sev,title,detail in [("content-security-policy","MEDIUM","Content-Security-Policy missing","CSP is not present; browser-side injection impact may be harder to contain."),("strict-transport-security","MEDIUM","HSTS missing","Strict-Transport-Security is not present."),("x-content-type-options","LOW","X-Content-Type-Options missing","MIME-sniffing protection header is not present."),("x-frame-options","LOW","X-Frame-Options missing","Clickjacking protection header is not present.")]:
        if key not in h: finding(sev,title,detail)
    if "server" in h: finding("LOW","Server header exposed","Server response header: "+h["server"][:160])
    if "x-powered-by" in h: finding("LOW","Technology header exposed","X-Powered-By response header is exposed.")
    for cookie in r.headers.get("Set-Cookie","").split(","):
        if "secure" not in cookie.lower(): finding("MEDIUM","Cookie without Secure flag","A Set-Cookie value appears not to include Secure.")
        if "httponly" not in cookie.lower(): finding("LOW","Cookie without HttpOnly flag","A Set-Cookie value appears not to include HttpOnly.")
        break
    finding("INFO","HTTPS enabled","Target was accessed over HTTPS.") if parsed.scheme.lower()=="https" else finding("MEDIUM","Plain HTTP","Target was accessed over HTTP rather than HTTPS.")
    return jsonify(ok=True,target=target,final_url=r.url,status=r.status_code,findings=findings,headers={k:v for k,v in r.headers.items()},note="Rasengan performs non-destructive HTTP configuration checks only. Findings are indicators for review, not proof of exploitability.")

@app.post("/api/shadow-clone")
def shadow_clone():
    data=request.get_json(silent=True) or {}; text=str(data.get("text",""))
    if not text.strip(): return jsonify(ok=False,error="Paste authorized security data to analyze."),400
    import concurrent.futures
    def ioc_check():
        ips=[]
        for ip in sorted(set(re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text))):
            try:
                a=ipaddress.ip_address(ip)
                if not a.is_private and not a.is_loopback and not a.is_reserved: ips.append(ip)
            except ValueError: pass
        hashes=sorted(set(re.findall(r'(?i)(?<![A-F0-9])(?:[A-F0-9]{32}|[A-F0-9]{40}|[A-F0-9]{64})(?![A-F0-9])',text)))
        return {"module":"IOC scan","status":"completed","findings":len(ips)+len(hashes),"details":f"{len(ips)} public IP(s), {len(hashes)} file hash(es) observed."}
    def auth_check():
        failed=len(re.findall(r'(?i)(failed password|authentication failure|login failed|invalid user)',text)); high=failed>=5
        return {"module":"Authentication analysis","status":"completed","findings":failed,"details":f"{failed} failed-authentication event(s) detected."+(" Repeated failure threshold reached." if high else "")}
    def web_check():
        headers=[]; lower=text.lower()
        for h in ["content-security-policy","strict-transport-security","x-content-type-options","x-frame-options"]:
            if h not in lower: headers.append(h)
        return {"module":"Web configuration","status":"completed","findings":len(headers),"details":("Missing header indicators: "+", ".join(headers)) if headers else "No missing common security-header indicators found."}
    def threat_check():
        rules=[("PowerShell execution",r'(?i)(powershell|cmd\.exe|wscript|cscript).{0,180}(?:-enc|-encodedcommand|downloadstring|invoke-expression|\biex\b)'),("Credential access",r'(?i)(mimikatz|sekurlsa|lsass|credential dumping)'),("Scanning activity",r'(?i)(port scan|nmap|masscan|scan detected)'),("Privilege escalation",r'(?i)(privilege escalation|sudo|administrator|root).{0,120}(success|granted|elevat)')]
        hits=[name for name,p in rules if re.search(p,text)]
        return {"module":"Threat behavior","status":"completed","findings":len(hits),"details":("Matched: "+", ".join(hits)) if hits else "No configured suspicious-behavior patterns matched."}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(lambda f:f(),[ioc_check,auth_check,web_check,threat_check]))
    return jsonify(ok=True,clones=len(results),results=results,note="Shadow Clone runs independent local defensive checks in parallel. Findings are indicators for review, not proof of compromise.")

@app.get("/api/demo-data")
def demo_data():
    return jsonify({"sharingan":"Sep 12 15:01:22 server sshd[2101]: Failed password for root from 203.0.113.50 port 4021 ssh2\nSep 12 15:01:24 server sshd[2102]: Failed password for root from 203.0.113.50 port 4022 ssh2\nSep 12 15:01:26 server sshd[2103]: Failed password for admin from 203.0.113.50 port 4023 ssh2\nSep 12 15:01:28 server sshd[2104]: Failed password for admin from 203.0.113.50 port 4024 ssh2\nSep 12 15:01:30 server sshd[2105]: Failed password for root from 203.0.113.50 port 4025 ssh2\nSep 12 15:03:02 server sshd[2110]: Accepted password for analyst from 192.168.1.20 port 4040 ssh2\nSep 12 15:05:11 server sudo: analyst : TTY=pts/0 ; COMMAND=/usr/bin/systemctl status nginx","amaterasu":"Failed password for root from 203.0.113.50\npowershell -enc suspiciouscommand\nmimikatz credential dumping\nSHA256: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08\nhttps://suspicious-example.test/login","shadow":"Failed password for root from 203.0.113.50\npowershell -enc suspiciouscommand\nmimikatz credential dumping\n192.168.1.20\nSHA256: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08\nContent-Security-Policy missing\nprivilege escalation granted","rasengan":"https://example.com","byakugan":"192.168.1.0/24","chidori":"127.0.0.1"})

if __name__=="__main__": app.run(debug=True)
