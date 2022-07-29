"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");
const path = require("path");
//const KeyCloakClient = require('./keycloak');

module.exports = settings => {
  const phases = settings.phases;
  const options = settings.options;
  const phase = options.env;
  const changeId = phases[phase].changeId;
  const oc = new OpenShiftClientX(Object.assign({namespace: phases[phase].namespace}, options));

  //add Valid Redirect URIs for the pull request to keycloak
  /************
  if(phase === 'dev') {
    const kc = new KeyCloakClient(settings, oc);
    kc.addUris();
  }
  *************/

  const templatesLocalBaseUrl = oc.toFileUrl(path.resolve(__dirname, "../../openshift"));
  var objects = [];

  // The deployment of your cool app goes here ▼▼▼

  //create network security policies for internal pod to pod communications
  /*
  if(phase === 'dev') {

    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/knp/knp-env-pr.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix,
        'ENVIRONMENT': phases[phase].phase
      }
    }))

    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/patroni-2.1.1/templates/prerequisite.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix
      }
    }))

    objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/patroni-2.1.1/templates/deploy.yaml`, {
      'param': {
        'SUFFIX': phases[phase].suffix,
        'CPU_REQUEST': phases[phase].patroniCpuRequest,
        'CPU_LIMIT': phases[phase].patroniCpuLimit,
        'MEMORY_REQUEST': phases[phase].patroniMemoryRequest,
        'MEMORY_LIMIT': phases[phase].patroniMemoryLimit,
        'REPLICAS': phases[phase].patroniReplica,
        'PVC_SIZE': phases[phase].patroniPvcSize,
        'STORAGE_CLASS': phases[phase].storageClass
      }
    }))
  }
  */

  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/frontend/frontend-dc-docker.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'ENV_NAME': phases[phase].phase,
      'HOST_NAME': phases[phase].host,
      'CPU_REQUEST': phases[phase].frontendCpuRequest,
      'CPU_LIMIT': phases[phase].frontendCpuLimit,
      'MEMORY_REQUEST': phases[phase].frontendMemoryRequest,
      'MEMORY_LIMIT': phases[phase].frontendMemoryLimit,
      'REPLICAS':  phases[phase].frontendReplicas,
      'REACT_APP_BCSC_KEYCLOAK_CLIENT_ID': phases[phase].reactAppBCSCKeycloakClientId,
      'REACT_APP_BCSC_KEYCLOAK_REALM': phases[phase].reactAppBCSCKeycloakRealm,
      'REACT_APP_BCSC_KEYCLOAK_URL': phases[phase].reactAppBCSCKeycloakUrl,
      'REACT_APP_BCEID_KEYCLOAK_CLIENT_ID': phases[phase].reactAppBCeIDKeycloakClientId,
      'REACT_APP_BCEID_KEYCLOAK_REALM': phases[phase].reactAppBCeIDKeycloakRealm,
      'REACT_APP_BCEID_KEYCLOAK_URL': phases[phase].reactAppBCeIDKeycloakUrl,
      'REACT_APP_API_BASE': phases[phase].reactAppApiBase
    }
  }))
  
  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/backend/backend-dc.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'ENV_NAME': phases[phase].phase,
      'BACKEND_HOST_NAME': phases[phase].backendHost,
      'CPU_REQUEST': phases[phase].backendCpuRequest,
      'CPU_LIMIT': phases[phase].backendCpuLimit,
      'MEMORY_REQUEST': phases[phase].backendMemoryRequest,
      'MEMORY_LIMIT': phases[phase].backendMemoryLimit,
      'HEALTH_CHECK_DELAY': phases[phase].backendHealthCheckDelay,
      'REPLICAS':  phases[phase].backendReplicas,
      'DJANGO_DEBUG': phases[phase].backendDjangoDebug,
      'CRA_ENVIRONMENT':  phases[phase].craEnvironment,       
      'BUCKET_NAME': phases[phase].bucketName,
      'CORS_ORIGIN_WHITELIST': phases[phase].corsOriginWhitelist
    }
  })) 

  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/task-queue/task-queue-dc.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'CPU_REQUEST': phases[phase].taskQueueCpuRequest,
      'CPU_LIMIT': phases[phase].taskQueueCpuLimit,
      'MEMORY_REQUEST': phases[phase].taskQueueMemoryRequest,
      'MEMORY_LIMIT': phases[phase].taskQueueMemoryLimit,
      'REPLICAS':  phases[phase].taskQueueReplicas,
      'CRA_ENVIRONMENT':  phases[phase].craEnvironment, 
      'DJANGO_DEBUG': phases[phase].taskQueueDjangoDebug,
      'CORS_ORIGIN_WHITELIST': phases[phase].corsOriginWhitelist
    }
  })) 

  oc.applyRecommendedLabels(
      objects,
      phases[phase].name,
      phase,
      `${changeId}`,
      phases[phase].instance,
  );
  oc.importImageStreams(objects, phases[phase].tag, phases.build.namespace, phases.build.tag);
  oc.applyAndDeploy(objects, phases[phase].instance);

};
