import matplotlib as plt
import numpy as np
import pandas as pd
import glob
import  matplotlib as plt


def pecentages(filename):
     df = pd.read_csv( filename ,  thousands = ',')
     df.drop([159] , inplace = True)
     df.loc[:,'종가':] = df.loc[:,'종가':].astype('int')
     result =[]
     for i in range(len(df)-2):
          result.append((df['종가'][i+1] - df['종가'][i])/df['종가'][i] *100)
     result.insert(0,0)
     result.insert(158,0)
     result =np.array(result).round(2)

     s1 = pd.Series(result)
     df2 = pd.concat([df , s1] , axis = 1)


     df2.columns  = ['index' , 'date' , '종가' , '전일비' , '거래량' , '상승률']

     df2.to_csv('C:/project/modify/수정_' +filename,encoding='utf-8-sig')

def Beta(filename , beta):
     df1 = pd.read_csv(filename)
     df2= pd.read_csv('C:/project/data/kospi.csv')
     df3 = pd.read_csv('C:/project/data/kosdaq2.csv')
     kospi = df2['등락률2']
     kospi = np.array(kospi)
     kospi = kospi[:158]
     kosdaq = df3['등락률2']
     kosdaq = np.array(kosdaq)
     kosdaq = kosdaq[:158]
     stock = df1['상승률']
     stock = np.array(stock)
     stock = stock[:158]
     if 'kospi' in filename:
          cov = np.cov(kospi, stock)
          Beta = cov[0][1] / cov[0][0]
          filename = filename.replace('C:/project/modify\\수정_' , '')
          filename = filename.replace('kospi', '')
          filename = filename.replace('.csv', '')
          beta[filename]  = Beta.round(2)
     else:
          cov = np.cov(kosdaq, stock)
          Beta = cov[0][1] / cov[0][0]
          filename = filename.replace('C:/project/modify\\수정_', '')
          filename = filename.replace('kosdaq', '')
          filename = filename.replace('.csv', '')
          beta[filename] = Beta.round(2)

def main():
     beta = {}
     df1 = pd.read_csv('C:/project/data/kospy.csv')
     df1['등락률'] = df1.등락률.apply(lambda x: x.replace('%', ''))
     df1['등락률2'] = pd.to_numeric(df1['등락률'])
     df1.to_csv('C:/project/data/kospi.csv',encoding='utf-8-sig')
     df2 = pd.read_csv('C:/project/data/kosdaq.csv')
     df2['등락률'] = df2.등락률.apply(lambda x: x.replace('%', ''))
     df2['등락률2'] = pd.to_numeric(df2['등락률'])
     df2.to_csv('C:/project/data/kosdaq2.csv', encoding='utf-8-sig')
     for files in glob.glob("*.csv"):
          pecentages(files)
     for files in glob.glob('C:/project/modify/*.csv'):
          Beta(files,beta)
     print(beta)



main()



