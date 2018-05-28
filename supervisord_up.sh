
if [ ! -d "/var/run" ]; then
  sudo mkdir -p /var/run
fi

sudo touch /var/run/supervisor.sock
sudo unlink /var/run/supervisor.sock

sudo supervisord -c $(pwd)/supervisord.conf
