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

def img(date1):
    X=np.array([258.0,270.0,294.0,320.0,342.0,369.0,396.0,446.0,480.0,586.0])[:,np.newaxis]
    y=np.array([236.4,234.4,252.8,298.6,314.2,342.2,360.8,368.0,391.2,390.8])

    lr=LinearRegression()
    pr=LinearRegression()

    quadratic=PolynomialFeatures(degree=2)
    X_quad=quadratic.fit_transform(X)

    lr.fit(X,y)
    X_fit=np.arange(250,800,10)[:,np.newaxis]
    y_lin_fit=lr.predict(X_fit)

    pr.fit(X_quad,y)
    y_quad_fit =pr.predict(quadratic.fit_transform(X_fit))

    y_lin_pred=lr.predict(X)
    y_quad_pred =pr.predict(X_quad)

    mse_lin=mean_squared_error(y,y_lin_pred)
    mse_quad=mean_squared_error(y,y_quad_pred)

    r2_lin=r2_score(y,y_lin_pred)
    r2_quad=r2_score(y,y_quad_pred)


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

    data2=pd.read_csv('data/진바이오텍.csv',engine='python',parse_dates=["date"],thousands=',')
    df2=pd.DataFrame(data2)
    result=df2['醫낃��'][:-1]
    result[:-1],data['date'][:158],data['new_cases'][:158]
    a=pd.concat([y,result[:-1],data['new_cases'][:158]],axis=1)
    x_train=a[['date','new_cases']]
    y_train=a['醫낃��']
    from sklearn.linear_model import ElasticNet
    mlr=ElasticNet(alpha=0.5,l1_ratio=0.5)
    mlr.fit(x_train, y_train) 
    y_quad_pred =mlr.predict(x_train)
    # inputdate=300
    # X_fit=np.arange(inputdate,inputdate+1,1)[:,np.newaxis]
    # y_quad_fit =pr.predict(quadratic.fit_transform(X_fit))
    # my_predict = mlr.predict([[inputdate,y_quad_fit]])
    # my_predict
    import matplotlib.pyplot as plt
    X_fit=np.arange(0,500,1)[:,np.newaxis]
    plt.scatter(y, y_train, alpha=0.4)
    plt.plot(x_train['date'],y_quad_pred,label='quadratic fit',color='orange')
    plt.xlabel("Actual Rent")
    plt.ylabel("Predicted Rent")
    plt.title("MULTIPLE LINEAR REGRESSION")
    inputdate=400
    X_fit=np.arange(inputdate,inputdate+1,1)[:,np.newaxis]
    test=np.arange(250,250+250,1)[:,np.newaxis]
    y_quad_fit =pr.predict(quadratic.fit_transform(X_fit))
    my_predict = mlr.predict([[inputdate,y_quad_fit]])
    percent=(my_predict/y_train.iloc[-1])*100
    plt.plot(inputdate,my_predict,color='red', marker='o')
    plt.savefig('jin.png')
    print(inputdate,"일 뒤에 %.2f 퍼센트증가"%round(percent[0]-100,2))
    return round(percent[0]-100,2)