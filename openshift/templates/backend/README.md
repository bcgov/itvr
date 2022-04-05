### Files included
    * backend-bc.yaml backend build config
    * backend-dc.yaml backend deployment config
    * django-secret-template.yaml create template.django-secret, it is not in pipeline and needs to run independently, it is used by backend-dc.yaml
    * backend-autoscaler.yaml create backend autoscaler, it is not in pipeline and needs to run independently

### Prepare for pipeline build and deploy

#### Before triggering pipeline

1. import python base image python-39:1-18.1634036280 to tools project

2. Create template secret template.django-secret

3. create user for itvr database, create user [username] with password '[password]';

4. create itvr database in patroni cluster, create database itvr owner [username] ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8'; 

5. create secret itvr-patroni-app

6. create template.django-secret

7. create itvr-email-service secret

#### After pipeline completes

1. After pipeline completes, create autoscaler for backend
