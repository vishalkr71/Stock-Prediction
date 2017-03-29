# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 11:02:15 2016

@author: vishalkr71
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Reading of Data  
def readdata():  
    start_date="2014-01-01"
    end_date="2014-04-01"
    symbols=['HERO','BULLET']
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    for symbol  in symbols:
        df_temp=pd.read_csv("{}.csv".format(symbol),index_col="Date",parse_dates=True,
                       usecols=['Date','Adj Close'],na_values=['nan'])
        df_temp=df_temp.rename(columns={'Adj Close':symbol})
        df1=df1.join(df_temp,how='inner')
    df1=df1.sort_index()
    print(df1)
    return df1
    
#Plotting of different data
def plotting(dataset):
    ax=dataset.plot(title="Stock Prices",fontsize=10)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    plt.show()
    
#Normalising of different price range
def normalise(dataset):
    return dataset/dataset.ix[0,:]

#Bollinger Bands
def bollingerbands(new_dataset):
    ax=new_dataset['HERO'].plot(title="Hero Bollinger Band", label='HERO')
    rm=new_dataset['HERO'].rolling(center=False,window=20).mean()
    rstd=new_dataset['HERO'].rolling(center=False,window=20).std()
    upperlimit=rm+2*rstd
    lowerlimit=rm-2*rstd
    rm.plot(label='Rolling Mean',ax=ax)
    upperlimit.plot(label='Upper Band',ax=ax)
    lowerlimit.plot(label='Lower Band',ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    ax.legend(loc='upper left')
    plt.show()
    
#Daily Returns of Stocks
def compute_dailyreturns(dataset): 
    df2=dataset.copy()
    df2[1:]=(df2[1:]/df2[:-1].values)-1
    df2.ix[0,:]=0
    return df2
    
#Histogram and Kurtosis
def histandkurt(dailyreturns):
    dailyreturns.hist(bins=20)
    mean=dailyreturns['HERO'].mean()
    print("Mean=",mean)
    std=dailyreturns['HERO'].std()
    print("Standard deviation=",std)
    plt.axvline(mean,color='w',linestyle='dashed',linewidth='2')
    plt.axvline(std,color='r',linestyle='dashed',linewidth='2')
    plt.axvline(-std,color='r',linestyle='dashed',linewidth='2')
    plt.show() 
    #Kurtosis of Stock
    print("Relation of Stocks")
    print(dailyreturns.kurtosis())
    
 #Scatter plot
def scatter(dailyreturns):
    dailyreturns.plot(kind='scatter',x='HERO',y='BULLET')
    beta_hero,alpha_hero=np.polyfit(dailyreturns['BULLET'],
                         dailyreturns['HERO'],1)
    plt.plot(dailyreturns['BULLET'],beta_hero*dailyreturns['BULLET']
             +alpha_hero,'-',color='r')
    plt.show()
    print(dailyreturns.corr(method='pearson'))
    

 #Main Function
if __name__ == "__main__":
   dataset = readdata()
   plotting(dataset)
   new_dataset=normalise(dataset)
   plotting(new_dataset)
   bollingerbands(new_dataset)
   dailyreturns=compute_dailyreturns(dataset)
   plotting(dailyreturns)
   histandkurt(dailyreturns)
   scatter(dailyreturns)
   
   
   
    
    
