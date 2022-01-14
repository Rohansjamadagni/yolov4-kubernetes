# Yolov4-kubernetes
Scaling yolov4 object detection using kubernetes

## Getting started

- Download the pretrained `yolov4.weights` from the official [repository](https://github.com/AlexeyAB/darknet)

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
    'http://ip-of-the-node:31117/files/' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@/path/to/img.jpg;type=image/jpeg'
   ```
 
 - A sample response would look something like this
 
    `{"result":"{'person': 0.8518975, 'frisbee': 0.23659469, 'tennis racket': 0.24101968}"}`

## Adding a nginx load balancer

- On a different machine install nginx

    `sudo apt install nginx`

- Modify `loadbalancer/loadbalancer.conf` with the appropriate node ip addresses

- Copy `loadbalancer/loadbalancer.conf` to `/etc/nginx/conf.d/loadbalancer.conf`

- Restart nginx service 

    `sudo systemctl restart nginx`
    
- Curl the api using the command mentioned earlier by using the ip of the load balancer 
