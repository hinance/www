# Hinance Homepage

Homepage build automation for [hinance](http://www.hinance.org).
This is a reproducible build: all dependencies versions are frozen.
Among other things, it builds the example bookkeeping reports using the actual
program code, so it can be used as a reference when building
[hinance](https://github.com/hinance/hinance).
In the end it deploys everything to the Git repo.

## How to Build

Install [Docker](https://www.docker.com/).

Clone this repo:
   `git clone https://github.com/hinance/www <<<path-to-repo>>>`

Create config file at `/etc/hinance-www/config.sh`:
```
URL='<<<www.hinance.org>>>'
GIT_REPO='<<<git@github.com:hinance/hinance.github.io.git>>>'
GIT_USER='<<<James T. Kirk>>>'
GIT_EMAIL='<<<kirk@enterprise.uss>>>'
ID_RSA_PUB='<<<public ssh rsa key to access to the git repo>>>'
ID_RSA='<<<private ssh rsa key to access to the git repo>>>'
```

Run `<<<path-to-repo>>>/run.sh`

## License

The contents of this repo is licensed under MIT License.

## Contact

Oleg Plakhotniuk: contact@hinance.org
