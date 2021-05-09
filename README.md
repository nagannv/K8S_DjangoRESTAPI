# K8S_DjangoRESTAPI
Django REST framework API to deploy container based applications in the form of Kubernetes Operator on the Kubernetes clusters. 

Objective:
Deploy software Container based application on Kubernetes in the form of Operator by invoke REST API using REST client using CLI.

Components
1.	Django REST API framework as the Backend
https://www.django-rest-framework.org/

2.	REST API CLI client using Python Click package as User interface.
https://click.palletsprojects.com/en/7.x/

3.	Python Kubernetes Client Plugin to bride between the Kubernetes API server and Django REST framework 
https://github.com/kubernetes-client/python

4.	Helm charts for Kubernetes application packaging
https://helm.sh/docs/topics/charts/

5.	Operator-SDK framework to create the Kubernetes Operator. 
https://sdk.operatorframework.io/

Pre-requisites
Package container-based applications using the helm charts and convert the helm charts into Kubernetes Operator for better application management use Operator SDK-framework and refactor the generated output.

Sample REST API calls and Responses

1.	Register an existing Kubernetes cluster to the Backend server.

main.py add-cluster --kubeconfig="/root/.kube/config"

POST /example/add-cluster

__Req Body__

{
    "cluster_config": ""
}

__Response__

{
    "is_successful": true,
    "cluster_id": "6046ac86-ce0d-4614-8e10-b63edf8e0553",
    "error": null
}

2.	Setting the Image 
main.py create-yaml --image-tag="latest" --image-name=" mongodb-exporter"

POST /example/create-yaml

__Req Body__

{
    "image_tag":" latest",
    "image_repository":"xebialabs/ mongodb-exporter "
}

__Response__

{
    "is_successful": true,
    "error": "",
    "uuid_for_yaml": "6f4a6ee4-da93-4025-a9d7-37c3ef2becde"
}

3.	Deploy application on Kubernetes cluster by supplying the Cluster ID and UUID of the Image Yaml

main.py deploy-resources --cluster-id="6046ac86-ce0d-4614-8e10-b63edf8e0553" --uuid-for-yaml="6f4a6ee4-da93-4025-a9d7-37c3ef2becde"

POST /example/deploy-resources.

__Req Body__

{
    "cluster_id": "6046ac86-ce0d-4614-8e10-b63edf8e0553"
"uuid_for_yaml": "6f4a6ee4-da93-4025-a9d7-37c3ef2becde",
}

__Response__

{
    "is_successful": true,
    "error": ""
}

4.	Deregister the K8S cluster from Backend Framework.

main.py delete-resources --cluster-id="6046ac86-ce0d-4614-8e10-b63edf8e0553"

DELETE /example/delete-resources.

__Req Body__

{
    "cluster_id": "6046ac86-ce0d-4614-8e10-b63edf8e0553"
"uuid_for_yaml": "6f4a6ee4-da93-4025-a9d7-37c3ef2becde",
}

__Response__

{
    "is_successful": true,
    "error": ""
}
