"""
workbench.py contains the class workbench(), which creates the technical setup. 
The class workbench() allows you to install and manage all the components 
necessary for the successfully productionizing your model.

The components you need are:

1. Docker: as a container technology https://www.docker.com
2. VirtualBox: as a driver https://www.virtualbox.org
3. Minikube: as a local Kubernetes cluster https://minikube.sigs.k8s.io/
4. Kubectl: as a Kubernetes CLI https://kubectl.docs.kubernetes.io

Slots:
--------
wd : str
    Stores the current working directory
current_status : str
    Stores the current status of the minikube cluster
platform : str
    Stores the platform the host is running on
py_version : string
    Stores the version of Python in use
dk_installed : boolean
    Stores if Docker is already installed
vb_installed : boolean
    Stores if VirtualBox is already installed
kc_installed : boolean
    Stores if kubectl is already installed
mk_installed : boolean
    Stores if minikube is already installed
dk_prev_installed : boolean
    Stores if Docker was already installed
vb_prev_installed : boolean
    Stores if VirtualBox was already installed
kc_prev_installed : boolean
    Stores if kubectl was already installed
mk_prev_installed : boolean
    Stores if minikube was already installed
current_projects : list
    Stores all active projects on the workbench
cpus_used : string
    Stores the CPUs allocated to the workbench
memory_used : string
    Stores the memory allocated to the workbench
"""

# import libs
import subprocess
import os
import sys
import re
import warnings

# setup the class
class workbench:

    # define the class object
    def __init__(self):

        # store the working directory
        self.wd = os.getcwd()

        # store the status
        self.current_status = 'initialized'

        # store the platform
        self.platform = sys.platform

        # check python version
        major_v = str(sys.version_info[0])
        minor_v = str(sys.version_info[1])
        micro_v = str(sys.version_info[2])

        # write to slot
        self.py_version = str(major_v + '.' + minor_v + '.' + micro_v)
        
        # store if components are installed
        self.vb_installed = None
        self.dk_installed = None
        self.kc_installed = None
        self.mk_installed = None

        # check if components were installed
        self.__check_installed()

        # store prev installed
        self.dk_prev_installed = self.dk_installed
        self.vb_prev_installed = self.vb_installed
        self.kc_prev_installed = self.kc_installed
        self.mk_prev_installed = self.mk_installed

        # store component versions
        self.dk_version = None
        self.vb_version = None
        self.kc_version = None
        self.mk_version = None

        # store memory usage
        self.cpus_used = None
        self.memory_used = None

        # welcome message
        welcome_message = """

                                                    Welcome to
        ██████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗██╗███████╗███████╗
        ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██║╚══███╔╝██╔════╝
        ██████╔╝██████╔╝██║   ██║██║  ██║██║   ██║██║        ██║   ██║██║   ██║██╔██╗ ██║██║  ███╔╝ █████╗  
        ██╔═══╝ ██╔══██╗██║   ██║██║  ██║██║   ██║██║        ██║   ██║██║   ██║██║╚██╗██║██║ ███╔╝  ██╔══╝  
        ██║     ██║  ██║╚██████╔╝██████╔╝╚██████╔╝╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║██║███████╗███████╗
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝
                                                                                                    
                                                                                                    
                        productionize is an open-source lightweight ML deployment tool.
                        You can containerize, deploy and ship your model, without ever
                        having to leave your beloved Python.


        Before we start, we will first setup your local workbench. The workbench is a collection of tools
        we need to do all those amazing things. You are running the following setup:

        Platform: {operating_system}
        Python:   {python_version}
        Cores:    {number_cores}

        The main components of the workbench are containerization and orchestration tools. I know there are
        many different tools out there, but we are using:

                  Already on machine      Purpose
        ------------------------------------------------------
        Docker:         {dk_exists}        Containerization
        VirtualBox:     {vb_exists}        Cluster Hypervisor
        Kubectl:        {kc_exists}        Kubernetes CLI
        Minikube:       {mk_exists}        Local Kubernetes


        You can download the missing components and configure them using: workbench.setup(). Don't worry
        though, using workbench.delete(), you will be able to cleanly uninstall all the components again.

        """.format(operating_system = self.platform,
                   python_version = self.py_version,
                   number_cores = os.cpu_count(),
                   dk_exists = self.dk_prev_installed,
                   vb_exists = self.vb_prev_installed,
                   kc_exists = self.kc_prev_installed,
                   mk_exists = self.mk_prev_installed)

        # print welcome message
        print(welcome_message)

        # check if brew exists
        try:
            
            # update brew before starting
            subprocess.call('brew update'.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        # if it crashed
        except:

            # raise Exception
            raise Exception('homebrew is not installed on your machine, please install it here: https://brew.sh')

        # add project slot
        self.current_projects = []
        
    # helper function to check if components are installed
    def __check_installed(self):

        """
        Helper method to check if components are already installed.

        This function tests if the main components Docker, VirtualBox, Kubectl
        and Minikube are already installed.
        """

        # try to call docker
        try:

            # call docker
            subprocess.call('docker version'.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # if it did not crash, it is installed
            self.dk_installed = True

        # if it crashes
        except:

            # it is not installed
            self.dk_installed = False
        
        # try to call virtualbox
        try:

            # call virtualbox
            subprocess.call('virtualbox --help'.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # if it did not crash, it is installed
            self.vb_installed = True

        # if it crashes
        except:

            # it is not installed
            self.vb_installed = False

        # try to call kubectl
        try:

            # call kubectl
            subprocess.call('kubectl config view'.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # if it did not crash, it is installed
            self.kc_installed = True

        # if it crashes
        except:

            # it is not installed
            self.kc_installed = False

        # try to call minikube
        try:

            # call minikube
            subprocess.call('minikube version'.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            # if it did not crash, it is installed
            self.mk_installed = True

        # if it crashes
        except:

            # it is not installed
            self.mk_installed = False

    # main function to debug
    def setup_debug(self, issue = "docker"):

        """
        main method to debug the setup() method.

        This function helps to debug any issues in the setup of the
        workbench. This method is supposed to give users some hints
        in case something goes wrong.

        Parameters
        ----------
        issue : string
            indicates what component should be investigated, the default is
            "docker", alternatives are "virtualbox", "kubectl" and "minikube".
        """

        # check if issue docker:
        if issue == 'docker':

            # install docker
            subprocess.call('brew cask install docker'.split())

        # check if issue virtualbox
        if issue == 'virtualbox':

            # install virtualbox
            subprocess.call('brew cask install virtualbox --force'.split())
        
        # check if issue kubectl
        if issue == 'kubectl':

            # install kubectl
            subprocess.call('brew install kubectl'.split())

        # check if issue minikube
        if issue == 'minikube':

            # install minikube
            subprocess.call('brew install minikube'.split())

            # link cli version
            subprocess.call('brew link --overwrite kubernetes-cli'.split())

    # helper function to install docker
    def __install_docker(self):

        """
        helper method to install Docker.

        This function downloads and sets up Docker Desktop. The user can then 
        use the Docker Desktop interface to log in.
        """

        # check if Docker is already installed
        if self.dk_prev_installed:

            #  collect version
            dk_version = subprocess.check_output('docker version --format "{{.Server.Version}}"'.split())
            dk_version = '.'.join(re.findall(r'\d+', str(dk_version)))

        # if it is not installed already
        else:

            # try to install docker
            try:

                # install docker
                dk_install_success = subprocess.call('brew cask install docker'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if dk_install_success == 0:

                    # set dk_install_success to True
                    dk_install_success = True
                
                # if it didn't work
                else:

                    # set dk_install_success to False
                    dk_install_success = False

            # handle crash
            except:

                # set dk_install_success to False
                dk_install_success = False

            # check if it worked
            if dk_install_success:

                # print message
                print ('> Docker was successfully installed')

                # update version
                dk_version = 'log in first'

            # if it didn't work
            else:

                # stop function
                raise Exception('Docker could not be installed, run setup_debug(issue = "docker") to print detailed logs')

        # write docker version to self
        self.dk_version = dk_version
        
    # helper function to install virtualbox
    def __install_virtualbox(self):

        """
        helper method to install VirtualBox.

        This function downloads and sets up VirtualBox. The users can now use
        VirtualBox to start VMs on their local machine.
        """

        # check if Virtualbox is already installed
        if self.vb_prev_installed:

            #  collect version
            vb_version = subprocess.check_output('vboxmanage --version'.split())
            vb_version = '.'.join(re.findall(r'\d+', str(vb_version))[0:3])

        # if it is not installed already
        else:

            # try to install virtualbox
            try:

                # install virtualbox
                vb_install_success = subprocess.call('brew cask install virtualbox --force'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if vb_install_success == 0:

                    # set vb_install_success to True
                    vb_install_success = True
                
                # if it didn't work
                else:

                    # set vb_install_success to False
                    vb_install_success = False

            # handle crash
            except:

                # set vb_install_success to False
                vb_install_success = False

            # check if it worked
            if vb_install_success:

                # try to collect version
                try:

                    # check the version
                    vb_version = subprocess.check_output('vboxmanage --version'.split())
                    vb_version = '.'.join(re.findall(r'\d+', str(vb_version))[0:3])

                    # print message
                    print ('> VirtualBox was successfully installed')
                
                # handle exception
                except:

                    # stop function
                    raise Exception('VirtualBox could not be installed, run setup_debug(issue = "virtualbox") to print detailed logs')

            # if it didn't work
            else:

                # stop function
                raise Exception('VirtualBox could not be installed, run setup_debug(issue = "virtualbox") to print detailed logs')

        # write VirtualBox version to self
        self.vb_version = vb_version

    # helper function to install kubectl
    def __install_kubectl(self):

        """
        helper method to install kubectl.

        This function downloads and sets up kubectl as a kubernetes-cli.
        """

        # check if kubectl is already installed
        if self.kc_prev_installed:

            #  collect version
            kc_version = subprocess.check_output('kubectl version --client=true'.split())
            kc_version = '.'.join(re.findall(r'\d+', str(kc_version))[0:2])

        # if it is not installed already
        else:

            # try to install kubectl
            try:

                # install kubectl
                kc_install_success = subprocess.call('brew install kubectl'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if kc_install_success == 0:

                    # set kc_install_success to True
                    kc_install_success = True
                
                # if it didn't work
                else:

                    # set kc_install_success to False
                    kc_install_success = False

            # handle crash
            except:

                # set kc_install_success to False
                kc_install_success = False

            # check if it worked
            if kc_install_success:

                # try to catch version
                try:

                    # check the version
                    kc_version = subprocess.check_output('kubectl version --client=true'.split())
                    kc_version = '.'.join(re.findall(r'\d+', str(kc_version))[0:2])

                    # print message
                    print ('> Kubectl was successfully installed')

                # handle exception
                except:

                    # stop function
                    raise Exception('Kubectl could not be installed, run setup_debug(issue = "kubectl") to print detailed logs')

            # if it didn't work
            else:

                # stop function
                raise Exception('Kubectl could not be installed, run setup_debug(issue = "kubectl") to print detailed logs')

        # write Kubectl version to self
        self.kc_version = kc_version

    # helper function to install minikube
    def __install_minikube(self):

        """
        helper method to install Minikube.

        This function downloads and sets up Minikube, which is a local 
        Kubernetes implementation.
        """

        # check if minikube is already installed
        if self.mk_prev_installed:

            #  collect version
            mk_version = subprocess.check_output('minikube version'.split())
            mk_version = '.'.join(re.findall(r'\d+', str(mk_version))[0:3])

        # if it is not installed already
        else:

            # try to install minikube
            try:

                # install minikube
                mk_install_success = subprocess.call('brew install minikube'.split(), stdout=subprocess.DEVNULL)

                # link kubectl
                subprocess.call('brew link --overwrite kubernetes-cli'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if mk_install_success == 0:

                    # set mk_install_success to True
                    mk_install_success = True
                
                # if it didn't work
                else:

                    # set mk_install_success to False
                    mk_install_success = False

            # handle crash
            except:

                # set kc_install_success to False
                mk_install_success = False

            # check if it worked
            if mk_install_success:

                # try to collect version
                try:

                    # check the version
                    mk_version = subprocess.check_output('minikube version'.split())
                    mk_version = '.'.join(re.findall(r'\d+', str(mk_version))[0:3])

                    # print message
                    print ('> Minikube was successfully installed')

                # handle exception
                except:

                    # stop function
                    raise Exception('Minikube could not be installed, run setup_debug(issue = "minikube") to print detailed logs')

            # if it didn't work
            else:

                # stop function
                raise Exception('Minikube could not be installed, run setup_debug(issue = "minikube") to print detailed logs')

        # write VirtualBox version to self
        self.mk_version = mk_version

    # main function to setup the workbench
    def setup(self, report = True):

        """
        main method to setup the workbench.

        This function downloads and sets up all components necessary for the
        workbench. The components include Docker, VirtualBox, Kubectl and
        Minikube.

        Parameters
        ----------
        report : boolean
            if True a process report is printed with the progress on the
            installation
        """

        # install docker
        self.__install_docker()

        # install virtualbox
        self.__install_virtualbox()

        # install kubectl
        self.__install_kubectl()

        # install minikube
        self.__install_minikube()

        # check if all components can be detected
        self.__check_installed()

        # check if the report should be printed
        if report:

            # build report
            report = """

            Setup Report:
            -------------

            This is an automatically generated report on the setup process of your local workbench. The set
            of components required for the workbench to work were processed as follows:

                                Status                     Version
            ---------------------------------------------------------------------
            Docker:         installed == {dk_exists}        {dk_version}
            VirtualBox:     installed == {vb_exists}        {vb_version}
            Kubectl:        installed == {kc_exists}        {kc_version}
            Minikube:       installed == {mk_exists}        {mk_version}

            In case not all components could be installed, please consult the setup_debug() method. This
            method prints out the system logs when installing and configuring the components.


            ! | If Docker was newly installed, you will need to log in to start Docker Desktop and log in
            ! | or create an account at Dockerhub https://hub.docker.com. In case you have any questions,
            ! | please consult: https://www.docker.com/products/docker-desktop.

            """.format(dk_exists = self.dk_version,
                       vb_exists = self.vb_prev_installed,
                       kc_exists = self.kc_prev_installed,
                       mk_exists = self.mk_prev_installed,
                       dk_version = self.dk_version,
                       vb_version = self.vb_version,
                       kc_version = self.kc_version,
                       mk_version = self.mk_version)

            # print report
            print (report)

        # update status
        self.current_status = 'installed'

    # main function to start cluster
    def start_cluster(self, cpus = '2', memory = '2G'):

        """
        main method to start the workbench cluster

        This function initiates and starts the local workbench cluster. The
        cluster is a Kubernetes based composition of Docker, VirtualBox,
        Kubectl and Minikube.

        Parameters
        ----------
        cpus : string
            indicates the number of cores the cluster can use as resources
        memory : string
            indicates the amount of memory the cluster can use
        """

        # try to start minikube
        try:

            # start minikube
            subprocess.call(str('minikube start --driver=virtualbox --cpus=' + cpus + ' --memory=' + memory).split())

            # update status
            self.current_status = 'running'

            # update resource usage
            self.cpus_used = cpus
            self.memory_used = memory

        # handle exception
        except:

            # update status
            self.current_status = 'crashed'

            # raise exception
            raise Exception('I could not start the cluster')

    # main function to open a new project
    def open_project(self, name = None):

        """
        main method to open projects on the workbench cluster.

        This function opens a new project on the workbench cluster. Technically
        speaking, this function creates a new Kubernetes namespace.

        Parameters
        ----------
        name : string
            indicates the project name, but should not have spaces or any
            separators, others than "-"
        """

        # check if project name was given
        if name is None:

            # assign default project name
            name = 'my-project'
        
        # if name was given
        else:

            # ensure the name complies with standards
            name = name.replace('_', '-').replace('/', '-')

        # try to create a new namespace
        try:

            # create new namespace
            subprocess.call(str('kubectl create namespace ' + name).split(), stdout=subprocess.DEVNULL)

            # send message
            print (str('> Successfully created project: ' + name))

            # add to list of projects
            self.current_projects.append(name)
        
        # if it crashed
        except:

            # raise Exception
            raise Exception('I could not create the new project')
    
    # main method to list all current projects
    def list_projects(self):

        """
        main method to list all projects on the workbench cluster.

        This function lists all projects that are currently on the workbench.
        """

        # print list with all projects on the workbench
        return self.current_projects

    # main method to list all products in project
    def list_products(self, project):

        """
        main method to list all products in a projec.

        This function lists all products that are currently deployed in a
        project on the workbench.

        Parameters
        ----------
        project : string
            String that gives the name of the project, for which products should be listed
        """

        # try to list all products
        try:

            # retrieve list of products
            command = str("kubectl get pods --template=\'{{range .items}}{{.metadata.name}}{{","}}{{end}}\' -n " + project)
            product_list = os.popen(command).read()

            # return product list
            return product_list

        # handle exception
        except:

            # print message
            print (str('It seems that there are no products deployed for your project: ' + project))

    # main method to delete a project
    def delete_project(self, name = None):

        """
        main method to delete projects on the workbench cluster.

        This function deletes a project on the workbench cluster. Technically
        speaking, this function deletes a Kubernetes namespace. To do so,
        the methods requires a project name

        Parameters
        ----------
        name : string
            indicates the project name, but should not have spaces or any
            separators, others than "-"
        """

        # check if name was given
        if name is None:

            # break function
            raise Exception('You need to provide a name for the project you want to delete')
        
        # if name was provided
        else:

            # try to delete the project
            try:

                # delete project    
                subprocess.call(str('kubectl delete namespaces ' + name).split(), stdout=subprocess.DEVNULL)

                # print message
                print (str('> Successfully deleted project: ' + name))

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete the project')

            # try to delete project out of list
            try:

                # delete project out of list
                self.current_projects.remove(name)
            
            # handle exception
            except:

                # print warning
                warnings.warn('I could not find the project in self.current_projects')

    # main function to give status report on cluster
    def inspect(self):

        """
        main method to build a status report on cluster.

        This function builds a report on the current workbench. It shows how
        many products, projects and resources are bound.
        """

        # check if all components are running
        self.__check_installed()

        # calculate number of projects
        project_counter = len(self.current_projects)

        # initialize product counter
        product_counter = 0

        # loop over all projects to count products
        for project in self.current_projects:

            # get the products deployed
            products_in_project = self.list_products(project = project)
            
            # split in list and count length
            product_counter = product_counter + len(products_in_project.split(','))

            # return
            return product_counter

        # build report
        report = """

        Workbench Report:
        -----------------

        This is an automatically generated report on your workbench. Your
        workbench consists of four main components:

                              Status                     Version
        ---------------------------------------------------------------------
        Docker:         installed == {dk_exists}        {dk_version}
        VirtualBox:     installed == {vb_exists}        {vb_version}
        Kubectl:        installed == {kc_exists}        {kc_version}
        Minikube:       installed == {mk_exists}        {mk_version}

        You are running this session with Python {python_version}. Your machine
        has {number_cores}. In total you allocated the following resources to
        the workbench:

        Cores:      {cpus_used}
        Memory:     {memory_used}

        Your workbench is currently hosting {product_counter} product in 
        {project_counter} project(s).

        """.format(operating_system = self.platform,
                   python_version = self.py_version,
                   number_cores = os.cpu_count(),
                   dk_exists = self.dk_installed,
                   vb_exists = self.vb_installed,
                   kc_exists = self.kc_installed,
                   mk_exists = self.mk_installed,
                   cpus_used = self.cpus_used,
                   memory_used = self.memory_used,
                   project_counter = project_counter,
                   product_counter = product_counter)

        # print report
        print (report)

    # main function to stop cluster
    def stop_cluster(self):

        """
        main method to stop the workbench cluster.

        This function stops the running workbench cluster.
        """

        # try to stop minikube
        try:

            # stop cluster
            subprocess.call('minikube stop'.split(), stdout=subprocess.DEVNULL)

            # update status
            self.current_status = 'stopped'

            # print message
            print ('> Successfully stopped the cluster')

        # handle exception
        except:

            # update status
            self.current_status = 'not responding'

            # raise exception
            raise Exception('I could not stop the cluster')

    # main function to uninstall workbench
    def uninstall(self, docker = None, kubectl = None, virtualbox = None, minikube = None, report = True):

        """
        main method to uninstall all components.

        This function cleanly uninstalls all components used for the workbench.
        The user can decide if a specific component is removed. If no input is
        given, the components that already were present, the components are 
        kept. For those components not present, the removal is processed.

        Parameters
        ----------
        docker : boolean
            indicates if docker should be removed from the machine
        kubectl : boolean
            indicates if kubectl should be removed from the machine
        virtualbox : boolean
            indicates if virtualbox should be removed from the machine
        minikube : boolean
            indicates if minikube should be removed from the machine
        report : True
            if True a process report is printed with the progress on the
            installation
        """

        # check if minikube should be deleted
        if minikube is None:

            # check if it was installed before
            if self.mk_prev_installed:

                # don't delete if it was there before
                minikube = False
            
            # if it wasn't installed before
            else:

                # delete if it wasn't there before
                minikube = True

        # check if kubectl should be deleted
        if kubectl is None:

            # check if it was installed before
            if self.kc_prev_installed:

                # don't delete if it was there before
                kubectl = False

            # if it wasn't installed before
            else:

                # delete if it wasn't there before
                kubectl = True

        # check if virtualbox should be deleted
        if virtualbox is None:

            # check if it was installed before
            if self.vb_prev_installed:

                # don't delete if it was there before
                virtualbox = False 

            # if it wasn't installed before
            else:

                # delete if it wasn't there before
                virtualbox = True
        
        # check if docker should be deleted
        if docker is None:

            # check if it was installed before
            if self.dk_prev_installed:

                # don't delete if it was there before
                docker = False

            # if it wasn't installed before
            else:

                # delete if it wasn't there before
                docker = True

        # check if Minikube should be deleted
        if minikube:

            # try to delete minikube
            try:

                # delete minikube
                mk_deleted = subprocess.call('brew uninstall minikube --force'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if mk_deleted == 0:

                    # print message
                    print ('> Successfully deleted Minikube')

                # if it didn't work
                else:

                    # raise Exception
                    raise Exception('I could not delete Minikube')

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete Minikube')

        # check if kubectl should be deleted
        if kubectl:

            # try to delete kubectl
            try:

                # delete kubectl
                kc_deleted = subprocess.call('brew uninstall kubectl --force'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if kc_deleted == 0:

                    # print message
                    print ('> Successfully deleted Kubectl')
                
                # if it didn't work
                else:

                    # raise Exception
                    raise Exception('I could not delete Kubectl')

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete Kubectl')

        # check if virtualbox should be deleted
        if virtualbox:

            # try to delete virtualbox
            try:

                # delete virtualbox
                vb_deleted = subprocess.call('brew cask uninstall virtualbox --force'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if vb_deleted == 0:

                    # print message
                    print ('> Successfully deleted VirtualBox')

                # if it didn't work
                else:

                    # raise Exception
                    raise Exception('I could not delete VirtualBox')

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete VirtualBox')

        # check if docker should be deleted
        if docker:

            # try to delete docker
            try:

                # delete docker
                dk_deleted = subprocess.call('brew cask zap docker --force'.split(), stdout=subprocess.DEVNULL)
                dk_deleted = subprocess.call('brew cask zap docker --force'.split(), stdout=subprocess.DEVNULL)

                # check if it worked
                if dk_deleted == 0:

                    # print message
                    print ('> Successfully deleted Docker')
                
                # if it didn't work
                else:

                    # raise Exception
                    raise Exception('I could not delete Docker')

            # handle exception
            except:

                # raise Exception
                raise Exception('I could not delete Docker')

        # check if they are still installed
        self.__check_installed()

        # check if report should be printed
        if report:

            # build report
            report = """

            Deletion Report:
            ----------------

            This is an automatically generated report on the uninstall process of your local workbench. The set
            of components required for the workbench to work were processed as follows:

                        Still on machine               
            --------------------------------
            Docker:         {dk_exists}       
            VirtualBox:     {vb_exists}  
            Kubectl:        {kc_exists}
            Minikube:       {mk_exists}


            """.format(dk_exists = self.dk_installed,
                    vb_exists = self.vb_installed,
                    kc_exists = self.kc_installed,
                    mk_exists = self.mk_installed)

            # print report
            print (report)