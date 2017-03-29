# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 21:03:33 2017

@author: vishalkr71
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm

#Reading of Data  
def readdata():  
    start_date="2016-01-01"
    end_date="2016-01-20"
    symbols=['HERO']
    dates=pd.date_range(start_date,end_date)
    df1=pd.DataFrame(index=dates)
    for symbol  in symbols:
        df1=pd.read_csv("{}.csv".format(symbol),index_col="Date",parse_dates=True,
                       usecols=['Date','Open','Close','Adj Close',],na_values=['nan'])
    df1=df1.sort_index()
    print(df1)
    return df1

#Division of stock in training and testing data
def division(dataset):
    opening=dataset.ix[:,1]
    closing=dataset.ix[:,2]
    openingPriceTrain, openingPriceTest, closingPriceTrain, closingPriceTest =\
    train_test_split(opening, closing, test_size=0.25, random_state=42)
    openingPriceTrain = np.reshape(openingPriceTrain, (openingPriceTrain.size, 1))
    closingPriceTrain = np.reshape(closingPriceTrain, (closingPriceTrain.size, 1))
    openingPriceTest = np.reshape(openingPriceTest, (openingPriceTest.size, 1))
    closingPriceTest = np.reshape(closingPriceTest, (closingPriceTest.size, 1))

    sampledData = {"openingPriceTrain":openingPriceTrain, "closingPriceTrain":closingPriceTrain,
                   "openingPriceTest":openingPriceTest, "closingPriceTest":closingPriceTest}
    return sampledData

#Random Forest Regression    
def predictRandomForestReg(data, priceToPredict):
    openingPriceTrain, openingPriceTest, closingPriceTrain, closingPriceTest = \
        data["openingPriceTrain"], data["openingPriceTest"], data["closingPriceTrain"], data["closingPriceTest"]
    clf = RandomForestRegressor(n_estimators=10)
    clf = clf.fit(openingPriceTrain, closingPriceTrain)
    print(clf.predict(priceToPredict))
    score=clf.score(openingPriceTest, closingPriceTest)
    print("Accuracy:")
    print(score)
    calculated=clf.predict(openingPriceTest)
    ax = plt.subplots()
    ax.scatter(openingPriceTrain, closingPriceTrain)
    ax.set_ylabel('Predicted SVM')
    ax.scatter(closingPriceTest,calculated )
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()
    
#Support Vector Regression    
def predict(data, priceToPredict):
    openingPriceTrain, openingPriceTest, closingPriceTrain, closingPriceTest = \
        data["openingPriceTrain"], data["openingPriceTest"], data["closingPriceTrain"], data["closingPriceTest"]
    openingPriceTrain.reshape(-1,1)
    closingPriceTrain.reshape(-1,1)
    clf = svm.LinearSVR()
    clf.fit(openingPriceTrain, closingPriceTrain)
    print(clf.predict(priceToPredict))
    score = clf.score(openingPriceTest, closingPriceTest)
    print("Accuracy:")
    print(score)
    
#Main Function
if __name__ == "__main__":
   dataset = readdata()
   sampledData= division(dataset)
   priceToPredict=3000
   print("Random Forest Regressor Prediction:")
   predictRandomForestReg(sampledData, priceToPredict)
   print("SVM Prediction:")
   predict(sampledData, priceToPredict)