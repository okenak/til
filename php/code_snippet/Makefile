FILE="-v"
CMD="-v"
PWD=$(shell pwd)

.PHONY: php
php:
	docker run -it --rm -v ${PWD}:/app -w /app php:7.4-cli php ${FILE}

.PHONY: composer
composer:
	docker run -it --rm -v ${PWD}:/app -w /app composer ${CMD}