# productionize - deploy ML models directly from Python [WIP]

<p align="center">
<i><code>productionize</code> is an open-source lightweight ML deployment tool.<br>
You can containerize, deploy and ship your model, without ever<br>
having to leave your beloved Python.</i>
</p>

***

## <code>productionize</code> in a nutshell

What does it do? Well, it does exactly what the catchy library name says it does. <code>productionize</code> helps you to productionize your API. As a Data Scientist, most of the projects I worked on face issue when productionizing code. Often, the code is not tested, standardized or environment agnostic enough to just deploy something somewhere. This where containers come in very handy. Containerization helps you to freeze the environment and decouple your model or just your code from the host system. This makes deployment much, much easier. 

However, working with Docker, Kubernetes and all these other fancy tools is not as simple as one might hope. The good news though, some steps can be automated and this is exactly what <code>productionize</code> does. As Data Scientist you can focus on your model and the containerization and deployment is handled by <code>productionize</code>. 

The workflow with <code>productionize</code> is very simple. First, you develop your API in Python. Next, <code>productionize</code> allows you easily setup a local Kubernetes cluster that allows you to test your API. In <code>productionize</code>, this local Kubernetes cluster is called a workbench, because it is Kubernetes, with a little extra stuff to help you work. Next, you deploy your API. You don't have to change your standard API script for that, <code>productionize</code> will handle that for you. Within a matter of seconds, your API is built into a container and deployed to your workbench. Here you can test your API and see if it works. If you are happy with it, you can simply export the container and deploy it to any Kubernetes cluster you like. 

That way, <code>productionize</code> makes it super easy to turn your local API into a production-ready container and the best part: you don't even have to leave Python.

## Installation

<code>productionize</code> is a Python library, which is hosted on PyPi. Currently, the functions are only supported on <b>macOS</b>. On the <b>darwin</b> platform you can therefore download the package using <code>pip</code>.

    pip install productionize

## Usage

Once the library is properly installed from PyPi, you can source it using your standard python import command. The core
of the library are it's three main classes, those can be imported as follows:

    # import lib
    from productionize import workbench, product

The library contains two major classes. The first one is the <code>workbench()</code> class. This class allows you to setup and manage a proper ML workbench on your local machine. The second one is the <code>product()</code> class. This class allows you to deploy your ML APIs to the local workbench and to any Kubernetes cluster.

### The <code>workbench()</code> class

Once the main classes are sourced, you can setup your very own workbench on your local machine. The workbench consists of several tools:

<ul>
    <li>Docker: a container technology, which helps us to build Docker container, which are the quasi-standard in Machine Learning deployment. You can read more about Docker <a href="https://docs.docker.com/">here</a>.</li>
    <li>VirtualBox: a driver that is needed to create a VM on you local machine to host the Kubernetes cluster, which is at the heart of the workbench. You can read more about VirtualBox <a href="https://www.virtualbox.org/">here</a></li>
    <li>Kubectl: a cli which allows you to interact with Kubernetes. You won't have to do that, but <code>productionize</code> is running Kubernetes commands in the background.</li>
    <li>Minikube: a local implemenation of Kubernetes. Minikube runs on a VM, which is administrated by Virtualbox.</li> 
</ul>

Technically, the components are ensembled in a simple fashion. However, the only specialty is, that Minikube is installed on top of VirtualBox.

To setup the workbench, these tools need to be installed. You can do this, by simple running the <code>setup()</code> method of the workbench class. Once initiated you can call the method.

    # initiate class
    cluster = workbench()

    # install and setup components
    cluster.setup()

To fire up the entire workbench, you first need to login to Docker Desktop. This is installed for you, however, you need to have it running. You can easily do this, just search on your computer - if you have a Mac you just use spotlight search - for Docker and start the application.

Next you will have to sign in. If you don't have an account already, you can create one for free at <a href="https://hub.docker.com>">Docker Hub</a>. Which is a lot like GitHub, just for containers.

Once you did this, you are good to go on. You can now start the cluster using the <code>start_cluster()</code> method. This method allows you to set the resource quota for the cluster. Default are two CPUs and 2GB of memory.

    # start the cluster
    cluster.start_cluster(cpus = '2', memory = '2G')

When the cluster is running, you can create a project. This helps to have a clean and well-structured cluster running. You can do this with the <code>open_project()</code> method.

    # open project
    cluster.open_project(name = "my-project")

In case you want to delete the project you can use the <code>delete_project()</code> method. Technically, the projects are namespaces on Kubernetes.

    # delete project
    cluster.delete_project(name = "my-project")

To stop the cluster you can simply use the <code>stop_cluster()</code> method. This one just idles the cluster, but doesn't remove all the components.

    # stop the cluster
    cluster.stop_cluster()

To cleanly uninstall all the components, you can just run the <code>uninstall()</code> method and even specify which components to delete. The default is, that the components that existed on your machine before will be not removed.

    # cleanly uninstall cluster components
    cluster.uninstall(docker = None, kubectl = None, virtualbox = None, minikube = None, report = True)

### The <code>product()</code> class

While the <code>workbench</code> class mainly concerns the infrastructure management, the <code>product</code> class deals with your API. The <code>product</code> class turns your API into a deployable product. Once you have an API programmed, for instance with Flask, the <code>product</code> class will do the rest for you. 

Let's consider the following python script containing a Flask API:

    #!flask/bin/python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/hello')
    def index():
        return "Hello, World!"

    if __name__ == '__main__':
        app.run(port = '8000', host = '0.0.0.0')

You can, of course, create any kind of API you like. You can also add new routes or whatever you need. To deploy an API to Kubernetes, you would typically need to containerize the API. <code>productionize</code> does that for you. The <code>product</code> class contains the <code>prepare_deployment()</code> method. This method produces a Dockerfile from your API script and a requirements file.

    # initiate the class and say which project the product belongs to
    my_api = product(project = "my-project")

    # prepare the deployment
    my_api.prepare_deployment(api_file = "path_to/api.py",  # path to the api file
                              requirements_file = "path_to/requirements.txt", # path to the req file
                              port = "8000", # the port your API is exposed to
                              name = "my-product") # the name you want to give your product

<p align = "center" style="font-size:9px">
Note: I would advise to not do any directory stunts here. The code in this library is flexible, however, it might be a bit tricky.
</p>

Once you run the <code>prepare_deployment()</code> method, <code>productionize</code> will build a Dockerfile in your current working directory.

You can, of course, modify and edit the Dockerfile. However, at your own risk. If you intend to work in an enterprise context it might be necessary to change permissions within the container. This does not have an effect on <code>productionize</code>. Per default, <code>productionize</code> containers run with root.

    FROM python:3.7.7
    RUN mkdir -p /api
    COPY api.py /api/api.py
    COPY requirements.txt /api/requirements.txt
    RUN python -m pip install -r /api/requirements.txt
    EXPOSE 8000
    ENTRYPOINT ["python", "api/api.py"] 

Once you ran the <code>prepare_deployment()</code> method, you can deploy your api to the workbench. Why would you do this? Well, the workbench should serve as your local test environment. Using the deploy() method, you can easily deploy your "product" to the workbench. 

    my_api.deploy()

Per default <code>deploy()</code> does not take any arguments. Those are not necessary as all info is stored in the my_api object after <code>prepare_deployment</code>. However, if you want, you can also deploy your product on your localhost.
Technically speaking, this will just create Docker container that runs on localhost. This can be acheived with the local arg
in the method call.

    my_api.deploy(local = True)

Once your product is deployed, the method will return the url under which you can reach your API. However, don't forget to add your custom routes.

Your output should look somewhat like this:

    >>> my_api.deploy()

        Deployment Report:
        ------------------

        This is an automatically generated report on the status of your deployed
        product. Your API is now containerized and hosted on the workbench. You
        can access the API using:

        http://XXX.XXX.XX.XXX:XXXXX/<your_route>

        You can call the API in whatever way it is designed. If you want to get
        rid of it, just use the delete_deployment() method. If you just want to
        update the API, you can just use prepare_deployment() to create a new
        Dockerfile and then deploy() again.

                  Your Product
        -----------------------
        Name:       my-product
        Project:    my-project
        Status:     deployed and healthy
        Access:     http://XXX.XXX.XX.XXX:XXXXX/<your_route>

        If you want to export the image to your local machine just use the
        export_product() method. If you want to push it to another registry,
        you can use the push_product() method.

Now you know how to reach your API. In case you find out it doesn't work and you change something on the code, you can just re-run <code>prepare_deployment()</code> and then <code>deploy()</code>. The <code>deploy()</code> will automatically realize that the "product" has already been deployed and will just update the existing one. In case you want to delete a product, you can just use the <code>delete_deployment()</code> method. This will also work for local deployments.

    # delete product
    my_api.delete_deployment(product = "my-product", project = "my-project")

When you are satisfied with your API, you might want to deploy or ship it to an enterprise-ready or collaborative cluster. As the workbench is at the heart a Kubernetes cluster, everything you do on the workbench, will work on any other cluster. To give you the freedom of choice, <code>productionize</code> implements a method to deploy anywhere.

This is the <code>push_product()</code> method. This method pushes the product in form of a Docker image to any registry you want. Default is DockerHub. However, you can select any registry you like. In case of secure registries, you will need credentials or a token. Those will be asked from you with a prompt.

    # push the product
    my_api.push_product(product = "my-product", registry = "my.registry:5000/image-name")

This method will automatically tag the image and run <code>docker push</code> to push the image to any remote industry.

## Next Steps

<code>productionize</code> is far from ready and is still work in progress. I started this project around mid of May 2020, when I was super annoyed when I had to built up a new test cluster on my local machine, cause I messed up the others too much. As this all started with me sitting on my Mac, this project is <b>at the moment only stable on macOS</b>. I already started to work on other UNIX systems, however Windows might take a bit of time. So the next steps are the following:

### Release 1.0

<ol>
    <li>Functional Features:</li>
        <ol>
            <li>Ease the export of products from workbench to local machine</li>
            <li>Integrate the push feature to external cluster registries</li>
        </ol>
    <li>Non-functional Features:</li>
        <ol>
            <li>Update unit testing for product() class</li>
        </ol>
</ol>

### Release 2.0

<ol>
    <li>Functional Features:</li>
        <ol>
            <li>Add workbench management feature</li>
        </ol>
    <li>Non-functional Features:</li>
        <ol>
            <li>Support latest Ubuntu version</li>
            <li>Support latest CentOS version</li>
        </ol>
</ol>