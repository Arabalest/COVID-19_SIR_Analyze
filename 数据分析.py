# coding=utf-8
import requests
import re
import json
import time
import pandas as pd
import matplotlib.pyplot as plt

import scipy.integrate as spi
import numpy as np
import pylab as pl

def GETDATA(file,column):
    df = pd.read_csv(file,header=0,encoding = 'gbk',engine ='python')
    df = df.dropna(subset=[column])#以column为基准删除空值所在的行
    df.drop_duplicates(subset=[column],keep='first',inplace=True)
    #print(df["时间"])
    x_label = []
    for i in df["时间"]:
        i = i.split(" ")
        i = i[0].split(".")
        x_label.append(int(i[0]+i[1]+i[2]))
    y_label = list(df[column])
    df2 = pd.DataFrame(data={'x':x_label,'y':y_label})
    df2.drop_duplicates(subset=['x'],keep='first',inplace=True)
    #print(df2)
    x_label = list(df2['x'])
    y_label = list(df2['y'])
    return x_label,y_label


 

 
def diff_eqs(INP,t):
    '''The main set of equations'''
    Y=np.zeros((3))
    V = INP
    Y[0] = - beta * V[0] * V[1]
    Y[1] = beta * V[0] * V[1] - gamma * V[1]
    Y[2] = gamma * V[1]
    return Y   # For odeint
 
people = {'湖北':5.917e7,
          '上海':2.424e7,
          '全国':1.395e10}

if __name__ == "__main__":
    city = "上海"
    for name in [city+"确诊"]:#[city+"确诊",city+"疑似",city+"治愈",city+"死亡"]
        X,Y = GETDATA("全国情况统计.csv",name)

        #plt.figure()
        #plt.plot(X,Y)
        #plt.show()

        #dometic Gamma: 0.0831 Beta: 0.3929 MSE: 38466.4444444
        #shanghai Gamma: 0.0769 Beta: 0.5 MSE: 38466.4444444
        Mbeta=1
        Mgamma=1
        trueGamma = Mgamma
        trueBeta =  Mbeta
        tmpMSE = -1
        inc = 0.001
        
        TS=1.0
        ND=70.0
        S0=1-1e-6
        I0=Y[0]/people[city]
        INPUT = (S0, I0, 0.0)
        t_range = np.array(X)-20200121
        
        train = 0
        if train == 1:
            for gamma in np.arange(Mgamma,0,-inc):
                for beta in np.arange(Mbeta,0,-inc):
                    RES = spi.odeint(diff_eqs,INPUT,t_range)
                    Infectious = RES[:,1]*people[city]
                    #Infectious= Infectious.astype(int)
                    #Y = np.array(Y,dtype='int')
                    #print(Infectious)
                    #print(Y)
                    #print(Infectious.shape[0])
                    MSE = np.sum((Infectious-Y)**2)/Infectious.shape[0]
                    if tmpMSE == -1:
                        tmpMSE = MSE
                    elif tmpMSE > MSE:
                        tmpMSE = MSE
                        trueGamma = gamma
                        trueBeta =  beta            
                    if MSE <=100:
                        print('MSE < 100','MSE =',tmpMSE)
                        print('Gamma:',gamma,'Beta:',beta)
                        exit(0)
                        
            print('MSE:',tmpMSE)
            print('Gamma:',trueGamma,'Beta:',trueBeta)
            print('END..')
            #print(np.sum((Infectious-Y)**2))
        else:
            gamma = 0.08
            beta = 0.51
            t_range = np.arange(0,250,1)
            RES = spi.odeint(diff_eqs,INPUT,t_range)
            Infectious = RES[:,1]*people[city]
            Infectious= Infectious.astype(int)
            Y = np.array(Y,dtype='int')
            print(Y)
            print(Infectious[0:11])
            plt.figure()
            plt.plot(t_range,Infectious)
            plt.show()            
        
        
      
            
            #print(INPUT)
            #print(t_range)
            #print(Y)
        
            
        #print(RES[:,1]*people[city])
         
