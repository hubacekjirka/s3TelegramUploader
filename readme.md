docker build . --tag hubacekjirka/s3telegramuploader

docker run --env-file .env -it hubacekjirka/s3telegramuploader


docker run -d --restart unless-stopped --env-file .env -it hubacekjirka/s3telegramuploader

curl ipinfo.io