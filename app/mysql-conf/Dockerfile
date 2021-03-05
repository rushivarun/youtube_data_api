# Derived from official mysql image (our base image)
FROM mysql
# Add a database
ENV MYSQL_ROOT_PASSWORD=my_secret_pw
# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./files/ /docker-entrypoint-initdb.d/