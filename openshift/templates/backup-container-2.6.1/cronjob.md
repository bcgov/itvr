# Cronjob prerequisites
Backup PVC: backup
KNP: allow CronJob to connect to Spilo

## Create database backup cronjob
oc process -f ./db-backup-cronjob-2.6.1.yaml \
JOB_NAME=itvr-db-backup \
JOB_PERSISTENT_STORAGE_NAME=backup \
SCHEDULE="00 08,20 * * *" \
TAG_NAME=2.6.1 \
DATABASE_SERVICE_NAME=itvr-crunchy-[env]-replicas \
DATABASE_DEFAULT_PORT=5432 \
DATABASE_NAME=itvr \
DATABASE_DEPLOYMENT_NAME=itvr-patroni-app \
DATABASE_USER_KEY_NAME=app-db-username \
DATABASE_PASSWORD_KEY_NAME=app-db-password \
BACKUP_STRATEGY=rolling \
BACKUP_DIR=/backups \
DAILY_BACKUPS=30 \
WEEKLY_BACKUPS=8 \
MONTHLY_BACKUPS=2 | oc apply -f - -n <namespace>


