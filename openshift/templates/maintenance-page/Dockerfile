FROM artifacts.developer.gov.bc.ca/docker-remote/httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
RUN chgrp -R root /usr/local/apache2/logs \
    && chmod -R g+w /usr/local/apache2/logs