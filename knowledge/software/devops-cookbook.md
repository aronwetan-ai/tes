# DevOps Cookbook — Snippet Library

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (`@nexusai.devops`) — referensi cookbook
Source: Adapted from SUPERAGENT v2 m2.md
Replaces: NOTHING — `companies/nexusai/skills/devops/SKILL.md` tetap autoritatif

---

## Purpose

Library bash snippets untuk infrastructure tasks yang sering muncul.
Snippet ini sudah tested, tinggal paste-adapt-run.

NexusAI devops SKILL.md tetap pegang kendali keputusan (when to deploy, what env, security review). Cookbook ini hanya implementation reference.

---

## A. Environment Bootstrap (Debian/Ubuntu)

```bash
# Update + essentials + firewall
apt update && apt upgrade -y
apt install -y curl wget git unzip nano htop ufw fail2ban
ufw allow 22 && ufw allow 80 && ufw allow 443 && ufw --force enable
```

---

## B. Node.js + PM2 Stack

```bash
# Node 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# PM2 + auto-start on reboot
npm install -g pm2
pm2 startup systemd
pm2 save
```

---

## C. Python venv Stack

```bash
apt install -y python3 python3-pip python3-venv
python3 -m venv /opt/venv
source /opt/venv/bin/activate
# pip install -r requirements.txt
```

---

## D. Nginx + Certbot SSL (Let's Encrypt)

```bash
# Install
apt install -y nginx certbot python3-certbot-nginx
systemctl enable nginx

# Free SSL cert (replace placeholders)
certbot --nginx -d <domain.tld> --non-interactive --agree-tos -m <email@domain.tld>
```

### Nginx reverse proxy template

```nginx
# /etc/nginx/sites-available/<app>
server {
    listen 80;
    server_name <domain.tld>;

    location / {
        proxy_pass http://localhost:<PORT>;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

---

## E. Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com | bash
systemctl enable docker
usermod -aG docker $USER
# logout-login supaya group berlaku
```

---

## F. Deployment Sequences

### Node.js app

```bash
git clone <url> <dir>
cd <dir>
npm install --production
pm2 start index.js --name "<id>"
pm2 save
```

### Python ASGI (FastAPI/Starlette)

```bash
pm2 start "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000" \
  --name "<id>"
pm2 save
```

### Static site

```bash
cp -r dist/* /var/www/html/
nginx -t && systemctl reload nginx
```

---

## G. Instrumentation (Real-Time Diagnostics)

```bash
# Resource usage
htop
df -h

# PM2 process status
pm2 monit
pm2 logs <id>

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Network ports
netstat -tlnp
ss -tlnp

# System journal
journalctl -xe
journalctl -u nginx -f
```

---

## H. Common Recipe — Deploy Node.js App with HTTPS

```bash
# 1. Bootstrap (skip if already done)
apt update && apt install -y nginx certbot python3-certbot-nginx
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs && npm install -g pm2

# 2. Clone + install
git clone <repo-url> /opt/<app>
cd /opt/<app> && npm install --production

# 3. Run
pm2 start index.js --name "<app>"
pm2 startup systemd && pm2 save

# 4. Reverse proxy
cat > /etc/nginx/sites-available/<app> <<EOF
server {
    listen 80;
    server_name <domain.tld>;
    location / { proxy_pass http://localhost:3000; proxy_set_header Host \$host; }
}
EOF
ln -s /etc/nginx/sites-available/<app> /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 5. SSL
certbot --nginx -d <domain.tld> --non-interactive --agree-tos -m <email@domain.tld>
```

---

## Reference

- Source: `update/v2/openclaw/skills/m2.md`
- Authority: `companies/nexusai/skills/devops/SKILL.md`
