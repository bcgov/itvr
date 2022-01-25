# Openshift

## Grant Developer's access
* Create the edit/admin RoleBinding for developers GitHub account, 
  - kind: User
    apiGroup: rbac.authorization.k8s.io
    name: <github username>@github
    
## Add role to group otherwise dev, test and prod can't pull images from tools
oc policy add-role-to-group system:image-puller system:serviceaccounts:ac294c-dev -n ac294c-tools
oc policy add-role-to-group system:image-puller system:serviceaccounts:ac294c-test -n ac294c-tools
oc policy add-role-to-group system:image-puller system:serviceaccounts:ac294c-prod -n ac294c-tools

## Keycloak
openshift/templates/keycloak/README.md

## Minio
openshift/templates/minio/README.md

## Patroni
openshift/templates/patroni-2.1.1/README.md

## Backend
openshift/templates/backend/README.md

## Frontend
openshift/templates/frontend/README.md

## Backup Container

