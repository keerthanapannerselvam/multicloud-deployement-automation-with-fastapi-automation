from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, AnyUrl
from kubernetes import config
from kubernetes.client import V1Container, V1ContainerPort, V1PodSpec, V1LabelSelector, V1PodTemplateSpec, V1ObjectMeta, AppsV1Api, AppsV1DeploymentSpec, AppsV1Deployment

app = FastAPI()

class AWSCredentials(BaseModel):
    access_key_id: str
    secret_access_key: str
    region: str

class K8sDeployRequest(BaseModel):
    cluster_credentials: AWSCredentials
    cluster_details: dict
    container_image_url: AnyUrl
    port_requirements: int

config.load_kube_config()

def create_deployment(namespace, deployment_name, image, port):
    container = V1Container(
        name="multicloudapp",
        image=image,
        ports=[V1ContainerPort(container_port=port)]
    )

    pod_spec = V1PodSpec(containers=[container])

    deployment_spec = AppsV1DeploymentSpec(
        replicas=1,
        selector=V1LabelSelector(match_labels={"app": "multicloudautomation"}),
        template=V1PodTemplateSpec(metadata=V1ObjectMeta(labels={"app": "multicloudautomation"}), spec=pod_spec)
    )

    deployment_metadata = V1ObjectMeta(name=deployment_name)

    deployment = AppsV1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=deployment_metadata,
        spec=deployment_spec
    )

    apps_api = AppsV1Api()
    deployment_response = apps_api.create_namespaced_deployment(namespace, deployment)
    print(f"Deployment created. Status: {deployment_response.status}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Cloud Deployment Automation with FastAPI!"}

@app.post("/k8s-deploy")
async def deploy_to_k8s(k8s_request: K8sDeployRequest):
    try:
        # Validate credentials and other steps (you need to implement this)

        # Create a Deployment
        create_deployment(
            namespace="default",
            deployment_name="automation",  # Replace with a suitable deployment name
            image=k8s_request.container_image_url,
            port=k8s_request.port_requirements
        )

        # Return success response
        return {"message": "Deployment to Kubernetes successful!"}
    except ApiException as e:
        # Return failure response with specific ApiException details
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Return failure response for other exceptions
        raise HTTPException(status_code=500, detail=str(e))
