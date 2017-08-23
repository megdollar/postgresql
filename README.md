# DreamApp

### About the Dream App:
Built as part of the [Udacity's Full Stack Nanodegree](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/262a84d7-86dc-487d-98f9-648aa7ca5a0f/concepts/079be127-2d22-4c62-91a8-aa031e760eb0) this is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates dream categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Hosted on Amazon Lightsail using an Ubuntu instance.

### Server Details:
* IP address: `18.220.131.73`
* URL: `http://ec2-18-220-131-73.us-east-2.compute.amazonaws.com/dreams/?category_id=8#`
* SSH PORT: 2200

### Getting Setup:
1. Initially connect with instance after downloading default key pair:
   `ssh -i ~/Downloads/LightsailDefaultPrivateKey-us-east-2.pem ubuntu@18.220.131.73`
2. Change Privellages so group and order cannot read the key pair:
   `chmod go -r ~/Downloads/LightsailDefaultPrivateKey-us-east-2.pem`
3. Updates:
   * Update package source list: `sudo apt-get update`
   * Update software: `sudo apt-get upgrade`
   * Remove any unneccesary packages: `sudo apt-get autoremove`
4. Install finger
   `sudo apt-get install finger`
5. Create new user 'Grader':
   `sudo add user grader`
   add password
6. Give user grader to sudo group
   `sudo usermod -aG sudo grader`
7. Switch to user
   `su -grader`

### Add Key-based Authentication:
*You will need two terminal windows, one as grader logged into instance and one local outside of the server*
1. Generate key in local machine (outside of ubuntu)
   `ssh-keygen`
   * When prompted, save file to: /users/'yourusername'/.ssh/lightsailApp
   * Add passphrase: 'udacity course'
2. Add public key to remote server, as grader logged into server type:
   `mkdir .ssh`
   `touch .ssh/authorized_keys`
3. Copy the files from local dir `.ssh/lightsailApp.pub` into the file `.ssh/authorized_keys` in the server
4. Add security file permissions for grader
   `chmod 700 .ssh`
   `chmod 644 .ssh/authorized_keys`
5. Log in as grader using this command:
   `ssh grader@18.220.131.73 -p22 -i ~/.ssh/lightsailApp`

### Change Port & Disable Password Login:
*Add custom tcp 2200 port to Lightsail application*
1. Navigate to sshd_config
   `sudo nano /etc/ssh/sshd_config`
   *Change line `Port 22` to `Port 2200`*
   *Uncomment line `PasswordAuthentication no`*
2. Restart sshd service
  `servce ssh restart`
3. Log in with new port
   `ssh grader@18.220.131.73 -p2200 -i ~/.ssh/lightsailApp`
   
### Configure Firewall:
1. Block all incoming ports
   `sudo ufw default deny incoming`
2. Allow outgoing connections on all ports
   `sudo ufw allow outgoing`
3. Allow incoming connections for SSH on port 2200:
   `sudo ufw allow 2200/tcp`
4. Allow incoming connections for HTTP on port 80:
   `sudo ufw allow 80/tcp`
   `sudo ufw allow www`
5. Allow UDP 123:
   `sudo allow 123/udp`
6. Double check the rules before enabling
   `sudo ufw show added`
7. Enable firewall
   `sudo ufw enable`
8. Check status
   `sudo ufw status`

### Change Timezone to UTC:
`sudo dpkg-reconfigure tzdata`
Select time

### Install Apache & WSGI:
`sudo apt-get install apache2`
`sudo 2enmod wsgi`
* The next steps relied heavily on this [DigitalOcean tutorial](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps#step-four-%E2%80%93-configure-and-enable-a-new-virtual-host), although the steps with implementing a virtual environment were omitted. Follow the tutorial. *

### Install PostgreSQL:
`sudo apt-get install postgresql`
1. Log into Postgres
   `sudo -u postgresql psql`
2. Create new user 'catalog'
   `CREATE USER catalog WITH PASSWORD 'xxxxx';` (enter password)
3. Create DB and give ownership to catalog user
   `CREATE DATABASE dreamApp OWNER catalog;`
4. Allow catalog user to Create, read, update, delete
   `GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA PUBLIC TO catalog;`

### Exit postgres and make further changes:
1. Ensure remote connections to PostgreSQL are not allowed
   `sudo nano /etc/postgresql/9.5/main/pg_hba.conf` 
   * Change the line that says local all all peer, to local all all md5*
2. Remove old .conf file
   `sudo a2dissite /etc/apache2/sites-enables/000-default.conf`
3. Restart postgres & apache
   `sudo service postgresql restart`
   `sudo service apache2 restart`
4. Install flask, SQLALlchemy, etc:
   `sudo apt-get install python-psycopg2 python-flask`
   `sudo apt-get install python-sqlalchemy python-pip`
   `sudo pip install oauth2client`
   `sudo pip install requests`
   `sudo pip install httplib2`
5. Install git
   `sudo apt-get install git`

### Use GIT to clone the repository for the catalog app:
1. Logged in as grader cd to the second level app
   `cd /var/www/DreamApp/DreamApp`
    `git init`
    `git remote add origing 'xxxx'` (path to repo)
    `git fetch`
    `git reset origin/master`
    `git checkout -t origin master`

### Change reference to locations in __init__.py:
1. Change to  `/var/www/DreamApp/DreamApp/'xxxx'` use this for any references to path in the file

### Update .wsgi File:
1. change 'Server Name' to the DNS `ec2-18-220-131-73.us-east.compute-1.amazonaws.com` 
2. The catalog app should now be available at `http://18-220-131-73` and `http://ec2-18-220-131-73.us-east-2.compute.amazonaws.com`

### Update Google OAuth client secrets:
1. Also change the javascript_origins field to the IP address and AWS assigned URL of the host. In this instance that would be: "javascript_origins":["http://18.220.131.73", "http://ec2-18-220-131-73.us-east-2.compute.amazonaws.com"]
2. Fill in the `client_id` and `client_secret` fields in the file `client_secrets.json`. 

* These addresses also need to be entered into the Google Developers Console -> API Manager -> Credentials, in the web client under "Authorized JavaScript origins". *

### Update Facebook OAuth client secrets:
1. In the Facebook developers website, in the "Advanced" tab, in the "Client OAuth Settings" section, add http://ec2-18-220-131-73.us-west-2.compute.amazonaws.com and http://18-220-131-73 to the "Valid OAuth redirect URIs" field. Then save these changes.
2. In the file `fb_client_secrets.json`, fill in the `app_id` and `app_secret` fields with the correct values.

### App specific changes:
1. In order to allow image uploads, change ownership of directory `/images/uploads` to the www-user:
   `sudo chown www-data:www-data /var/www/DreamApp/DreamApp/images/uploads`
   





