# CIS Integration

[IBM Cloud Internet Services (CIS)](https://cloud.ibm.com/catalog/services/internet-services) is a white labeled [Cloudflare](https://en.wikipedia.org/wiki/Cloudflare) offering on IBM Cloud. It provides a number of functionalities such as [Web Application Firewall (WAF)](https://cloud.ibm.com/docs/cis?topic=cis-waf-q-and-a), [Global Load Balancing (GLB)](https://cloud.ibm.com/docs/cis?topic=cis-global-load-balancer-glb-concepts), [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security), etc. It's a a popular solution for enterprise customers because it's a one stop shop for many functions and can replace several devices in certain cloud architectures. However, integrating CIS with apps deployed on the cloud is not a one click process and requires relatively complex manual setup.

## Overview
The goal of this project is to automate CIS integration for IBM Cloud application platforms. We will produce a command line tool that customers can use to simplify this process.

This command line tool currently supports [Code Engine](https://www.ibm.com/cloud/code-engine) applications and has been configured for MacOS. In order to connect a Code Engine app to a CIS instance, numerous resources must be set up within CIS, namely: DNS records, a TLS certificate, a Global Load Balancer, Origin Pool, and Health Check Monitor, and an Edge Function.

Before using this application:
* [Deploy a CIS instance](https://cloud.ibm.com/docs/cis?topic=cis-getting-started).
* Deploy a [Code Engine](https://ibm-cloudplatform.slack.com/archives/C01MHQ3MUF4/p1613432390005800) application

## Installation

### Docker (Recommended)
The only prerequisite needed for this installation is Docker. Please see https://docs.docker.com/get-docker/ to download and install Docker. 

Clone or download the repository and change into the project directory.
```
$ git clone https://github.ibm.com/GCAT/cis-integration.git
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
$ git clone https://github.ibm.com/GCAT/cis-integration.git
```
Once in the project directoy run the install script. If a permission error is encountered `sudo` might need to be used. 
```
$ ./install.sh
```

## Usage
For general information on how to use the tool, run the following command in the terminal on your computer: 
```
$ cis-integration code-engine --help
```

This tool offers two options to connect the CIS instance to the application. You may choose to build the resources needed for your CIS instance using either Python or [Terraform](https://www.terraform.io/) scripts. If you choose to use Terraform, this tool will build an [IBM Schematics](https://cloud.ibm.com/docs/schematics?topic=schematics-about-schematics) workspace to run the Terraform code. Note that Terraform is currently unable to ensure that the TLS mode for TLS certificates is in End-to-end CA Signed or check for duplicate certificates.

Regardless of the option you choose, the tool will require you to input some information about your CIS instance and Code Engine application. You can find this information by going to https://cloud.ibm.com and logging into your IBM Cloud account. Navigate to the "Resource list" tab and locate your CIS instance and Code Engine app

### To deploy resources using Python scripts:
1. Install the tool using the [installation](#installation) instructions listed above
2. Access the command terminal on your computer 
3. If you're using Docker, build and run your Docker image with the above commands
4. Input the following generic command:
```
$ cis-integration code-engine -c [CIS CRN] -z [CIS ID] -d [CIS DOMAIN] -a [CODE ENGINE APP URL]
```
### Arguments:
* **CIS CRN:** the cloud resource name (CRN) of your CIS instance. Found in the "Overview" tab of your CIS resource page. 
    Example: `crn:v1:test:public:internet-svcs:global:a/2c38d9a9913332006a27665dab3d26e8:836f33a5-d3e1-4bc6-876a-982a8668b1bb::`
* **CIS ID:** the ID associated with your CIS instance. Found in the "Overview" tab of your CIS resource page under "Domain ID". 
    Example: `ae3445ji01b31lvi934jlaef09fad1lc`
* **CIS DOMAIN:** the domain name connected to your CIS instance. Found near the top of your CIS resource page. 
    Example: `example.com`
* **CODE ENGINE APP URL:** the URL of your Code Engine application. Found by navigating to your Code Engine application page and clicking on "Open application URL". 
    Example: `example-app.8jl3icnad39.us-south.codeengine.appdomain.cloud`

### To deploy resources using Terraform scripts:
1. Install the tool using the [installation](#installation) instructions listed above
2. Access the command terminal on your computer
3. If you're using Docker, build and run your Docker image with the above commands
4. Input the following generic command:
```
$ cis-integration code-engine --terraform -r [RESOURCE GROUP] -n [CIS NAME] -d [CIS DOMAIN] -a [CODE ENGINE APP URL]
```
### Arguments:
* **RESOURCE GROUP:** the resource group connected to the CIS instance. Found by navigating to your CIS resource page and clicking on "Details".
* **CIS NAME:** the name of your CIS instance.
* **CIS DOMAIN:** the domain name connected to your CIS instance. Found near the top of your CIS resource page. 
    Example: `example.com`
* **CODE ENGINE APP URL:** the URL of your Code Engine application. Found by navigating to your Code Engine application page and clicking on "Open application URL". 
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
APP_URL="<CODE_ENGINE_APP_URL>"
```
Example usage
```
cis-integration code-engine --env
```
## Resources
- [Deploy CIS instance](https://cloud.ibm.com/docs/cis?topic=cis-getting-started).
- [Deploy Code Engine application](https://ibm-cloudplatform.slack.com/archives/C01MHQ3MUF4/p1613432390005800)
- [Python](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Terraform](https://www.terraform.io/)