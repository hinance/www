FROM hinance/hinance:0.0.0-2015-03-12
ADD hinance-www /hinance-www
WORKDIR /hinance-www
RUN ["bash", "-l", "/hinance-www/setup/setup.sh"]
