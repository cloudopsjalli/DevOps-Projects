===============================================================================================
1.Launch an EC2 instance
==============================================================================================
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

===============================================================================================
configuring ngnix server
===============================================================================================


cp /usr/local/nginx/conf/nginx.conf nginx.conf.bak
sudo vim /usr/local/nginx/conf/nginx.conf 
:%d --- enter " copy this code"
==============================================================================================

worker_processes  auto;

events {
    worker_connections  1024;
}

rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application live {
            live on;
            record off;
        }
    }
}

http {
    server {
        listen 8080;

        location / {
            root html;
        }
    }
}

sudo /usr/local/nginx/sbin/nginx -s reload
=====================================================================

start nginx
=====================================================================

1.sudo /usr/local/nginx/sbin/nginx
2.ps -ef | grep nginx
3.sudo netstat -lntp | grep nginx

now open inbound ports
1935 and 8080
Launch the url http://pubicip:8080

sudo tail -f /usr/local/nginx/logs/error.log
sudo tail -f /usr/local/nginx/logs/access.log
sudo netstat -plant | grep 1935
sudo ss -ltnp | grep 1935
sudo netstat -an | grep 1935

========================================================================
--->Modify the conf file and add the below hls lines.
=====================================================================
sudo vim /usr/local/nginx/conf/nginx.conf


rtmp {
    server {
        listen 1935;
        chunk_size 4096;

        application live {
            live on;
            record off;

            hls on;
            hls_path /usr/local/nginx/html/hls;
            hls_fragment 3;
            hls_playlist_length 9;
        }
    }
}

=====================================================
sudo mkdir -p /usr/local/nginx/html/hls
sudo chmod -R 755 /usr/local/nginx/html/hls
=====================================================
update the http{} block

server {
    listen 8080;

    location /hls {
        types {
            application/vnd.apple.mpegurl m3u8;
            video/mp2t ts;
        }
        root /usr/local/nginx/html;
    }
}
======================================================
sudo /usr/local/nginx/sbin/nginx -s reload

ls /usr/local/nginx/html/hls  =========> you should see

classroom.m3u8
classroom0.ts
classroom1.ts
classroom2.ts

=========================================
http://<EC2_PUBLIC_IP>:8080/hls/classroom.m3u8
======================================================
pushing  the files to S3

========================================================

aws  --version
sudo apt install awscli
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

unzip awscliv2.zip
sudo ./aws/install
aws --version
==============================================================================

Create s3 bucket
create a folder in /hls


===============================================================================
create a script which will copy the contents of files to s3.

#!/bin/bash

while true
do
  aws s3 sync /usr/local/nginx/html/hls s3://streamingjalli01/hls --delete
  sleep 10
done

4.s3://streamingjalli01/hls/
5.create an index.html as below
6.create static website hosting
7.ublock public access
8.Dont update bucket policy and you will get 403 error
8.update bucket policy

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::streamingjalli01/*"
        }
    ]
}

================================================================================

http://"your s3 bucket-ast-1.amazonaws.com/hls/classroom.m3u8

===============================================================================

cloud front distribution

1.cloud font distribution
2.stop public access
3.create a cloudfront distribution
4.select the bucket as origin: streamingjalli01.s3.us-east-1.amazonaws.com
5.disable waf
6.deploy, all settings are default
7.edit the policy which cloudfront creates and then copy that policy in the S3 bucket policy.
8.use the stream : https://xxxxxxxx.cloudfront.net/hls/classroom.m3u8

sample bucket policy will be like 

{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::streamingjalli01/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::570116614705:distribution/E3LYWLDEMTNW7P"
                }
            }
        }
    ]
}

================================================================================================================

================================================================================================================

Troubleshooting
================================================================================================================
create behviors for dark screen

You separated behaviors:

Behavior 1 — *.m3u8

TTL = 0 (or caching disabled)

Always fetch fresh playlist from S3

Behavior 2 — *.ts

Cached for 60–300 seconds(TTL = 60, Max = 300)--->create a custom cache profile.

Reduces S3 load

Improves performance

This is exactly how production streaming CDNs are configured.

===================================================================================================================
