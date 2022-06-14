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

  //before deploy k6 backend, copy backend-dc.yaml to backend-k6-dc.yaml and add BYPASS_AUTHENTICATION and gove value True
  //sample image files are available at https://www.learningcontainer.com/sample-jpeg-file-download-for-testing/
  objects = objects.concat(oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/templates/backend/backend-k6-dc.yaml`, {
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
      'BUCKET_NAME': phases[phase].bucketName
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
