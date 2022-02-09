FILE_LIST = ./.installed_files.txt

.PHONY: build clean install publish pull push uninstall

build:
	@ python ./setup.py sdist bdist_wheel

clean:
	@ rm -Rf ./build ./dist

default: | pull clean install

install:
	@ python ./setup.py install --record $(FILE_LIST)

publish:
	@ twine upload dist/*

pull:
	@ git pull

push:
	@ git push

pypi: | clean build publish

uninstall:
	@ while read FILE; do echo "Removing: $$FILE"; rm "$$FILE"; done < $(FILE_LIST)
