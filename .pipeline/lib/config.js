'use strict';
const options= require('@bcgov/pipeline-cli').Util.parseArguments()
const changeId = options.pr //aka pull-request
const version = '1.0.0'
const name = 'itvr'
const ocpName = 'apps.silver.devops'

//if work directly on bcgov repo, the value is bcgov
//if work on forked developer repo, the value is the developer's GitHub Id
//without this line of code, the pr deployment cann't removed when the pr is closed

/*
Resource usage base:

Name        CPU         Memory
backend     40m          520M
frontend    70m         500M
superset    1m          180M
metabase    130m         820M
patroni     70m         410M
redis       2m          20M
Minio       3m          150M
backup      1m          20M

Set the cpu usage 20m as the lowest
Set the limit as two times of request
electric-vehicle-rebates.gov.bc.ca
*/
options.git.owner='bcgov'
//Have to set options.git.repository to be itvr otherwise an error will be thrown as the label github-repo 
//will contain https://github.com/bcgov/itvr which is not allowed as a valid label
options.git.repository='itvr'

const phases = {

  build: {namespace:'ac294c-tools'   , transient:true, name: `${name}`, phase: 'build', 
          changeId:`${changeId}`, suffix: `-build-${changeId}`  , instance: `${name}-build-${changeId}`, 
          version:`${version}-${changeId}`, tag:`build-${version}-${changeId}`, ocpName: `${ocpName}`},

  dev: {namespace:'ac294c-dev', transient:true, name: `${name}`, ssoSuffix:'-dev', 
        ssoName:'dev.oidc.gov.bc.ca', phase: 'dev'  , changeId:`${changeId}`, suffix: `-dev-${changeId}`, 
        instance: `${name}-dev-${changeId}`  , version:`${version}-${changeId}`, tag:`dev-${version}-${changeId}`, 
        host: `itvr-dev-${changeId}.${ocpName}.gov.bc.ca`, djangoDebug: 'True', logoutHostName: 'logontest.gov.bc.ca',
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        frontendCpuRequest: '30m', frontendCpuLimit: '60m', frontendMemoryRequest: '30Mi', frontendMemoryLimit: '60Mi', frontendReplicas: 1, snowplowCollector: '',
        reactAppBCSCKeycloakClientId: 'itvr', reactAppBCSCKeycloakRealm: 'rzh2zkjq', reactAppBCSCKeycloakUrl: 'https://dev.oidc.gov.bc.ca/auth/', reactAppApiBase: `https://itvr-backend-dev-${changeId}.apps.silver.devops.gov.bc.ca`, 
        reactAppBCeIDKeycloakClientId: 'itvr-on-gold-cluster-3972', reactAppBCeIDKeycloakRealm: 'standard', reactAppBCeIDKeycloakUrl: 'https://dev.loginproxy.gov.bc.ca/auth/', 
        backendCpuRequest: '60m', backendCpuLimit: '120m', backendMemoryRequest: '150Mi', backendMemoryLimit: '300Mi', backendHealthCheckDelay: 30, backendHost: `itvr-backend-dev-${changeId}.${ocpName}.gov.bc.ca`, backendReplicas: 1, backendDjangoDebug: 'True', bucketName: 'itvrdv', craEnvironment: 'A', corsOriginWhitelist: 'https://itvr-dev.apps.silver.devops.gov.bc.ca', 
        minioCpuRequest: '30m', minioCpuLimit: '100m', minioMemoryRequest: '150Mi', minioMemoryLimit: '300Mi', minioPvcSize: '3Gi',
        schemaspyCpuRequest: '50m', schemaspyCpuLimit: '200m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '1G', rabbitmqPvcSize: '1G', rabbitmqReplica: 1, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '60m', patroniCpuLimit: '120m', patroniMemoryRequest: '200Mi', patroniMemoryLimit: '400Mi', patroniPvcSize: '2G', patroniReplica: 2, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`,
        taskQueueCpuRequest: '60m', taskQueueCpuLimit: '120m', taskQueueMemoryRequest: '200Mi', taskQueueMemoryLimit: '400Mi', taskQueueReplicas: 1, taskQueueDjangoDebug: 'True',},

  test: {namespace:'ac294c-test', name: `${name}`, ssoSuffix:'-test', 
        ssoName:'test.oidc.gov.bc.ca', phase: 'test'  ,  changeId:`${changeId}`, suffix: `-test`, 
        instance: `${name}-test`, version:`${version}`, tag:`test-${version}`, 
        host: `itvr-test.${ocpName}.gov.bc.ca`, djangoDebug: 'False', logoutHostName: 'logontest.gov.bc.ca',
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        frontendCpuRequest: '30m', frontendCpuLimit: '60m', frontendMemoryRequest: '30Mi', frontendMemoryLimit: '60Mi', frontendReplicas: 2, frontendMinReplicas: 1, frontendMaxReplicas: 3, snowplowCollector: 'spm.apps.gov.bc.ca',
        reactAppBCSCKeycloakClientId: 'itvr', reactAppBCSCKeycloakRealm: 'rzh2zkjq', reactAppBCSCKeycloakUrl: 'https://test.oidc.gov.bc.ca/auth/', reactAppApiBase: `https://itvr-backend-test.apps.silver.devops.gov.bc.ca`,
        reactAppBCeIDKeycloakClientId: 'itvr-on-gold-cluster-3972', reactAppBCeIDKeycloakRealm: 'standard', reactAppBCeIDKeycloakUrl: 'https://test.loginproxy.gov.bc.ca/auth/',
        backendCpuRequest: '60m', backendCpuLimit: '120m', backendMemoryRequest: '150Mi', backendMemoryLimit: '300Mi', backendHealthCheckDelay: 30, backendReplicas: 2, backendMinReplicas: 1, backendMaxReplicas: 3, backendHost: `itvr-backend-test.${ocpName}.gov.bc.ca`, backendDjangoDebug: 'False', bucketName: 'itvrts', craEnvironment: 'A', corsOriginWhitelist: 'https://itvr-test.apps.silver.devops.gov.bc.ca', 
        minioCpuRequest: '30m', minioCpuLimit: '100m', minioMemoryRequest: '150Mi', minioMemoryLimit: '300Mi', minioPvcSize: '3G',
        schemaspyCpuRequest: '20m', schemaspyCpuLimit: '200m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '700M', rabbitmqPvcSize: '1G', rabbitmqReplica: 2, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '60m', patroniCpuLimit: '120m', patroniMemoryRequest: '200Mi', patroniMemoryLimit: '400Mi', patroniPvcSize: '5G', patroniReplica: 2, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`,
        taskQueueCpuRequest: '60m', taskQueueCpuLimit: '120m', taskQueueMemoryRequest: '200Mi', taskQueueMemoryLimit: '400Mi', taskQueueReplicas: 1, taskQueueDjangoDebug: 'False',},

  prod: {namespace:'ac294c-prod', name: `${name}`, ssoSuffix:'', 
        ssoName:'oidc.gov.bc.ca', phase: 'prod'  , changeId:`${changeId}`, suffix: `-prod`, 
        instance: `${name}-prod`, version:`${version}`, tag:`prod-${version}`, 
        metabaseCpuRequest: '200m', metabaseCpuLimit: '300m', metabaseMemoryRequest: '500Mi', metabaseMemoryLimit: '2Gi', metabaseReplicas: 1,
        host: `itvr-prod.${ocpName}.gov.bc.ca`, djangoDebug: 'False', logoutHostName: 'logon7.gov.bc.ca',
        frontendCpuRequest: '30m', frontendCpuLimit: '60m', frontendMemoryRequest: '30Mi', frontendMemoryLimit: '60Mi', frontendReplicas: 2, frontendMinReplicas: 2, frontendMaxReplicas: 5, snowplowCollector: 'spt.apps.gov.bc.ca',
        reactAppBCSCKeycloakClientId: 'itvr', reactAppBCSCKeycloakRealm: 'rzh2zkjq', reactAppBCSCKeycloakUrl: 'https://oidc.gov.bc.ca/auth/', reactAppApiBase: `https://itvr-backend-prod.apps.silver.devops.gov.bc.ca`,
        reactAppBCeIDKeycloakClientId: 'itvr-2674', reactAppBCeIDKeycloakRealm: 'onestopauth-basic', reactAppBCeIDKeycloakUrl: 'https://oidc.gov.bc.ca/auth/',
        backendCpuRequest: '60m', backendCpuLimit: '120m', backendMemoryRequest: '150Mi', backendMemoryLimit: '300Mi', backendHealthCheckDelay: 30, backendReplicas: 3, backendMinReplicas: 3, backendMaxReplicas: 5, backendHost: `itvr-backend-prod.${ocpName}.gov.bc.ca`, backendDjangoDebug: 'False', bucketName: 'itvrpr', craEnvironment: 'P', corsOriginWhitelist: 'https://electric-vehicle-rebates.gov.bc.ca', 
        minioCpuRequest: '30m', minioCpuLimit: '100m', minioMemoryRequest: '150Mi', minioMemoryLimit: '300Mi', minioPvcSize: '3G',
        schemaspyCpuRequest: '50m', schemaspyCpuLimit: '400m', schemaspyMemoryRequest: '150M', schemaspyMemoryLimit: '300M', schemaspyHealthCheckDelay: 160,
        rabbitmqCpuRequest: '250m', rabbitmqCpuLimit: '700m', rabbitmqMemoryRequest: '500M', rabbitmqMemoryLimit: '1G', rabbitmqPvcSize: '5G', rabbitmqReplica: 2, rabbitmqPostStartSleep: 120, storageClass: 'netapp-block-standard',
        patroniCpuRequest: '60m', patroniCpuLimit: '120m', patroniMemoryRequest: '200Mi', patroniMemoryLimit: '400Mi', patroniPvcSize: '5G', patroniReplica: 3, storageClass: 'netapp-block-standard', ocpName: `${ocpName}`,
        taskQueueCpuRequest: '60m', taskQueueCpuLimit: '120m', taskQueueMemoryRequest: '200Mi', taskQueueMemoryLimit: '400Mi', taskQueueReplicas: 1, taskQueueDjangoDebug: 'False',}

};

// This callback forces the node process to exit as failure.
process.on('unhandledRejection', (reason) => {
  console.log(reason);
  process.exit(1);
});

module.exports = exports = {phases, options};
