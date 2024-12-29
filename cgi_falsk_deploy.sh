#!/usr/bin/env bash

# Script to create a virtual Python environment and install Flask

# Define variables
VENV_DIR="venv"
PYTHON_BIN="python3"
CURRENT_DIR=$(PWD)
HTACCESS_FILE=".htaccess"
CGI_START_FILE="cgi_serve.py"
INDEX_FILE="index.py"

# Check if Python is installed
if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "Error: $PYTHON_BIN is not installed. Please install Python 3."
    exit 1
fi

# Create the virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists in '$VENV_DIR'."
else
    echo "Creating virtual environment in '$VENV_DIR'..."
    $PYTHON_BIN -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
    echo "Virtual environment created successfully."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Error: Failed to upgrade pip."
    deactivate
    exit 1
fi

# Install Flask
echo "Installing Flask..."
pip install flask
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Flask."
    deactivate
    exit 1
fi

echo "Flask installed successfully."

# Deactivate the virtual environment
deactivate

mkdir public_html
cd public_html

echo "Creating .htaccess file to configure apache server"

cat > "$HTACCESS_FILE" <<EOL
SetEnv HOME

RewriteEngine On
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ cgi-bin/cgi_serve.py/\$1 [QSA,L]

DirectoryIndex cgi-bin/cgi_serve.py
Options +ExecCGI
AddHandler cgi-script .py
SetEnv PATH $CURRENT_DIR/venv/bin:\$PATH
SetEnv PYTHONPATH $CURRENT_DIR/venv/lib/python3.11/site-packages
EOL

mkdir cgi-bin
cd cgi-bin

echo "Creating cgi launching script"

cat > "$CGI_START_FILE" <<EOL
#!/usr/bin/env python3

from wsgiref.handlers import CGIHandler
from index import app

CGIHandler().run(app)

EOL

chmod +x $CGI_START_FILE

echo "Creating index file"

cat > "$INDEX_FILE" <<EOL
#!/usr/bin/python3

from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def hello_world():
    return 'Hello World from Python Flask!'

EOL







