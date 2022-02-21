build:
	docker build . -t hubacekjirka/s3telegramuploader:latest

run_debug:
	# Remove contianer if it already exists
	docker container rm s3uploader_debug -f

	# Run container without launching the app.py
	docker run \
	--interactive \
	--detach \
	--name s3uploader_debug \
	--env-file .env \
	hubacekjirka/s3telegramuploader:latest \
	/bin/bash
