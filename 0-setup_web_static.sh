#!/usr/bin/env bash
# Sets up a web server for the deployment of web_static

# Install Nginx if it is not already installed
if ! command -v nginx > /dev/null 2>&1; then
    apt-get update -y
    apt-get install -y nginx
fi

# Create the folders (-p: no error if they already exist)
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test the Nginx configuration
cat > /data/web_static/releases/test/index.html << 'HTML'
<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>
HTML

# Create the symbolic link (deleted and recreated on every run)
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group (recursive)
chown -R ubuntu:ubuntu /data/

# Serve /data/web_static/current/ at /hbnb_static (only add it once)
CONFIG="/etc/nginx/sites-enabled/default"
if [ -f "$CONFIG" ] && ! grep -q "location /hbnb_static" "$CONFIG"; then
    sed -i '0,/server_name .*;/s//&\n\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}/' "$CONFIG"
fi

# Restart Nginx
service nginx restart

exit 0
