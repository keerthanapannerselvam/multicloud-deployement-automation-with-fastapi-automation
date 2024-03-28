from fastapi import FastAPI, HTTPException, Form, Body
from pydantic import BaseModel, AnyUrl
from kubernetes import client, config
import boto3
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
kubeconfig_path = "config.yaml"

class KubernetesCluster(BaseModel):
    cluster_name: str
    cluster_region: str
    kubeconfig: str

class ContainerDetails(BaseModel):
    container_image: str
    port: int

class AWSCredentials(BaseModel):
    access_key_id: str
    secret_access_key: str
    region: str

class ECSClusterDetails(BaseModel):
    cluster_name: str
    cluster_region: str

class ECSDeployRequest(BaseModel):
    aws_credentials: AWSCredentials
    ecs_cluster_details: ECSClusterDetails
    container_image_url: AnyUrl
    port_requirements: int

config.load_kube_config()

def create_kubernetes_deployment(namespace, deployment_name, image, port):
    try:
        # Load Kubernetes configuration
        config.load_kube_config(config_file=kubeconfig_path)

        # Create Kubernetes API client
        api_instance = client.CoreV1Api()

        # Define Pod manifest
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": deployment_name},
            "spec": {
                "containers": [{
                    "name": "my-container",
                    "image": image,
                    "ports": [{"containerPort": port}]
                }]
            }
        }

        # Create Pod in the specified Kubernetes cluster
        api_instance.create_namespaced_pod(namespace=namespace, body=pod_manifest)

        logging.info(f"Deployment to Kubernetes cluster: {deployment_name}")
        return {"status": "success", "message": "Deployment to Kubernetes successful"}

    except Exception as e:
        logging.error(f"Kubernetes deployment failed. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deployment failed. Error: {str(e)}")

def deploy_to_ecs(ecs_client, cluster_name, container_image_url, port_requirements):
    try:
        # Your ECS deployment logic goes here...

        # Example: Print the cluster name
        logging.info(f"Deploying to ECS cluster: {cluster_name}")

        # Return a response indicating the success or failure of the deployment
        return {"status": "success", "message": "Deployment to ECS successful"}

    except Exception as e:
        # Log the error
        logging.error(f"ECS deployment failed. Error: {str(e)}")
        # Return a response indicating the failure
        raise HTTPException(status_code=500, detail=f"Deployment failed. Error: {str(e)}")

@app.get("/")
def read_root():
    return {"Welcome"}

@app.post("/k8s-deploy")
async def deploy_to_kubernetes(cluster: KubernetesCluster = Body(...), container_details: ContainerDetails = Body(...)):
    return create_kubernetes_deployment(
        namespace="default",
        deployment_name="my-deployment",
        image=container_details.container_image,
        port=container_details.port
    )

@app.post("/ecs-deploy")
async def deploy_to_ecs_endpoint(
    aws_access_key_id: str = Form(...),
    aws_secret_access_key: str = Form(...),
    aws_region: str = Form(...),
    ecs_cluster_name: str = Form(...),
    ecs_cluster_region: str = Form(...),
    container_image_url: AnyUrl = Form(...),
    port_requirements: int = Form(...)
):
    aws_credentials = AWSCredentials(
        access_key_id=aws_access_key_id,
        secret_access_key=aws_secret_access_key,
        region=aws_region
    )
    ecs_cluster_details = ECSClusterDetails(
        cluster_name=ecs_cluster_name,
        cluster_region=ecs_cluster_region
    )
    ecs_request = ECSDeployRequest(
        aws_credentials=aws_credentials,
        ecs_cluster_details=ecs_cluster_details,
        container_image_url=container_image_url,
        port_requirements=port_requirements
    )
    return deploy_to_ecs(
        ecs_client=boto3.client(
            "ecs",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        ),
        cluster_name=ecs_cluster_name,
        container_image_url=container_image_url,
        port_requirements=port_requirements
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
