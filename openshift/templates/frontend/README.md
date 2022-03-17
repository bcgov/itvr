### Files included

    * frontend-bc.yaml frontend build config
    * frontend-dc.yaml frontend deployment config
    * frontend-autoscaler.yaml create backend frontend, it is not in pipeline and needs to run independently

### Before triggering pipeline

1. import nodejs base image from RedHat
oc import-image ubi8/nodejs-16:1-18 --from=registry.access.redhat.com/ubi8/nodejs-16:1-18 --confirm

### After pipeline completes

1. Create autoscaler for frontend
