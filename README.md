Use these files to compile a Docker image for running TabPy Server in a container. If your use case does not require any chages to these files, you can pull the already compiled image from docker hub.
The compiled image can be pulled and run directly from https://hub.docker.com/repository/docker/gghidiu/tabpy using the following command:
```
docker image pull gghidiu/tabpy:interworks
```
Run the container using:
```
docker container run --publish 9004:9004 gghidiu/tabpy:interworks
```
