## CGI Flask Deploy Script

On my hosting plan they use a cgi server for python applications. 
They have no CPannel, so it took some tinkering to get my first Flask app running.

cgi_falsk_deploy.sh is an automated script to deploy a "hello world" Flask app.

## Getting Started

1. Prepare a hosting space and a domain where you intend to host the python app.
2. connect to your space via ssh
3. List your folders: ```ls -la``` That should show your configured domain directory.
4. run the script:
   ```sh
   curl https://raw.githubusercontent.com/ujagaga/cgi_flask_deploy/refs/heads/main/cgi_flask_deploy.sh -o cgi_flask_deploy.sh
   chmod +x cgi_flask_deploy.sh
   ./cgi_flask_deploy.sh
   ```

When asked input the domain you just configured. After this you should be able to see the "Hello from Flask" message on your domain, assuming DNS propagation is done, which may take up to 24 hours.

## What it does

1. Creates a folder structure and necessary apache configuration files:
```
├── venv
├── public_html
      ├── .htaccess
      └── cgi-bin
            ├── cgi_serve.py
            └── index.py
```
2. Installes a virtual environment with Flask package

## What now

Now you can navigate to your domain folder and activate the python virtual environment:

```source venv/bin/activate```

Then install all your necessary packages using pip and set up your app. 

## Contact

ujagaga@gmail.com

