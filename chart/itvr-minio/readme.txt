

Add the following two keys to tfrs-minio-[env] secret
  root-user
  root-password
helm -n namespace -f ./values-dev.yaml install itvr-minio-dev oci://registry-1.docker.io/bitnamicharts/minio --version 14.1.7
Create Opensift route tfrs-minio-console-dev
Update the existing route tfrs-minio-dev to use the newly created service itvr-minio api port