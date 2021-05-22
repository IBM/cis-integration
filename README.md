# CIS Integration

[IBM Cloud Internet Services (CIS)](https://cloud.ibm.com/catalog/services/internet-services) is a white labeled [Cloudflare](https://en.wikipedia.org/wiki/Cloudflare) offering on IBM Cloud. It provides a number of functionalities such as [Web Application Firewall (WAF)](https://cloud.ibm.com/docs/cis?topic=cis-waf-q-and-a), [Global Load Balancing (GLB)](https://cloud.ibm.com/docs/cis?topic=cis-global-load-balancer-glb-concepts), [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security), etc. It's a a popular solution for enterprise customers because it's a one stop shop for many functions and can replace several devices in certain cloud architectures. However, integrating CIS with apps deployed on the cloud is not a one click process and requires relatively complex manual setup.

The goal of this project is to automate CIS integration for IBM Cloud application platforms. We will produce a command line tool that customers can use to simplify this process.

The most relevant platforms are [Code Engine](https://www.ibm.com/cloud/code-engine), [Gen2 IKS](https://www.ibm.com/cloud/kubernetes-service), [ROKS](https://www.openshift.com/products/kubernetes-engine), and [Gen2 VSI](https://ibm.github.io/cloud-enterprise-examples/deploy-vsi/content-overview/) (VSI is not a true platform but rather an infrastructure solution that customers use to deploy their own app platforms.)

There are other platforms and infrastructure solutions such as Cloud Foundry, Classic IKS, Classic VSI, Bare Metal, etc., but they are less popular.

What you will need to learn:

* [How to deploy CIS](https://cloud.ibm.com/docs/cis?topic=cis-getting-started).
* How to deploy an app on one of the platforms, pick one:
..* [Code Engine](https://ibm-cloudplatform.slack.com/archives/C01MHQ3MUF4/p1613432390005800)
..* [Gen2 IKS](https://ibm.github.io/kube101/)
..* [Gen2 VSI](https://cloud.ibm.com/docs/solution-tutorials?topic=solution-tutorials-vpc-app-deploy)
..* [ROKS](https://cloud.ibm.com/docs/openshift)
* [How to connect the CIS instance to the app](https://cloud.ibm.com/docs/cis?topic=solution-tutorials-multi-region-k8s-cis).
