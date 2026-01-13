# Deploy guide (server preparation)

This guide describes how to prepare an Ubuntu server for deploying the Online School Django project
with Gunicorn + systemd + Nginx.

## 1) Create deploy user and SSH access

# login as root first
adduser deploy
usermod -aG sudo deploy

# copy your public key to server (run from your local machine)
# ssh-copy-id deploy@SERVER_IP

# on server: disable password auth after key works
sudo nano /etc/ssh/sshd_config
# set:
#   PasswordAuthentication no
#   PermitRootLogin no
sudo systemctl restart ssh

## 2) Firewall (UFW)

sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status

## 3) Install system packages

sudo apt update
sudo apt install -y python3-venv python3-pip git nginx postgresql-client

## 4) Project directory layout

sudo mkdir -p /opt/online_school
sudo chown -R deploy:deploy /opt/online_school

# clone repository
cd /opt/online_school
git clone <YOUR_REPO_URL> .

## 5) Virtualenv and dependencies

python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install poetry
poetry install --no-interaction --no-root

## 6) Environment file

# create /opt/online_school/.env based on .env.example
nano /opt/online_school/.env

# IMPORTANT: set DJANGO_ALLOWED_HOSTS, SECRET_KEY, DB_*, etc.

## 7) Django init

/opt/online_school/.venv/bin/python manage.py migrate --noinput
/opt/online_school/.venv/bin/python manage.py collectstatic --noinput

## 8) systemd (Gunicorn)

# copy service file
sudo cp /opt/online_school/deploy/online_school.service /etc/systemd/system/online_school.service

sudo systemctl daemon-reload
sudo systemctl enable online_school.service
sudo systemctl start online_school.service
sudo systemctl status online_school.service

## 9) Nginx site

# copy nginx config
sudo cp /opt/online_school/deploy/nginx.conf /etc/nginx/sites-available/online_school.conf

# enable site
sudo ln -sf /etc/nginx/sites-available/online_school.conf /etc/nginx/sites-enabled/online_school.conf

# optional: disable default site
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl restart nginx

## 10) Verify

curl -I http://SERVER_IP/
