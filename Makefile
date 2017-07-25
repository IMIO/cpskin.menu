#!/usr/bin/make
.PHONY: buildout cleanall test instance

bootstrap.py:
	wget http://downloads.buildout.org/2/bootstrap.py

bin/python:
	virtualenv-2.7 .
	touch $@

bin/buildout: buildout.cfg bin/python
	./bin/pip install zc.buildout==2.9.3
	touch $@

buildout: bin/buildout
	./bin/buildout -t 7

test: buildout
	./bin/test

jenkins: bin/buildout
	./bin/buildout -c jenkins.cfg

instance: buildout
	./bin/instance fg


cleanall:
	rm -rf bin develop-eggs downloads include lib parts .installed.cfg .mr.developer.cfg bootstrap.py parts/omelette
