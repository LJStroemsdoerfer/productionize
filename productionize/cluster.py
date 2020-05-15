"""
cluster.py contains the class cluster(), which is allows you to build up a
local Kubernetes cluster. Thus cluster can be managed and even served by the 
product() class object.

Slots:
--------
"""

# import libs
import subprocess
import os

# setup the class
class cluster:

    # describe the class
    def __init__(self):

        # store working directory
        self.wd = os.getcwd()

        # store status of cluster
        self.current_status = None 