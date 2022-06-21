FROM artifacts.developer.gov.bc.ca/docker-remote/clamav/clamav:0.105_base
RUN chgrp -R root /var/log/clamav && \
    chmod -R g+w /var/log/clamav && \
    chgrp -R root /var/lib/clamav && \
    chmod -R g+w /var/lib/clamav