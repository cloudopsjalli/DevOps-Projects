apt update
apt upgrade
sudo apt install build-essential libpcre3 libpcre3-dev libssl-dev zlib1g zlib1g-dev git -y
cd /home/ubuntu
wget http://nginx.org/download/nginx-1.24.0.tar.gz
tar -zxvf nginx-1.24.0.tar.gz
git clone https://github.com/arut/nginx-rtmp-module.git

cd nginx-1.24.0
./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
make
sudo make install
