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

### Install Apache:
`sudo apt-get install apache2`


