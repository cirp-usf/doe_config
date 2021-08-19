# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 10:40:46 2021

@author: Steffen
"""



import numpy as np
import csv
import os.path


basepath = os.path.dirname(__file__)

csvfile = os.path.join(basepath, 'step', 'laser_modules.csv')




def load_modules():
    with open(csvfile) as f:
        csvreader = csv.reader(f.readlines(), delimiter=';')

    # Discard the first line
    next(csvreader)
    module_data = []
    for row in csvreader:
        rec = [row[0]]
        rec.extend(list(map(float, row[1:])))
        module_data.append(rec)
    return module_data

def suggest_laser(InputWave, InputPower, InputWeighting):
    
    df = np.genfromtxt(csvfile, delimiter=';',skip_header=1,usecols=(1,2))
    
    rows, columns = df.shape
    
    values = [x for x in range(0, rows)]
    df = np.insert(df, 0, values, axis=1)
    
    
    column0 = df[:,1:2]
    MaxWave=np.amax(column0,axis=0)
    MinWave=np.amin(column0,axis=0)
    ScaledWave=(column0-MinWave)/(MaxWave-MinWave)
    df = np.hstack((df, ScaledWave))
    ScaledInputWave=(InputWave-MinWave)/(MaxWave-MinWave)
    diffwave=abs(ScaledWave-ScaledInputWave)*InputWeighting
    df = np.hstack((df, diffwave))
    
    column1 = df[:,2:3]
    MaxPower=np.amax(column1,axis=0)
    MinPower=np.amin(column1,axis=0)
    ScaledPower=(column1-MinPower)/(MaxPower-MinPower)
    df = np.hstack((df, ScaledPower))
    ScaledInputPower=(InputPower-MinPower)/(MaxPower-MinPower)
    diffpower=abs(ScaledPower-ScaledInputPower)*(1-InputWeighting)
    df = np.hstack((df, diffpower))
    
    
    Distance= np.sqrt(diffwave*diffwave+diffpower*diffpower)
    df = np.hstack((df, Distance))
    idx = df[:,7].argsort()[0]
    lmodules = load_modules()
    return lmodules[idx], idx
    

