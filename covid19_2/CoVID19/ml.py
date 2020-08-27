import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
import datetime as dt
import os
from sklearn.linear_model import Ridge
def img1(date1,text,beta1,kos):
    if beta1=="베타에 값없다":
        print("베타에 값없음")
        return
    os.remove('static/images/jin.png')

    lr=LinearRegression()
    pr=LinearRegression()

    X_fit=np.arange(250,800,10)[:,np.newaxis]
 
    import datetime as dt
    data=pd.read_excel('data/covid2.xlsx')
    df=pd.DataFrame(data)
    X=df['new_cases'][:158][:,np.newaxis]
    y=df['date'][:158].astype("int64")
    y=y/86400
    y=y-y[0]
    y=y/1000000000
    quadratic=PolynomialFeatures(degree=6)
    X_quad=quadratic.fit_transform(X)
    X_fit=np.arange(0,500,1)[:,np.newaxis]
    pr.fit(X_quad,y)
    y_quad_fit =pr.predict(quadratic.fit_transform(X_fit))
    y_quad_pred =pr.predict(X_quad)

    mse_quad=mean_squared_error(y,y_quad_pred)
    r2_quad=r2_score(y,y_quad_pred)

    data2=pd.read_csv('data/'+text+'.csv',engine='python',parse_dates=["date"],thousands=',')
    
    if kos==1:
        kospy=pd.read_csv('data/kospy.csv',engine='python')
    elif kos==2:
        kospy=pd.read_csv('data/kosdaq.csv',engine='python')
    kospyDf=pd.DataFrame(kospy)
    kospynum=kospyDf.iloc[:,5][:158]
    kospynum=kospynum.map(lambda x: float(x[:-1])*beta1)
    df2=pd.DataFrame(data2)
    result=df2.iloc[:,2][:-1]
    result[:-1],data['date'][:158],data['new_cases'][:158]
    a=pd.concat([y,result[:-1],data['new_cases'][:158],kospynum],axis=1)
    x_train=a[['date','new_cases','�벑�씫瑜�']]
    y_train=a.iloc[:,1]
    from sklearn.linear_model import ElasticNet
    mlr=ElasticNet(alpha=0.5,l1_ratio=0.5)
    mlr.fit(x_train, y_train) 
    y_quad_pred=mlr.predict(x_train)
    print(x_train)
    ridge=Ridge().fit(pd.DataFrame(y),pd.DataFrame(kospynum))
    y_fit1=ridge.predict(np.arange(0,500,1)[:,np.newaxis])


    # inputdate=300
    # X_fit=np.arange(inputdate,inputdate+1,1)[:,np.newaxis]
    # y_quad_fit =pr.predict(quadratic.fit_transform(X_fit))
    # my_predict = mlr.predict([[inputdate,y_quad_fit]])
    # my_predict
    import matplotlib.pyplot as plt
    X_fit=np.arange(0,500,1)[:,np.newaxis]
    plt.scatter(y, y_train, alpha=0.4)
    plt.plot(x_train['date'],y_quad_pred,label='quadratic fit',color='orange')
    plt.xlabel("covid after Date(2020-01-02)")
    plt.ylabel("Predicted Closing price")
    plt.title("MULTIPLE LINEAR REGRESSION predict closing price")
    inputdate=date1
    X_fit=np.arange(inputdate,inputdate+1,1)[:,np.newaxis]
    test=np.arange(250,250+250,1)[:,np.newaxis]
    y_quad_fit =pr.predict(quadratic.fit_transform(X_fit))
    y_quad_fit1=ridge.predict(X_fit)
    

    

    my_predict = mlr.predict([[inputdate,y_quad_fit,y_quad_fit1]])
    percent=(my_predict/y_train.iloc[-1])*100
    plt.plot(inputdate,my_predict,color='red', marker='o')
    plt.savefig('static/images/jin.png')
    plt.cla()
    print(inputdate,"일 뒤에 %.2f 퍼센트증가"%round(percent[0]-100,2))
    return round(percent[0]-100,2)

