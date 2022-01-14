# Yolov4-kubernetes
Scaling yolov4 object detection using kubernetes

## Getting started

- Build the Docker image

  `docker build -t image_name:version .`

- Publish the docker image to dockerhub

  `docker push image_name:version`

- Modify `deployments/yolo.yaml` with the apropriate container image

- On a kubernetes cluster apply the yolov4-fastapi deployment along with the expose-service to expose the node-port
 
  `kubectl apply -f deployments/yolo.yaml -f deployments/expose-service.yaml`
  
 ## Testing
 
 - Check the service and deployment status using kubectl commands
 
    `kubectl get pods` and `kubectl get services`
  
 - Try acessing the endpoint using any one of the ips of the nodes on port `31117` as mentioned in the `expose-service.yaml` file
 
 - You can curl the api to get the response
 
   ```
   curl -X 'POST' \
    'http://ip-of-the-node/files/' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@/path/to/img.jpg;type=image/jpeg'
   ```
 
 - A sample response would look something like this
 
    `{"result":"{'person': 0.8518975, 'frisbee': 0.23659469, 'tennis racket': 0.24101968}"}`
