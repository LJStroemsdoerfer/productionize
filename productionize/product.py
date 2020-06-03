"""
product.py contains the class product(), which is at the center of productionizing 
your ML model. The product() class takes an API script and allows you to easily
containerize the API. You can then deploy the container, export the image or call
the deployed API.

Slots:
--------
wd : string
    Current working directory
current_status : string
    Current status of the product
py_version : string
    Python version in use in the current session
product_name : string
    Name of your product to deploy
project_name : string
    Name of your project on the workbench
api_file : string
    Contains the path to the api_file that should be used
requirements_file : string
    Contains the path to the requirements_file that should be used
port : string
    Contains the port the API should be exposed to
service_url : string
    Contains the url to reach your service
local : boolean
    If True, the product will be deployed on localhost
"""

# import libs
import subprocess
import os
import sys

# setup the class
class product:

    # describe the class
    def __init__(self, name = None, project = None):

        # store working directory
        self.wd = os.getcwd()

        # store status of product
        self.current_status = 'initialized'

        # check python version
        major_v = str(sys.version_info[0])
        minor_v = str(sys.version_info[1])
        micro_v = str(sys.version_info[2])

        # write to slot
        self.py_version = str(major_v + '.' + minor_v + '.' + micro_v)

        # check if product name was given
        if name is None:

            # give default name
            name = 'my-product'
    
        # store name in self
        self.product_name = name.replace('_', '-').replace('/', '-')

        # check if project name was given
        if project is None:

            # give default name
            project = 'my-project'

        # store project name
        self.project_name = project.replace('_', '-').replace('/', '-')

        # store path to api file
        self.api_file = None

        # store path to requirements file
        self.requirements_file = None

        # store port to deploy
        self.port = None

        # store service url
        self.service_url = None

        # store if local deployment
        self.local = None
    
        # build report
        report = """

        Product Report:
        ---------------

        This is an automatically generated report on the status of your product 
        deployment. productionize considers a product to be a deployable API.

          Your Product
        -----------------------
        Name:       {product}
        Project:    {project}
        Status:     {status}

        With the product class you can easily deploy your python API, without
        leaving python. You first have to prepare the deployment, which will
        trigger the build of a Dockerfile in your current working directory:

            # initialize the class
            your_api = product()

            # prepare the deployment
            your_api.prepare_deployment(api_file = "/path/api.py",
                                        requirements_file = "/path/requirements.txt",
                                        port = "8000")
        
        Then you can simply deploy your API using your_api.deploy(). I split
        the deployment process in two parts, so that you are able to adjust
        the Dockerfile, if you need to.

        If you want to delete the a deployment, you can just use delete_deployment().
        In case you want to update a deployment, just prepare and then deploy again.

        """.format(product = self.product_name,
                   project = self.project_name,
                   status = self.current_status)

        # print report
        print (report)

    # helper method to build Dockerfile
    def __build_dockerfile(self):

        """
        Private method to build a Dockerfile.
        This function first builds a Docker file from a python script and 
        a requirements.txt.
        """

        # try create a dockerfile
        try:

            # store dk_file_path
            dk_file_path = str(self.wd + '/Dockerfile')

            # open a new file
            subprocess.call(str('touch ' + dk_file_path).split(), stdout=subprocess.DEVNULL)

            # write content
            content = """\
            FROM python:{version}
            RUN mkdir -p /api
            COPY {api_file} /api/api.py
            COPY {requirements_file} /api/requirements.txt
            RUN python -m pip install -r /api/requirements.txt
            EXPOSE {port}
            ENTRYPOINT ["python", "api/api.py"]\
            """.format(version=self.py_version,
                    api_file = self.api_file,
                    requirements_file = self.requirements_file,
                    port = int(self.port))

            # open Dockerfile
            file = open(dk_file_path, "w")

            # write content to Dockerfile
            file.write(content)

            # close connection
            file.close()

            # write file path to self
            self.dk_file_path = dk_file_path

            # check if it worked
            if self.dk_file_path is None:

                # raise Exception
                raise Exception('I could not create the Dockerfile in your current working directory: ' + self.wd)

        # handle exception
        except:

            # raise exception
            raise Exception(str('I could not create the Dockerfile in your current working directory: ' + self.wd))

    # main function to deploy API
    def prepare_deployment(self, api_file, requirements_file, port):

        """
        Main method to prepare the deployment.

        This function builds a dockerfile out of the script and the require-
        ments file provided. Together with the system python version, the
        container is defined. After this function, the user can take a look
        to the Dockerfile and even adjust it, however, at the users own risk.

        Parameters
        ----------
        api_file : string
            String with the path to the python api file
        requirements_file : string
            String with the path to the requirements file
        port : string
            String with the port number to expose
        name : string
            String with the name of your deployment
        """

        # check the api file
        if isinstance(api_file, str):

            # try to read in first lines
            try:

                # read in file
                with open(api_file) as file:
                    first_line_api = file.readline()

                # store to self, but ensure there is no tilde
                self.api_file = api_file.replace('~','')

            # exception handling
            except:

                # raise Exception
                raise Exception(str('I could not find your file: ' + api_file))
        
        # if it is not a string
        else:

            # raise Exception
            raise Exception('api_file arg should be a path anf a filename to your python file that defines the api: e.g. your_folder/your_script.py')
    
        # check the requirements file
        if isinstance(requirements_file, str):

            # try to read in first lines
            try:

                # read in file
                with open(requirements_file) as file:
                    first_line_req = file.readline()

                # store to self, but ensure there is no tilde
                self.requirements_file = requirements_file.replace('~', '')

            # exception handling
            except:

                # raise Exception
                raise Exception(str('I could not find your file: ' + requirements_file))
        
        # if it is not a string
        else:

            # raise Exception
            raise Exception('requirements_file arg should be a path anf a filename to your requirements.txt: e.g. your_folder/your_reqs.txt')

        # check if port is string
        if isinstance(port, str):

            # store to self
            self.port = str(port)

        # if it is not a string
        else:

            # raise exception
            raise Exception('port arg should be a string with the desired exposing port: e.g. port = "8000"')
        
        # build Dockerfile
        self.__build_dockerfile()

        # change status
        self.current_status = 'ready to deploy'

        # build report
        report = """

        Deployment Report:
        ------------------

        This is an automatically generated report on the preparation of your
        deployment. The Dockerfile was built using the following files:

        {api_file}:
        ----------------
        {first_line_api}
        ----------------

        and

        {requirements_file}:
        ----------------
        {first_line_req}
        ----------------

        The Dockerfile is ready to be used. You can inspect your Dockerfile: 
        
        {dk_file_path}

        You can of course edit the file, however, this is at your own risk. The
        processes in the container currently run as root. You can change that
        of course, as long as your API allows you to.

          Your Product
        -----------------------
        Name:       {name}
        Project:    {project}
        Status:     {status}

        You can now deploy your product using the deploy() method.


        """.format(api_file = self.api_file,
                   first_line_api = first_line_api,
                   requirements_file = self.requirements_file,
                   first_line_req = first_line_req,
                   dk_file_path = self.dk_file_path,
                   name = self.product_name,
                   project = self.project_name,
                   status = self.current_status)
    
        # print report
        print (report)

    # helper method to create Dockerfile
    def __build_image(self, local):
        """
        Private method to build a Docker image.

        This function takes the Dockerfile and creates an image on the Minikube
        internal registry.

        Parameters
        ----------
        local : boolean
            If True, the image is build locally
        """

        # try to create the image on the minikube registry
        try:
        
            # make sure this is run from wd
            os.chdir(self.wd)

            # check if local build
            if not local:
                
                # build image from Dockerfile
                command = str('eval $(minikube -p minikube docker-env) && docker build -t ' + self.product_name + '-image:latest .')
                os.system(command)

            # if local build
            else:

                # build image from Dockerfile
                command = str('docker build -t ' + self.product_name + '-image:latest .')
                os.system(command)

        # handle exception
        except:

            # raise exception
            raise Exception('I could not build the Docker image from the Dockerfile. In case you edited the file, please check if that was correct.')

    # helper method to run a deployment
    def __run_deployment(self, local):
        """
        Private method to run a deployment.

        This function uses kubectl to run a deployment on minikube.

        Parameters
        ----------
        local : boolean
            If True, the product is deployed locally instead of on the workbench
        """

        # try to run deployment
        try:
            
            # check if local deployment
            if not local:

                # run deployment
                command = str('kubectl run ' + self.product_name + ' --image=' + self.product_name + "-image:latest --image-pull-policy='Never' -n " + self.project_name)
                os.system(command)
            
            # if local true
            else:

                # run container
                command = str('docker run -p ' + self.port + ':' + self.port + ' -d --name ' + self.product_name + ' ' + self.product_name + '-image')
                os.system(command)

        # handle exception
        except:

            # raise exception
            raise Exception('I could not run the deployment from the Docker image, make sure the Dockerfile is working.')

    # helper method to expose pod
    def __expose_pod(self):

        """
        Private method to expose a deployment.

        This function exposes the pod that was just deployed.
        """

        # try to expose the pod
        try:

            # expose the pod
            command = str('kubectl expose pod ' + self.product_name + ' --port=' + self.port + ' --type=NodePort -n ' + self.project_name)
            subprocess.call(command.split(), stdout=subprocess.DEVNULL)

        # handle exception
        except:

            # raise exception
            raise Exception('I could not expose the service, make sure your workbench is setup properly')

    # helper method to get the url
    def __get_url(self):

        """
        Private method to get the url of a deployment.

        This function exposes the service on a minikube level an retreives
        the url.
        """

        # try to expose service
        try:

            # expose the service on minikube
            command = str('minikube service ' + self.product_name + ' -n ' + self.project_name + ' --url')
            service_url = subprocess.check_output(command.split())

            # decode url
            service_url = str(service_url.decode("utf-8")).replace("\n", "")
                
            # add route warning
            service_url = service_url + str('/<your_route>')

            # write the url to self
            self.service_url = service_url

        # handle exception
        except:

            # raise exception
            raise Exception('I could not expose the service to your host machine. Make sure the workbench is properly setup.')

    # helper function to check if deployment exists
    def __check_pods(self, product, project):

        """
        Private method to check if a pod exists.

        This function checks, if a pod already exists on Minikube.

        Parameters
        ----------
        product : string
            String with the name of the product
        project : string
            String with the name of the project
        """

        # try to check if service exists
        try:

            # check for service
            command = str('kubectl get pod ' + product + ' -n' + project)
            exists = subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check result
            if exists == 0:

                # return False
                return True
            
            # if not 0, then False
            else:

                # return False
                return False
        
        # if it breaks, it doesn't exist
        except:

            # return False
            return False

    # helper function to check if service exists
    def __check_svcs(self, product, project):

        """
        Private method to check if a svc exists.

        This function checks, if a svc already exists on Minikube.

        Parameters
        ----------
        product : string
            String with the name of the product
        project : string
            String with the name of the project
        """

        # try to check if service exists
        try:

            # check for service
            command = str('kubectl get services ' + product + ' -n' + project)
            exists = subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check result
            if exists == 0:

                # return False
                return True
            
            # if not 0, then False
            else:

                # return False
                return False
        
        # if it breaks, it doesn't exist
        except:

            # return False
            return False

    # helper function to check if container exists
    def __check_container(self, product):

        """
        Private method to check if a container exists.

        This function checks, if a container already exists on localhost.

        Parameters
        ----------
        product : string
            String with the name of the product
        """

        # try to check if container exists
        try:

            # check for service
            command = str('docker container inspect ' + product)
            exists = subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # check result
            if exists == 0:

                # return False
                return True
            
            # if not 0, then False
            else:

                # return False
                return False
        
        # if it breaks, it doesn't exist
        except:

            # return False
            return False

    # helper function to delete pod
    def __delete_pod(self, product, project):

        """
        Main method to delete pod.

        This function deletes the pods of specific products and all
        Minikube artifacts with it.

        Parameters
        ----------
        product : string
            String that gives the name of the product deployment that should be deleted
        project : string
            String that gives the name of the project in which the product should be deleted
        """

        # try to delete pod
        try:

            # delete the pod
            command = str('kubectl delete pod ' + product + ' -n ' + project)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        # handle exception
        except:

            # raise exception
            raise Exception('I could not delete the pod for deployment: ' + product)

    # helper function to delete service
    def __delete_services(self, product, project):

        """
        Main method to delete services.

        This function deletes the services of specific products and all
        Minikube artifacts with it.

        Parameters
        ----------
        product : string
            String that gives the name of the product deployment that should be deleted
        project : string
            String that gives the name of the project in which the product should be deleted
        """

        # try to delete service
        try:

            # delete the service
            command = str('kubectl delete service ' + product + ' -n ' + project)
            subprocess.call(command.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        # handle exception
        except:

            # raise exception
            raise Exception('I could not delete the service for deployment: ' + product)    

    # helper function to delete docker container
    def __delete_container(self, product):

        """
        Main method to delete container.

        This function deletes the a locally running Docker container

        Parameters
        ----------
        product : string
            String that gives the name of the product deployment that should be deleted
        """

        # try to delete a container
        try:

            # stop the container
            command = str('docker stop ' + product)
            subprocess.call(command.split(), stdout=subprocess.DEVNULL)

            # rm container
            command = str('docker rm ' + product)
            subprocess.call(command.split(), stdout=subprocess.DEVNULL)

        # handle exception
        except:

            # raise exception
            raise Exception('I could not delete the container for deployment: ' + product)

    # main method to delete products
    def delete_deployment(self, product, project):

        """
        Main method to delete deployments.

        This function deletes the deployment of specific products and all
        Minikube artifacts with it.

        Parameters
        ----------
        product : string
            String that gives the name of the product deployment that should be deleted
        project : string
            String that gives the name of the project in which the product should be deleted
        """

        # try to delete the product deployment
        try:

            # check if local deployment
            if not self.local:

                # check if pod exists
                if self.__check_pods(product = product, project = project):

                    # delete the pod
                    self.__delete_pod(product = product, project = project)

                # if it does not exist
                else:

                    # print message
                    print ('There is no pod for your deployment: ' + product)

                # check if service exists
                if self.__check_svcs(product = product, project = project):

                    # delete the pod
                    self.__delete_services(product = product, project = project)

                # if it does not exist
                else:

                    # print message
                    print ('There is no service for your deployment: ' + product)

            # if local
            else:

                # check if the container exists
                if self.__check_container(product = product):

                    # delete the container
                    self.__delete_container(product = product)

                # if it does not exist
                else:

                    # print message
                    print ('There is no container for your deployment: ' + product)

        # handle exception
        except:

            # raise exception
            raise Exception(str('I could not delete the deployment of your product: ' + product))

    # main method to deploy product
    def deploy(self, local = False):

        """
        Main method to deploy the product.

        This function takes the Dockerfile and deploys it to the workbench. The
        user can also choose to just run the container locally.

        Parameters
        ----------
        local : boolean
            if set to True, the product is build locally and not deployed to
            the workbench.
        """
        # check if product is already prepared
        if self.dk_file_path is None:

            # raise Exception
            raise Exception('You first need to run prepare_deployment() before deploying your product.')

        # store local in self
        self.local = local

        # check if local build requested
        if not self.local:

            # build docker image on Minikube registry
            self.__build_image(local = self.local)

            # check if already exists
            pod_exists_already = self.__check_pods(product = self.product_name, project = self.project_name)
            svc_exists_already = self.__check_svcs(product = self.product_name, project = self.project_name)

            # if pod already exists delete it
            if pod_exists_already:

                # delete product 
                self.__delete_pod(product = self.product_name,
                                project = self.project_name)

            # if service already exists delete it
            if svc_exists_already:

                # delete service
                self.__delete_services(product = self.product_name,
                                    project = self.project_name)

            # run deployment
            self.__run_deployment(local = local)

            # expose deployment
            self.__expose_pod()

            # get url
            self.__get_url()

            # change the status
            self.current_status = 'deployed and healthy'

            # build report
            report = """

            Deployment Report:
            ------------------

            This is an automatically generated report on the status of your deployed
            product. Your API is now containerized and hosted on the workbench. You
            can access the API using:

            {service_url}

            You can call the API in whatever way it is designed. If you want to get
            rid of it, just use the delete_deployment() method. If you just want to
            update the API, you can just use prepare_deployment() to create a new
            Dockerfile and then deploy() again.

                    Your Product
            -----------------------
            Name:       {name}
            Project:    {project}
            Status:     {status}
            Access:     {service_url}

            You are not forced to stay on your workbench though. You can use
            the push_product() method to push the image of your product to any
            registry you want.
            """.format(service_url = self.service_url,
                    name = self.product_name,
                    project = self.project_name,
                    status = self.current_status)

            # print report
            print (report)
        
        # if local build is requested
        else:

            # build the Docker image locally
            self.__build_image(local = self.local)

            # run the docker container locally
            self.__run_deployment(local = self.local)

            # change the status
            self.current_status = 'deployed and healthy'

            # construct the url
            self.service_url = str('localhost:' + self.port + '/<your_route>')

            # build report
            report = """

            Deployment Report:
            ------------------

            This is an automatically generated report on the status of your deployed
            product. Your API is now containerized and hosted on your local machine.
            You can access the API using:

            {service_url}

            You can call the API in whatever way it is designed. If you want to get
            rid of it, just use the delete_deployment() method. If you just want to
            update the API, you can just use prepare_deployment() to create a new
            Dockerfile and then deploy() again.

                    Your Product
            -----------------------
            Name:       {name}
            Project:    {project}
            Status:     {status}
            Access:     {service_url}

            You are not forced to stay on your local machine though. You can use
            the push_product() method to push the image of your product to any
            registry you want.
            """.format(service_url = self.service_url,
                    name = self.product_name,
                    project = self.project_name,
                    status = self.current_status)

            # print report
            print (report)

    # main method to push product to other registry
    def push_product(self, registry):
        """
        Main method to push your product.

        This function pushes the docker image to any other registry. Depending
        on the privacy setting, the user will need to login to the registry and
        create a token first.

        Parameters
        ----------
        registry : string
            Gives the url to the target registry, if you just push to Dockerhub, 
            just pass your DockerHub user name to the registry arg
        """

        # try to push to the registry
        try:

            # tag the image to a remote registry
            command = str('eval $(minikube -p minikube docker-env) && docker tag ' + self.product_name + '-image ' + registry + '/' + self.product_name + '-image')
            os.system(command)

            # print message
            print (str('> Successfully tagged the image as ' + registry + '/' + self.product_name + '-image'))

            # tag the image to a remote registry
            command = str('eval $(minikube -p minikube docker-env) && docker push ' + registry + '/' + self.product_name + '-image')
            os.system(command)

            # print message
            print (str('> Successfully pushed image to ' + registry))

        # handle exception    
        except:

            # raise exception
            raise Exception('I could not push the product to another registry. Make sure you have the proper registry url and the correct credentials in case it is a private registry.')   