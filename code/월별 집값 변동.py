import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
font_name = fm.FontProperties(fname = "C:/Windows/Fonts/malgun.ttf").get_name()
plt.rc("font", family = font_name)
import seaborn as sns

import warnings
warnings.filterwarnings(action = "ignore", category = FutureWarning)

from scipy.optimize import curve_fit


# 데이터 불러오기
data = pd.read_csv('data/서울특별시_부동산_면적당_가격_평균_2006-2020년.csv')


# 사용한 데이터는 2007년 ~ 2020년 이기때문에 2006년 데이터는 삭제
data = data[data['신고년도'] != 2006]
data = data.set_index('자치구명').reset_index()

# 각 자치구명들의 시간 변화에 따른 면적당 집값 변화량의 시각화
f, ax = plt.subplots(5, 5, figsize=(20, 15))
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.4)

cols = list(data['자치구명'].unique())

for i in range(len(cols)):
    sns.lineplot('신고년도', '면적당 가격',
                data=data.loc[data['자치구명'] == cols[i]],
                ax = ax[i//5, i%5])
    ax[i//5, i%5].set_title(cols[i])


# 신고년도와 면적당 집값의 상관관계의 시각화
def x_func(x, a, b, c):
    y = a*np.power(x-2006, b) + c
    return y

cols = list(data['자치구명'].unique())
colors = ['firebrick', 'darksalmon', 'sienna', 'sandybrown', 'bisque',
         'tan', 'gold', 'darkkhaki', 'olivedrab', 'chartreuse',
          'darkgreen', 'lightseagreen', 'paleturquoise', 'deepskyblue', 'aliceblue',
          'slategray', 'royalblue', 'navy', 'mediumpurple', 'plum',
         'm', 'mediumvioletred', 'lightpink', 'khaki', 'yellow']

plt.figure(figsize=(15, 12))
for i in range(len(cols)):
    parameters, covariance = curve_fit(x_func,
                                       data[data['자치구명'] == cols[i]]['신고년도'],
                                      data[data['자치구명'] == cols[i]]['면적당 가격'])
    fit_a = parameters[0]
    fit_b = parameters[1]
    fit_c = parameters[2]
    
    fit_x = x_func(data[data['자치구명'] == cols[i]]['신고년도'],
                  fit_a, fit_b, fit_c)
    
    plt.plot(data[data['자치구명'] == cols[i]]['신고년도'],
            data[data['자치구명'] == cols[i]]['면적당 가격'],
             'o', color=colors[i])
    plt.plot(data[data['자치구명'] == cols[i]]['신고년도'],
            fit_x, '-', label=cols[i], color=colors[i])

plt.title('신고년도와 면적당 가격의 상관관계')
plt.legend(shadow=True, fancybox=True, loc='best')