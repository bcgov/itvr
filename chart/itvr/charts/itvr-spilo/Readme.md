## Before running Helm
* Create Object Storage secret
Testing command: helm template itvr -f ./values-dev.yaml --set accessId=11,accessKey=22 bucketName=33 . > 1.yaml

Testing command: helm template itvr -f ./values-dev.yaml --set accessId=nr-itvr-dev,accessKey=Kh/idaPzesehyZlvL2ESkOC1xqZ76NUvVBhv9HXv,bucketName=itvrdv . > 1.yaml
Testing command: helm template itvr -f ./values-test.yaml --set accessId=,accessKey= bucketName= . > 1.yaml
Testing command: helm template itvr -f ./values-prod.yaml --set accessId=,accessKey= bucketName= . > 1.yaml