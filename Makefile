all: install build

deps/install:
	pip install -r requirements.txt
deps/reqs:
	pipreqs . --savepath requirements.prod.txt
deps/freeze:
	python -m pip freeze > requirements.txt
deps/outdated:
	python -m pip list --outdated
deps/check:
	python -m pip check

run/transitbroker:
	python pkgs/transitbroker/transitbroker/cli.py local /tmp/foo
run/transitctl:
	python pkgs/transitctl/transitctl/cli.py $(ARGS)
run/transitconsole:
	python pkgs/transitconsole/transitconsole/cli.py

format:
	python -m ruff format .

lint:
	python -m ruff check .

test: test/transitbroker test/transitclient test/transitctl test/transitconsole
test/%:
	pytest pkgs/$*/$*

coverage: coverage/transitbroker coverage/transitclient coverage/transitctl coverage/transitconsole
coverage/%:
	pytest --cov pkgs/$*/$*

build: build/transitbroker build/transitctl build/transitconsole
build/%:
	pyinstaller \
		--workpath pkgs/$*/build \
		--distpath pkgs/$*/dist \
		--specpath pkgs/$* \
		--name $* \
		--onefile \
		pkgs/$*/$*/cli.py

exec/%:
	./pkgs/$*/dist/$* $(ARGS)

clean: clean/transitctl clean/transit
clean/%:
	rm -rf pkgs/$*/build
	rm -rf pkgs/$*/dist
	rm -rf pkgs/$*/*.spec

compose.build:
	docker compose build
compose.up:
	docker compose up

ollama/start:
	ollama start
