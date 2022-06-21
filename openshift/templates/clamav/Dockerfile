FROM artifacts.developer.gov.bc.ca/docker-remote/clamav/clamav:0.105_base
RUN ls -l /
RUN chgrp -R root /var/log/clamav && \
    chmod -R g+w /var/log/clamav && \
    chgrp -R root /var/lib/clamav && \
    chmod -R g+w /var/lib/clamav && \
    chgrp -R root /run && \
    chmod -R g+w /run
RUN ls -l /
RUN ls -l /run/clamav