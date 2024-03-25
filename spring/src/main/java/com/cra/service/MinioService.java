package com.cra.service;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Value;

import java.io.InputStream;

import io.minio.MinioClient;
import io.minio.GetObjectArgs;

@Service
public class MinioService {
    @Value("${MINIO_ENDPOINT}")
    private String url;

    @Value("${MINIO_ROOT_USER}")
    private String accessKeyId;

    @Value("${MINIO_ROOT_PASSWORD}")
    private String secretAccessKey;

    @Value("${MINIO_BUCKET_NAME}")
    private String bucketName;

    private MinioClient getClient() {
        return MinioClient.builder()
                .endpoint(url)
                .credentials(accessKeyId, secretAccessKey)
                .build();
    }

    public InputStream getObject(String objectName) throws Exception {
        MinioClient client = getClient();
        return client.getObject(
                GetObjectArgs.builder()
                        .bucket(bucketName)
                        .object(objectName)
                        .build());
    }

}
