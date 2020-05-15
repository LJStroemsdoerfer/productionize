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

# setup the class
class workbench:

    # define the class
    def __init__(self):

        # store the working directory
        self.wd = os.getcwd()

        # define the status
        self.current_status = None 

    