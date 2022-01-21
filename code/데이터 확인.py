import numpy as np
import pandas as pd

# 부동산 가격 데이터 확인

# 1. 실거래가 정보
# 데이터 불러오기
data = []

for i in range(2006, 2021):
    data.append(pd.read_csv('data/원본/서울특별시_부동산_실거래가_정보_{}년.csv'.format(i)))

# 컬럼명 입력
cols = ['자치구명', '신고년도', '건물면적', '층정보', '건물주용도', '물건금액', '건축년도']

# 필요없는 컬럼 제거
for i in range(len(data)):
    data[i] = data[i][cols]

# 리스트화 되어있는 데이터프레임들을 하나로 합침
df = pd.DataFrame(columns = cols)
for i in range(len(data)):
    df = pd.concat([df, data[i]], axis=0)

# 인덱스 초기화
df.set_index('자치구명', inplace=True)
df.reset_index(inplace=True)

# 저장하기
df.to_csv('data/서울특별시_부동산_실거래가_정보_2006-2020년.csv')

# 면적당 가격을 구하기 위한 전처리
data = pd.read_csv('data/서울특별시_부동산_실거래가_정보_2006-2020년.csv')
data

data['면적당 가격'] = data['물건금액'] / data['건물면적']
data1 = data.groupby(['자치구명', '신고년도'])['면적당 가격'].mean()
data1

data1.to_csv('data/서울특별시_부동산_면적당_가격_평균_2006-2020년.csv')

# 2. 매매지수 정보(간단한 전처리)
data = pd.read_excel('data/유형별_매매가격지수_2005.01-2021.09.xlsx', header=1)

del data['항목']
del data['단위']

data.to_csv('data/유형별_매매가격지수_2005.01-2021.09.csv')

# 3. 연령별 인구(간단한 전처리)
data = pd.read_csv('data/원본/시군구_성_연령(5세)별_주민등록연앙인구_2005-2020.csv')

del data['단위']
del data['항목']
del data['Unnamed: 21']

data['성별'] = data['성별'][data['성별'] != '계']
data.dropna(axis=0, inplace=True)

data.to_csv('data/시군구_성_연령(5세)별_인구_2005-2020.csv')