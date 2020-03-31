# fekrinocore
Initialize server :
~~~~
ssh root@ip_adsress
adduser ubuntu
usermod -aG sudo ubuntu
ufw allow OpenSSH
ufw enable
rsync --archive --chown=ubuntu:ubuntu ~/.ssh /home/ubuntu
exit
~~~~
**ssh ubuntu@ip_address**
~~~~
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql-contrib curl

sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
~~~~

**Virtual Envs**
~~~~
mkdir /home/ubuntu/.envs

cd /home/ubuntu/.envs 
virtualenv coronacore
~~~~

**Cloning Repositories**
~~~~
mkdir /home/ubuntu/dev
cd /home/ubuntu/dev
git clone https://gitlab.com/mhsn.iranmanesh/coronacore.git
git clone https://gitlab.com/thevahidal/coronakoo-pwa.git
git clone https://gitlab.com/mhsn.iranmanesh/corona-web.git
~~~~

**Docker**
~~~~
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
~~~~

**Postgres**
~~~~
sudo docker run --name=corona-postgis -d -e POSTGRES_USER=ubuntu -e POSTGRES_PASS=PASSWORD -e POSTGRES_DBNAME=corona-db -p 25432:5432 -v $HOME/postgres_data:/var/lib/postgresql kartoza/postgis
~~~~

**Django setup**
~~~~
source /home/ubuntu/.envs/coronacore/bin/activate
cd /home/ubuntu/dev/coronacore/

sudo apt-get install binutils libproj-dev gdal-bin

pip install -r requirments.txt

mkdir /home/ubuntu/dev/coronacore/logs

python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate

mkdir /home/ubuntu/dev/coronacore/static/map
~~~~

**Rabbit MQ**
~~~~
sudo apt-get install -y erlang
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl status rabbitmq-server
~~~~

**Gunicorn**
~~~~
sudo nano /etc/systemd/system/gunicorn.socket
[INSERT DATA FROM FILE]

sudo nano /etc/systemd/system/gunicorn.service
[INSERT DATA FROM FILE]

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
~~~~

**Celery / Beats**
~~~~

sudo apt-get install supervisor
sudo nano /etc/supervisor/conf.d/coronacore-celery.conf
[INSERT DATA FROM FILE]
sudo nano /etc/supervisor/conf.d/coronacore-beat.conf
[INSERT DATA FROM FILE]

sudo supervisorctl reread
sudo supervisorctl update
~~~~

**Nginx**
~~~~

sudo apt install nginx

sudo nano /etc/nginx/sites-available/fectogram
[INSERT DATA FROM FILE]

sudo ln -s /etc/nginx/sites-available/fectogram /etc/nginx/sites-enabled
sudo nginx -t

sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx

sudo systemctl reload nginx

sudo ufw allow 'Nginx Full'

sudo certbot --nginx -d fectogram.com -d www.fectogram.com
sudo certbot --nginx -d app.fectogram.com -d www.app.fectogram.com
~~~~

**NPM**
~~~~

sudo apt-get install curl
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install nodejs
node -v 
npm -v

cd /home/ubuntu/dev/coronakoo-pwa
npm install
npm run build
~~~~


