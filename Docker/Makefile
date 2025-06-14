.PHONY: build run compose-up compose-down

build:
	docker build -t keila .

run:
	docker run --rm --privileged -p 5000:5000 keila

compose-up:
	docker-compose -f docker-compose-fastapi.yml up --build

compose-down:
	docker-compose -f docker-compose-fastapi.yml down