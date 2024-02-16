# Multi-Cloud Deployment Automation with FastAPI

## Overview

This FastAPI project enables users to deploy containerized applications to both Kubernetes and AWS ECS clusters. The application provides two endpoints, `/k8s-deploy` for Kubernetes deployment and `/ecs-deploy` for AWS ECS deployment.

## Table of Contents

1. [Cluster Deployment](#cluster-deployment)
   - [Run Minikube or EKS on AWS](#run-minikube-or-eks-on-aws)
   - [Create an AWS ECS Cluster](#create-an-aws-ecs-cluster)
2. [FastAPI Application](#fastapi-application)
   - [Endpoints](#endpoints)
3. [Documentation](#documentation)
   - [How to Use](#how-to-use)
   - [Setup and Run Locally](#setup-and-run-locally)

## 1. Cluster Deployment

### 1.1 Run Minikube or EKS on AWS

Follow these steps to set up Minikube locally or create an EKS cluster on AWS:

- **Minikube:**
  - Install Minikube using the official documentation.
  - Start Minikube using `minikube start`.

- **EKS on AWS:**
  - Use the AWS Management Console or AWS CLI to create an EKS cluster.
  - Follow the instructions in the assignment for using CloudFormation or Terraform.

### 1.2 Create an AWS ECS Cluster

Follow the instructions provided in the assignment to create an AWS ECS Cluster using CloudFormation or Terraform.

## 2. FastAPI Application

### 2.1 Endpoints

- **/k8s-deploy:** Deploy to a Kubernetes cluster.
- **/ecs-deploy:** Deploy to an AWS ECS cluster.

## 3. Documentation

### 3.1 How to Use

#### 3.1.1 /k8s-deploy Endpoint

1. **Send a POST request:**
   - Send a POST request to `/k8s-deploy` with the following JSON parameters:
     - `cluster_name`: Name of the Kubernetes cluster.
     - `cluster_region`: Region of the Kubernetes cluster.
     - `kubeconfig`: Contents of the Kubernetes configuration file.
     - `container_image`: URL of the container image.
     - `port`: Port requirements for the container.

   Example using `curl`:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
     "cluster_name": "your_cluster_name",
     "cluster_region": "your_cluster_region",
     "kubeconfig": "your_kubeconfig_contents",
     "container_image": "your_container_image_url",
     "port": 8080
   }' http://localhost:8000/k8s-deploy
