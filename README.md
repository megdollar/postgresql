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
   


### Launch the VM:
1. Inside the Vagrant directory downloaded from the full-stack-nanodegree-vm run this command in your terminal
   `vagrant up`
2. Log in to the VM 
   `vagrant ssh`
3. Change directory to the files and look around
   `cd /vagrant' 'ls' `
   
### Set Up the Database:
1. Load the data in the local database
   `python database_setup.py`
2. Populate the database
   `python dreamFiles.py `

### Set up Google Login:
1. Log in to [Google Dev Console](https://console.developers.google.com/)
2. Go to Credentials
3. Select Create Crendentials > OAuth Client ID
4. Select Web Application
5. Enter name 'Dream Catalog'
6. Under 'Authorized Javascript Origins add' `http://localhost:5000/`
7. Authorized redirect URIs = 'http://localhost:5000/login' && 'http://localhost:5000/gconnect'
8. Click create client ID
9. Download JSON and save it as "client_secret.json" in the root directory (replace the existing)
10. In main.html replace the line "data-clientid="#####.apps.googleusercontent.com" so that it uses your Client ID from the web applciation.

### Set up Facebook Login:
1. Log in to [Facebook Dev Console](https://developers.facebook.com/)
2. Go to Dashboard
3. Click `Add Product` on the bottom left of the page
4. Add `facebook login`
5. Click Client OAuth
6. Add `http://localhost:5000/` to the Valid OAuth redirect URIs section
7. Replace app_id and app_secret in fb_client_secrets.json file

### Run the Application:
1. From the vagrant direcotry inside the VM
   `python project.py`
2. Navigate to [http://localhost:5000/](http://localhost:5000/) in your browser

### Exiting the VM
To exit type `control + D`
