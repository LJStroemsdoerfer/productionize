"""
workbench.py contains the class workbench(), which creates the technical setup. 
The class workbench() allows you to install and manage all the components 
necessary for the successfully productionizing your model.

The components you need are:

1. Docker: as a container technology https://www.docker.com
2. VirtualBox: as a driver https://www.virtualbox.org
3. Minikube: as a local Kubernetes cluster https://minikube.sigs.k8s.io/
4. Kubectl: as a Kubernetes CLI https://kubectl.docs.kubernetes.io

"""

# import libs
import subprocess
import os
import sys

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

                                Status                      Purpose
        ---------------------------------------------------------------------
        Docker:         installed == {dk_exists}        Containerization
        VirtualBox:     installed == {vb_exists}        Cluster Hypervisor
        Kubectl:        installed == {kc_exists}        Kubernetes CLI
        Minikube:       installed == {mk_exists}        Local Kubernetes


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
        
    # function to check if components are installed
    def __check_installed(self):

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
    