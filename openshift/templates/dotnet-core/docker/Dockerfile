FROM image-registry.openshift-image-registry.svc:5000/ac294c-tools/dotnet-60:6.0-5
ENV CRA_KEY=$CRA_KEY
ADD cra /opt/app-root/src/cra
WORKDIR /opt/app-root/src/cra
CMD ./file-transfer.sh