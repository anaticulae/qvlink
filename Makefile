.PHONY: docker-build docker-run build clean

VERSION := $(shell git rev-parse --short HEAD 2>/dev/null || echo "latest")
CURDIR := $(CURDIR)

NAME = qvlink
IMAGE := ghcr.io/anaticulae/$(NAME):$(VERSION)

docker-build:
	docker build -t $(IMAGE) .

docker-upload:
	docker push $(IMAGE)

docker-doctest: docker-build
	docker run\
		-v $(CURDIR):/var/workdir\
		-v /tmp/qvlink:/tmp/qvlink\
		$(IMAGE)\
		"baw test docs"

docker-fasttest: docker-decrypt
	docker run\
		-v $(CURDIR):/var/workdir\
		-v /tmp/qvlink:/tmp/qvlink\
		-e HOVERPOWER_STORE=/var/workdir/hoverpower/repo\
		-e HOVERPOWER_SECRET\
		$(IMAGE)\
		"baw test fast"

docker-longtest: docker-decrypt
	docker run\
		-v $(CURDIR):/var/workdir\
		-v /tmp/qvlink:/tmp/qvlink\
		-e HOVERPOWER_STORE=/var/workdir/hoverpower/repo\
		-e HOVERPOWER_SECRET\
		$(IMAGE)\
		"baw test long"

docker-alltest: docker-decrypt
	docker run\
		-v $(CURDIR):/var/workdir\
		-v /tmp/qvlink:/tmp/qvlink\
		-e HOVERPOWER_STORE=/var/workdir/hoverpower/repo\
		-e HOVERPOWER_SECRET\
		$(IMAGE)\
		"baw test all"

docker-lint: docker-build
	docker run\
		-v $(CURDIR):/var/workdir\
		$(IMAGE)\
		"baw lint all"

docker-decrypt: docker-build
	docker run\
		-v $(CURDIR):/var/workdir\
		-v /tmp/qvlink:/tmp/qvlink\
		-e HOVERPOWER_STORE=/var/workdir/hoverpower/repo\
		-e HOVERPOWER_SECRET\
		$(IMAGE)\
		"powerdownload && powerdecrypt"

docker-release: docker-build
	@if git describe --exact-match --tags HEAD >/dev/null 2>&1; then\
		echo "Current commit is already tagged. Skipping release.";\
	else \
		docker run\
			-v $(CURDIR):/var/workdir\
			-e GH_TOKEN\
			$(IMAGE)\
			"baw release --no_test --no_linter";\
	fi
