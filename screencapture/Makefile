all: clean build

build:
	cd src ; \
	zip ../screencapture.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm -f *.alfredworkflow

update-lib:
	pip install -d ./ Alfred-Workflow
	tar xzvf Alfred-Workflow-*.tar.gz
	cp -r Alfred-Workflow-*/workflow src/
	rm -rf Alfred-Workflow-*