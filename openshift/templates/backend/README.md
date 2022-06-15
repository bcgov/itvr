### Files included
    * backend-bc.yaml backend build config
    * backend-dc.yaml backend deployment config
    * django-secret-template.yaml create template.django-secret, it is not in pipeline and needs to run independently, it is used by backend-dc.yaml
    * backend-autoscaler.yaml create backend autoscaler, it is not in pipeline and needs to run independently

### Prepare for pipeline build and deploy

#### Before triggering pipeline

1. import python base image python-39:1-18.1634036280 to tools project

2. Create template secret template.django-secret, template.django-salt

3. create secret itvr-patroni-app, itvr-email-service, itvr-object-storage and itvr-superuser(prod only)

4. create user for itvr database, create user [username] with password '[password]'

5. create itvr database in patroni cluster, create database itvr owner [username] ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8'

6. login to spilo pods, run the following psql to only keep 24 hours log files, otherwise they take too much space
    ALTER SYSTEM SET log_filename='postgresql-%H.log';
    ALTER SYSTEM SET log_connections='off';
    ALTER SYSTEM SET log_disconnections='off';
    ALTER SYSTEM SET log_checkpoints='off';
    select pg_reload_conf();

#### After pipeline completes

1. After pipeline completes, create autoscaler for backend

2. run "python manage.py createsuperuser" on backend pod