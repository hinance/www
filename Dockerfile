FROM hinance/hinance:1.1.0draft-2015-09-01
ADD hinance-www /hinance-www
WORKDIR /hinance-www
RUN ["bash", "-l", "/hinance-www/setup/setup.sh"]
