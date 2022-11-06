# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 08:53:41 2022

@author: alain
"""
import os
import sys

print('_'*20)
print(' Python installed :')
print('   - in     :' , os.path.dirname(sys.executable))
print('   - Version:' , sys.version)
print('_'*20)
print(' Path :')
for dir in sys.path:
    print('   - ' , dir)
print('_'*20)
    