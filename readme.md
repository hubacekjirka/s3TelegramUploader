docker build . --tag hubacekjirka/s3telegramuploader

docker run --env-file .env -it hubacekjirka/s3telegramuploader


docker run -d --restart unless-stopped --env-file .env -it hubacekjirka/s3telegramuploader

curl ipinfo.io



# GitHub Runner
Credits:
- [GitHub blog](https://github.blog/2020-08-04-github-actions-self-hosted-runners-on-google-cloud/)
## x64 Architecture
Docker Build
```sh
docker build -t hubacekjirka/github_runner_x64 -f ./github_runner.dockerfile .
```

Running container
```sh
docker run --detach --env-file .env_github_runner_x64 hubacekjirka/github_runner_x64
```

Stopping container
```sh
docker stop <container id>
```
Stopping the container gracefully is important is the runner needs to reregister itself.

## ARM32 Architecture
TBD