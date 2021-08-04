# CIS Integration

[IBM Cloud Internet Services (CIS)](https://cloud.ibm.com/catalog/services/internet-services) is a white labeled [Cloudflare](https://en.wikipedia.org/wiki/Cloudflare) offering on IBM Cloud. It provides a number of functionalities such as [Web Application Firewall (WAF)](https://cloud.ibm.com/docs/cis?topic=cis-waf-q-and-a), [Global Load Balancing (GLB)](https://cloud.ibm.com/docs/cis?topic=cis-global-load-balancer-glb-concepts), [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security), etc. It's a a popular solution for enterprise customers because it's a one stop shop for many functions and can replace several devices in certain cloud architectures. However, integrating CIS with apps deployed on the cloud is not a one click process and requires relatively complex manual setup.

## Overview
The goal of this project is to automate CIS integration for IBM Cloud application platforms. We will produce a command line tool that customers can use to simplify this process.

This command line tool currently supports [Code Engine](https://www.ibm.com/cloud/code-engine) applications and [IBM Cloud Kubernetes Service](https://www.ibm.com/cloud/kubernetes-service) clusters, and has been configured for MacOS. 

In order to connect a Code Engine app to a CIS instance, numerous resources must be set up within CIS, namely: DNS records, a TLS certificate, a Global Load Balancer, Origin Pool, and Health Check Monitor, and an Edge Function.

To connect a Kubernetes cluster to a CIS instance, DNS records must be created in the CIS instance, a TLS Edge Certificate must be created in CIS, a TLS certificate can be ordered by the Kubernetes Certificate Manager and imported to your IKS cluster as a secret (optional), and ACL rules must be configured and an Ingress must be created in your IKS cluster.

Before using this application, make sure you have an existing Code Engine app and a CIS instance with a domain name:
* [Deploy a CIS instance](https://cloud.ibm.com/docs/cis?topic=cis-getting-started)
* [Deploy a Code Engine application](https://cloud.ibm.com/docs/codeengine?topic=codeengine-deploy-app-tutorial) 

## Installation

### Docker (Recommended)
The only prerequisite needed for this installation is Docker. Please see https://docs.docker.com/get-docker/ to download and install Docker. 

Clone or download the repository and change into the project directory.
```
$ git clone https://github.com/IBM/cis-integration.git
```
Now within the cloned project we need to build and run our Docker image. To do this run the following commands. 
```
$ docker build -t cis-int . 
```
```
$ docker run -it --name cis-cli-app --rm cis-int
```

The `--rm cis-int` above is optional if you wish to keep the container running.

### Non-Docker
The main prerequisite for this installation is Python. We suggest that you use Python3.8 or newer see https://www.python.org/downloads/. 

Clone or download the repository and navigate into the project directory.
```
$ git clone https://github.com/IBM/cis-integration.git
```
Once in the project directoy run the install script. If a permission error is encountered `sudo` might need to be used. 
```
$ ./install.sh
```

#### Uninstall Option `--uninstall` and `-u`
If you decided to install directly onto your machine and wish to uninstall the gathered dependencies and resources you can specify the `--uninstall` or `-u` argument. This will remove everything that was installed onto your computer and will ask you to confirm before it continues. Below are examples on how you would use this command:
```
cis-integration --uninstall
```
or
```
ci -u
```

## Code Engine Usage
For general information on how to use the tool, run the following command in the terminal on your computer: 
```
$ cis-integration code-engine --help
```

This tool offers two options to connect the CIS instance to the application. You may choose to build the resources needed for your CIS instance using either Python or [Terraform](https://www.terraform.io/) scripts. If you choose to use Terraform, this tool will build an [IBM Schematics](https://cloud.ibm.com/docs/schematics?topic=schematics-about-schematics) workspace to run the Terraform code. 

Regardless of the option you choose, the tool will require you to input some information about your CIS instance and Code Engine application. You can find this information by going to https://cloud.ibm.com and logging into your IBM Cloud account. Navigate to the "Resource list" tab and locate your CIS instance and Code Engine app.

### To deploy resources using Python scripts:
**WARNING:** If you have any resources already present on your CIS instance that will conflict with the resources that will be created by this tool (i.e. a DNS Record with 'www' as its name), this method will automatically update them to represent the configuration specified by this tool. If you are concerned about overwriting any resources you've created yourself, use the [Terraform implementation](#to-deploy-resources-using-terraform-scripts) listed below.

1. Install the tool using the [installation](#installation) instructions listed above
2. Access the command terminal on your computer 
3. If you're using Docker, build and run your Docker image with the above commands
4. Input the following generic command:
```
$ cis-integration code-engine -n [CIS NAME] -r [RESOURCE GROUP] -d [CIS DOMAIN] -a [CODE ENGINE APP DOMAIN]
```
An alternative command is also available:
```
$ cis-integration code-engine -c [CIS CRN] -z [CIS ZONE ID] -d [CIS DOMAIN] -a [CODE ENGINE APP DOMAIN]
```
### Arguments:
* **CIS NAME:** the name of your CIS instance.
* **RESOURCE GROUP:** the resource group connected to the CIS instance. Found by navigating to your CIS resource page and clicking on "Details".
* **CIS CRN:** the cloud resource name (CRN) of your CIS instance. Found in the "Overview" tab of your CIS resource page. 
    Example: `crn:v1:test:public:internet-svcs:global:a/2c38d9a9913332006a27665dab3d26e8:836f33a5-d3e1-4bc6-876a-982a8668b1bb::`
* **CIS ID:** the ID associated with your CIS instance. Found in the "Overview" tab of your CIS resource page under "Domain ID". 
    Example: `ae3445ji01b31lvi934jlaef09fad1lc`
* **CIS DOMAIN:** the domain name connected to your CIS instance. Found near the top of your CIS resource page. 
    Example: `example.com`
* **CODE ENGINE APP DOMAIN:** the hostname of your Code Engine application. Found by navigating to your Code Engine application page and clicking on "Open application URL". 
    Example: `example-app.8jl3icnad39.us-south.codeengine.appdomain.cloud`

### To deploy resources using Terraform scripts:
**Note:** This version will not execute any portion of the Terraform scripts if it detects any conflicting resources already present on your CIS instance. Please review the [CIS Manual Steps](https://github.com/IBM/cis-integration/blob/master/cis_manual_steps.md) document to see what resources are created by this tool.

1. Install the tool using the [installation](#installation) instructions listed above
2. Access the command terminal on your computer
3. If you're using Docker, build and run your Docker image with the above commands
4. Input the following generic command:
```
$ cis-integration code-engine --terraform -r [RESOURCE GROUP] -n [CIS NAME] -d [CIS DOMAIN] -a [CODE ENGINE APP DOMAIN]
```
If you would like to view a detailed log from the Schematics workspace showing the resources being created during the execution of the Terraform `apply` function, add `--verbose` to the above command.
### Arguments:
* **RESOURCE GROUP:** the resource group connected to the CIS instance. Found by navigating to your CIS resource page and clicking on "Details".
* **CIS NAME:** the name of your CIS instance.
* **CIS DOMAIN:** the domain name connected to your CIS instance. Found near the top of your CIS resource page. 
    Example: `example.com`
* **CODE ENGINE APP DOMAIN:** the hostname of your Code Engine application. Found by navigating to your Code Engine application page and clicking on "Open application URL". 
    Example: `example-app.8jl3icnad39.us-south.codeengine.appdomain.cloud`

**Note:** For the origin pool, origin name, and health check resources, this tool builds them using generic names. If you would like to change these later, navigate to the "Reliability" tab of your CIS instance and click on the "Global load balancers" tab. You can find your origin pools and health checks here and edit them manually.

### Code Engine `--env` global option
The `--env` global option allows for parameters to be passed through a file named `credentials.env` instead of through command line arguments. The format of this file is important, please see below on how to format this file with the needed information. `credentials.env` must be present in the current working directory.
```
CRN="<CIS_CRN>"
ZONE_ID="<CIS_ID>"
API_ENDPOINT="https://api.cis.cloud.ibm.com"
CIS_SERVICES_APIKEY="<YOUR_CIS_SERVICES_APIKEY>"
CIS_NAME="<CIS_INSTANCE_NAME>"
RESOURCE_GROUP="<YOUR_IBM_CLOUD_RESOURCE_GROUP>"
APP_DOMAIN="<CODE_ENGINE_APP_DOMAIN>"
CIS_DOMAIN="<DOMAIN_NAME>"
```
Example usage
```
cis-integration code-engine --env
```

### Deleting created resources with the `--delete` option
If you decide to delete the resources you've created using this tool, the `--delete` global option is available to you. The global load balancer, origin pool, health check, DNS records, TLS certificate(s), edge function, and (by adding --terraform to the command) the Schematics workspace(s) created by this tool may be deleted. Use the following generic examples to format the command:
```
cis-integration code-engine --delete -n [CIS NAME] -r [RESOURCE GROUP] -d [CIS DOMAIN]
```
or
```
cis-integration code-engine --delete -c [CIS CRN] -z [CIS ZONE ID] -d [CIS DOMAIN]
```
**Note:** If you do not use the `--terraform` option, you will prompted at each stage to confirm the deletion of the selected resource(s). Input 'y' or 'yes' to confirm (NOT case sensitive). 

If you created your resources using the `--terraform` global option, then a Schematics workspace was created on your IBM Cloud account to execute the terraform scripts that built your resources. By adding the `--terraform` option to the `--delete` command, the resources will be deleted using the workspace's internal `destroy` action. The workspace will then be deleted along with the rest of the resources.

## IKS Usage
For general information on how to use the tool, run the following command in the terminal on your computer: 
```
$ cis-integration iks --help
```

This tool offers two options to connect the CIS instance to the cluster. You may choose to build the resources needed for your CIS instance using either Python or [Terraform](https://www.terraform.io/) scripts. If you choose to use Terraform, this tool will build an [IBM Schematics](https://cloud.ibm.com/docs/schematics?topic=schematics-about-schematics) workspace to run the Terraform code. 

Regardless of the option you choose, the tool will require you to input some information about your CIS instance and IKS cluster. You can find this information by going to https://cloud.ibm.com and logging into your IBM Cloud account. Navigate to the "Resource list" tab and locate your CIS instance and IKS cluster.

### To deploy resources using Python scripts:
1. Install the tool using the [installation](#installation) instructions listed above
2. Access the command terminal on your computer 
3. If you're using Docker, build and run your Docker image with the above commands
4. Input the following generic command:
```
cis-integration iks -n [CIS NAME] -r [RESOURCE GROUP] -d [CIS DOMAIN] -i [IKS CLUSTER ID] --namespace [IKS NAMESPACE] --service_name [IKS SERVICE NAME] --service_port [IKS TARGET PORT]
```
### Arguments:
* **RESOURCE GROUP:** the resource group connected to the CIS instance. Found by navigating to your CIS resource page and clicking on "Details".
* **CIS NAME:** the name of your CIS instance.
* **CIS DOMAIN:** the domain name connected to your CIS instance. Found near the top of your CIS resource page. 
    Example: `example.com`
* **IKS CLUSTER ID:** the ID associated with your IKS cluster. Found in the "Details" section in the "Overview" tab of your IKS cluster.
    Example: `g3jk284d008l7s14gcsg` 
* **IKS NAMESPACE:** the name of the virtual cluster using your physical IKS cluster resources. Found by opening your kubernetes dashboard and clicking the "Namespaces" tab in the "Cluster" section.
* **IKS SERVICE NAME:** the name of the Service exposing your application by rerouting incoming traffic to pods. Found by opening your kubernetes dashboard and clicking on the "Services" tab in the "Service" section.
* **IKS TARGET PORT:** the target port of your Service that every incoming port is mapped to. Found be opening your kubernetes dashboard, clicking the "Services" tab in the "Service" section, and clicking the "edit" button in the top-right corner.

### To deploy resources using Terraform scripts:
1. Install the tool using the [installation](#installation) instructions listed above
2. Access the command terminal on your computer 
3. If you're using Docker, build and run your Docker image with the above commands
4. Input the following generic command:
```
cis-integration iks --terraform -n [CIS NAME] -r [RESOURCE GROUP] -d [CIS DOMAIN] -i [IKS CLUSTER ID] --namespace [IKS NAMESPACE] --service_name [IKS SERVICE NAME] --service_port [IKS TARGET PORT]
```
### Arguments:
* **RESOURCE GROUP:** the resource group connected to the CIS instance. Found by navigating to your CIS resource page and clicking on "Details".
* **CIS NAME:** the name of your CIS instance.
* **CIS DOMAIN:** the domain name connected to your CIS instance. Found near the top of your CIS resource page. 
    Example: `example.com`
* **IKS CLUSTER ID:** the ID associated with your IKS cluster. Found in the "Details" section in the "Overview" tab of your IKS cluster.
    Example: `g3jk284d008l7s14gcsg` 
* **IKS NAMESPACE:** the name of the virtual cluster using your physical IKS cluster resources. Found by opening your kubernetes dashboard and clicking the "Namespaces" tab in the "Cluster" section.
* **IKS SERVICE NAME:** the name of the Service exposing your application by rerouting incoming traffic to pods. Found by opening your kubernetes dashboard and clicking on the "Services" tab in the "Service" section.
* **IKS TARGET PORT:** the target port of your Service that every incoming port is mapped to. Found be opening your kubernetes dashboard, clicking the "Services" tab in the "Service" section, and clicking the "edit" button in the top-right corner.

## Resources
- [Deploy CIS instance](https://cloud.ibm.com/docs/cis?topic=cis-getting-started)
- [Deploy Code Engine application](https://cloud.ibm.com/docs/codeengine?topic=codeengine-deploy-app-tutorial)
- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Terraform](https://www.terraform.io/)
