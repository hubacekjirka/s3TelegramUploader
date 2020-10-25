<h1 align="center">Welcome to S3 Telegram Uploader repo 👋</h1>

> The bot is a supportive application for the [Photo Of The Day app](https://github.com/hubacekjirka/dailyPhotoTwitterBot). It's purpose it to simplify photo upload process to a simple conversation with a bot over Telegram.

> Upload process: 

> <img src="https://raw.githubusercontent.com/hubacekjirka/s3TelegramUploader/docker-compose/bot.jpeg" width="50%" height="50%"/>

### 🏠 [Homepage](http://blog.hubacek.uk)

## Usage
Rename .env_example to .env and fill in the values.


### Docker
Running using Docker
```sh
docker run -d --restart unless-stopped --env-file .env hubacekjirka/s3-telegram-uploader:latest
```

### Docker-compose
Navigate to the repo's directory and run the following command
```sh
docker-compose up -d --remove-orphans
```

## Author

👤 **jiri hubacek**

* Twitter: [@hubacekjirka](https://twitter.com/hubacekjirka)
* Github: [@hubacekjirka](https://github.com/hubacekjirka)


## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [jiri hubacek](https://github.com/hubacekjirka).<br />
This project is [MIT](https://github.com/hubacekjirka/dailyPhotoTwitterBot/blob/master/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
