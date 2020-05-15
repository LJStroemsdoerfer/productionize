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
"""

# import libs
import subprocess
import os

# setup the class
class product:

    # describe the class
    def __init__(self):

        # store working directory
        self.wd = os.getcwd()

        # store status of product
        self.current_status = 'initialized'