

Add the following two keys to tfrs-minio-[env] secret
  root-user
  root-password
Deploy Minio per environment
  helm -n namespace -f ./values-env.yaml install itvr-minio-env oci://registry-1.docker.io/bitnamicharts/minio --version 14.1.7
Create Opensift routes 
  oc process -f ./itvr-routes.yaml ENV=env | oc create -f - -n namespace

