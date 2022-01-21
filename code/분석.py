import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

from matplotlib import rc
rc('font',family='AppleGothic')

import matplotlib as mpl
mpl.rcParams['axes.unicode_minus'] = False
from sklearn import linear_model
from scipy import stats
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.optimize import curve_fit


data=pd.read_csv('/Users/hanjaemin/Downloads/data_merge_real_final.csv')
data.head()

#총전입, 총전출 열 삭제

del data['총전입']
del data['총전출']

#독립변수 설정
su=['순이동', '미분양 물량', '아파트 매매량', '1인당공원면적',
    '교원1인당 학생(명)', '학원(개)', '대학교(개)',
    '의료기관(개)', '대형마트 및 백화점(개)', '박물관(개)',
    '구치소(개)', '화장시설(개)', '인구밀도']

#아파트와 독립변수 간 상관관계 파악을 위한 그래프 그리기

def booli(*gu):
    global gus
    gus = []
    for i in gu:
        i = data.loc[data['구별'] == i]
        gus.append(i)
        for j in su:
            sns.pairplot(i, vars=['아파트', j], height=3, kind="reg")
        
booli('강남구', '강동구', '강북구', '강서구', '관악구', '광진구',
      '구로구', '금천구', '노원구', '도봉구',
      '동대문구', '동작구', '마포구', '서대문구', '서초구',
      '성동구', '성북구', '송파구', '양천구', '영등포구',
      '용산구', '은평구', '종로구', '중구', '중랑구')

#데이터 이름 설정

강남구 = gus[0]
강동구 = gus[1]
강북구 = gus[2]
강서구 = gus[3]
관악구 = gus[4]
광진구 = gus[5]
구로구 = gus[6]
금천구 = gus[7]
노원구 = gus[8]
도봉구 = gus[9]
동대문구 = gus[10]
동작구 = gus[11]
마포구 = gus[12]
서대문구 = gus[13]
서초구 = gus[14]
성동구 = gus[15]
성북구 = gus[16]
송파구 = gus[17]
양천구 = gus[18]
영등포구 = gus[19]
용산구 = gus[20]
은평구 = gus[21]
종로구 = gus[22]
중구 = gus[23]
중랑구 = gus[24]

# pairplot 을 통해 각 자치구의 집값과 다른 변수들의 상관관계 확인
# for 반복문으로 한번에 상관관계를 확인하려 했으나
# pairplot 을 반복해서 돌릴경우 겹치기도 하고
# 시간을 너무 많이 잡아먹었기 때문에 각 자치구 마다 하나씩 처리해줄 필요가 있었음
# for i in range(len(gus)):
#     sns.pairplot(gus[i], vars=['아파트', '순이동', '미분양 물량', '아파트 매매량',
#                                '1인당공원면적', '교원1인당 학생(명)', '학원(개)',
#                                '대학교(개)', '의료기관(개)', '대형마트 및 백화점(개)',
#                                '박물관(개)', '구치소(개)', '화장시설(개)', '인구밀도'],
#                  height=3, kind="reg").set(title='강남구')
# 함수의 첫부분의 자치구 부분을 순차적으로 바꾸어가며 데이터를 수집
sns.pairplot(강남구, vars=['아파트', '순이동', '미분양 물량', '아파트 매매량', '1인당공원면적',
                        '교원1인당 학생(명)', '학원(개)', '대학교(개)', '의료기관(개)',
                        '대형마트 및 백화점(개)', '박물관(개)', '구치소(개)',
                        '화장시설(개)', '인구밀도'],
             height=3, kind="reg").set(title='강남구')

for i in range(len(gus)):
    print(gus[i].iloc[0,1], '\n')
    
    print("미분양 물량와 아파트의 상관계수 :",
          np.corrcoef(gus[i]["미분양 물량"],
                      gus[i]['아파트'])[1,0].round(2))
    
    print("교원1인당 학생(명)과 아파트의 상관계수 :",
          np.corrcoef(gus[i]["교원1인당 학생(명)"],
                      gus[i]['아파트'])[1,0].round(2))
    
    print("학원(개)와 아파트의 상관계수 :",
          np.corrcoef(gus[i]["학원(개)"],
                      gus[i]['아파트'])[1,0].round(2))
    
    print("의료기관(개)와 아파트의 상관계수 :",
          np.corrcoef(gus[i]["의료기관(개)"],
                      gus[i]['아파트'])[1,0].round(2))
    
    print("대형마트 및 백화점(개)과 아파트의 상관계수 :",
          np.corrcoef(gus[i]["대형마트 및 백화점(개)"],
                      gus[i]['아파트'])[1,0].round(2))
    
    print("인구밀도와 아파트의 상관계수 :",
          np.corrcoef(gus[i]["인구밀도"],
                      gus[i]['아파트'])[1,0].round(2))
    
    print("--"*20, '\n')


# 상관관계가 무의미한 변수 제거
for i in range(len(gus)):
    
    del gus[i]['순이동']
    del gus[i]['아파트 매매량']
    del gus[i]['1인당공원면적']
    del gus[i]['대학교(개)']
    del gus[i]['박물관(개)']
    del gus[i]['구치소(개)']
    del gus[i]['화장시설(개)']

# 자치구별 heatmap 역시 위의 pairplot 과 마찬가지로 한번에 그릴 수 없었기 때문에
# 하나씩 확인해줄 필요가 있었음
# gus 를 0부터 24까지 하나씩 불러보면서 heatmap 을 확인
sns.heatmap(gus[0].corr(), annot=True, cmap='YlGnBu')
# for i in range(len(gus)):
#     sns.heatmap(gus[i].corr(), annot=True, cmap='YlGnBu')

# 선별요인을 사용하여 집값과의 상관관계 시각화
# 이 역시 한번에 확인할 수 없었기 때문에 하나씩 확인
f, ax = plt.subplots(2, 3, figsize=(20, 10))

sns.regplot(data=강남구, x='아파트', y='미분양 물량', ax=ax[0, 0], color='r')
sns.regplot(data=강남구, x='아파트', y='교원1인당 학생(명)', ax=ax[1, 0])
sns.regplot(data=강남구, x='아파트', y='학원(개)', ax=ax[0, 1], color='y')
sns.regplot(data=강남구, x='아파트', y='의료기관(개)', ax=ax[1, 1], color='b')
sns.regplot(data=강남구, x='아파트', y='대형마트 및 백화점(개)', ax=ax[0, 2], color='g')
sns.regplot(data=강남구, x='아파트', y='인구밀도', ax=ax[1, 2])
# for i in range(len(gus)):
#     sns.regplot(data=gus[i],
#                 x='아파트', y='미분양 물량', ax=ax[0, 0], color='r')
#     sns.regplot(data=gus[i],
#                 x='아파트', y='교원1인당 학생(명)', ax=ax[1, 0])
#     sns.regplot(data=gus[i],
#                 x='아파트', y='학원(개)', ax=ax[0, 1], color='y')
#     sns.regplot(data=gus[i],
#                 x='아파트', y='의료기관(개)', ax=ax[1, 1], color='b')
#     sns.regplot(data=gus[i],
#                 x='아파트', y='대형마트 및 백화점(개)', ax=ax[0, 2], color='g')
#     sns.regplot(data=gus[i],
#                 x='아파트', y='인구밀도', ax=ax[1, 2])

# 필요없는 컬럼 삭제 및 컬럼명 통일
for i in range(len(gus)):
    del gus[i]['날짜']
    del gus[i]['구별']
    gus[i].columns=["아파트", "미분양물량", "교원일인당학생", "학원개",
                    '의료기관개', '대형마트및백화점개', '인구밀도']

# 회귀분석을 통해서 종속변수들의 영향력을 확인
cols = list(data['구별'].unique())
for i in range(len(gus)):
    model = smf.ols(formula='''
                    아파트 ~ 미분양물량 + 교원일인당학생 + 학원개 +
                    의료기관개 + 대형마트및백화점개 + 인구밀도'
                    ''', data = gus[i])
    result = model.fit()
    print(cols[i])
    print(result.summary())
    print('\n'*5)

# 강남구 아파트 지수에 대형마트 및 백화점 개수를 제외한 나머지 변수들은 유의미한 영향을 준다.

# 강남구 아파트 지수에 유의한 영향을 주는 변수들로 다시 회귀
model = smf.ols(formula = '''
                아파트 ~ 미분양물량 + 교원일인당학생 + 학원개 +
                의료기관개 +인구밀도
                ''', data = gus[0])
result = model.fit()
result.summary() 

for i in range(len(gus)):
    X = gus[i][["미분양물량","교원일인당학생","학원개",'의료기관개','인구밀도']]
    X = sm.add_constant(X) # adding a constant

    olsmod = sm.OLS(gus[i]['아파트'], X).fit()
    print(olsmod.summary())

#분석 결과 Adj. R-squared가 0.875로 다섯가지 변수는 강남구 아파트지수에 영향을 미치며 약 88%의 설명력을 가진다.


# 구별 상관 계수 뽑기
X_cols = ["미분양물량", "교원일인당학생", "학원개", '의료기관개', '인구밀도']

for i in range(len(gus)):
    X = gus[i][X_cols]
    y = gus[i][['아파트']]
    
    regr = linear_model.LinearRegression()
    model = regr.fit(X, y)

    print(cols[i], '의 상관계수')
    print('Intercept :', model.intercept_)
    
    print('Coefficients :\n', X_cols[0], ':', model.coef_[0][0],
          ',', X_cols[1], ':', model.coef_[0][1],
          ',', X_cols[2], ':', model.coef_[0][2],
          ',', X_cols[3], ':', model.coef_[0][3],
          ',', X_cols[4], ':', model.coef_[0][4])

# 위에서 구한 상관관계를 시각화(한번에 다 볼 수 없었으므로 일단 강남구만)
# 다른 구들을 볼땐 gus 의 index 를 변화시켜서 확인
k = ['학원개', '미분양물량', '교원일인당학생']

def x_func(x, a, b, c):
    y = (a/(x - b))*abs(x - c)*(80 - (1/x))
    return y

f,axes = plt.subplots(1, 3, figsize=(15, 15))

for i in range(len(k)):
    parameters, covariance = curve_fit(x_func, gus[0].iloc[:, i], gus[0]['아파트'], maxfev=100000)
    fit_a = parameters[0]
    fit_b = parameters[1]
    fit_c = parameters[2]

    print(fit_a, fit_b, fit_c)
    fit_x = x_func(gus[0].iloc[:, i], fit_a, fit_b, fit_c)
    
    ax[i%3].plot(gus[0].iloc[:, i], gus[0]['아파트'], 'o', label='data')
    ax[i%3].plot(gus[0].iloc[:, i], fit_x, label='fit')
    ax[i%3].set_title('강남구')