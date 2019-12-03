# Simple mocked http server

Simple http server which will respond with configurable error-ratio.
Requests will be served from defined files.
This will serve success and error responses defined in files.
It also sends headers defined in file.

## Why

To pick up some basic server programming skills in python and get a bit more familiar with HTTPServer class.
There are ready to use solutions like http://wiremock.org

## How to run

* [Dockerfile](Dockerfile)
* Sample responses [success.json](success.json) and [error.json](error.json) (success and error responses are the same)
