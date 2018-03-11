# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 10:19:30 2016

@author: zdc
"""

import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
    
