<h1 align="center">Welcome to S3 Telegram Uploader repo 👋</h1>
<img src="https://github.com/hubacekjirka/s3TelegramUploader/workflows/Build%20and%20push%20from%20the%20main%20branch/badge.svg"/>

> The bot is a supportive application for the [Photo Of The Day app](https://github.com/hubacekjirka/dailyPhotoTwitterBot). Its purpose is to simplify the photo upload process to a simple conversation with a bot over Telegram.

> A CI process automatically kicks in on commit to the main branch. It launches Docker's buildx command for multi-arch builds. My bot instance runs on Raspberry Pi.

> Upload process: 

> <img src="https://raw.githubusercontent.com/hubacekjirka/s3TelegramUploader/master/bot.jpeg" width="35%" height="35%"/>


## Usage
Rename .env_example to .env and fill in the values.


### Docker
Navigate to the repo's directory and run the following command
```sh
docker run -d --restart unless-stopped --env-file .env hubacekjirka/s3-telegram-uploader:latest
```

### Docker-compose
Navigate to the repo's directory and run the following command
```sh
docker-compose up -d --remove-orphans
```

### Auto pulling
Automatic pulling of the docker image from docker hub may be scheduled as a cron job. The job would invoke the docker_auto_pull.sh script.

## Author

👤 **jiri hubacek**

* Web: [Blog](https://blog.hubacek.uk)
* Twitter: [@hubacekjirka](https://twitter.com/hubacekjirka)
* Github: [@hubacekjirka](https://github.com/hubacekjirka)


## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [jiri hubacek](https://github.com/hubacekjirka).<br />
This project is [MIT](https://github.com/hubacekjirka/dailyPhotoTwitterBot/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
