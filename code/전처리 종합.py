from functools import reduce
import datetime
import pandas as pd
import numpy as np

########## 유동인구 전처리 ##########
floating_pop = pd.read_csv("data/유동인구수.csv")

### 첫번째 행을 column 이름으로 지정
floating_pop.rename(columns=floating_pop.iloc[0], inplace=True)

floating_pop.drop(floating_pop.index[0], inplace=True)
floating_pop.head()

### 필요없는 column 삭제
floating_pop.drop(["단위"], axis=1, inplace=True)

### '순이동', '총전입', '총전출'만 가져오기
floating_pop = floating_pop[floating_pop['항목'].isin(['순이동',
                                                     '총전입',
                                                     '총전출'])]
floating_pop

### 날짜 column 수정(2005. 01 월 -> 2005년 1월)
floating_pop.columns = floating_pop.columns.str.replace(" ", "")
floating_pop.columns = floating_pop.columns.str.replace(".", "년 ")
floating_pop.columns

floating_pop_columns = ['구별', '항목']

for col in floating_pop.columns[2:]:
    if col[6] == '0':
        col = col[:6] + col[7:]
    floating_pop_columns.append(col)

floating_pop.columns = floating_pop_columns
floating_pop.columns

### 서울 전체 데이터와 구별 데이터 구분하기
floating_pop_seoul = floating_pop[floating_pop['구별'] == '서울특별시']
floating_pop_gu = floating_pop[floating_pop['구별'] != '서울특별시']
floating_pop_gu.reset_index(drop=True, inplace=True)

### to csv
floating_pop_gu.to_csv("data/floating_pop_gu.csv",
                       index=False, encoding="CP949")


########## 매매가격지수 전처리 ##########
price = pd.read_csv("data/유형별_매매가격지수_2005.01-2021.09.csv",
                    encoding="utf-8")
price.drop('Unnamed: 0', axis=1, inplace=True)

### 필요없는 행 삭제

### '~~권' 행 삭제
index1 = price[price['지역별'].str.contains("권")].index

price.drop(index1, inplace=True)


### column 수정 및 이름 변경

### 구 이름 뒤에 '구' 붙이기

price["지역별"] = price["지역별"] + '구'
price

### 날짜 column 수정(2005. 01 월 -> 2005년 1월)
price.columns = price.columns.str.replace(" ", "")
price.columns = price.columns.str.replace(".", "년 ")
price.columns

price_columns = ['항목', '구별']

for col in price.columns[2:]:
    if col[6] == '0':
        col = col[:6] + col[7:]
    price_columns.append(col)

price.columns = price_columns

### to csv
price.to_csv("data/trade_price.csv", index=False, encoding="CP949")


########## 편의시설, 혐오시설 전처리 ##########
## 전처리 함수

def pre_processing(file_name, column_name):
    ### 파일 불러오기
    data = pd.read_csv("data/" + file_name + ".csv")
    
    ### 항목 column 추가
    data.insert(1, "항목", column_name)
    
    ### 첫 행이 컬럼명일 경우 첫 행 삭제
    if data.iloc[0, 0] != "강남구":
        data.drop(index=0, axis=0, inplace=True)
    
    ### column 이름 변경
    # 공원
    if data.columns[0] == "행정구역(시군구)별":
        data.rename(columns = {'행정구역(시군구)별':'구별'}, inplace=True)
        
    # 혐오시설
    elif data.columns[0] == "행정구역(시군구별)":
        data.rename(columns = {'행정구역(시군구별)':'구별'}, inplace=True)
        
    # 학생 수, 대학교 수
    elif data.columns[0] == "행정구역별":
        data.rename(columns = {'행정구역별':'구별'}, inplace=True)
            
    # 인구밀도
    elif file_name == "서울시 구별 인구밀도 월별 통계 2007~2020":
        pass
    
    # 학원, 의료기관, 마트, 박물관
    else:
        data.rename(columns = {'Unnamed: 0':'구별'}, inplace=True)
    
    ### 날짜, 구별로 그룹화
    data = data.groupby(['구별', '항목']).sum()
    data_T = data.T.stack(level=0)

    ### to_csv
    data_T.to_csv("data/" + file_name + "_전처리.csv", index=False)

pre_processing("서울시 공원 (1인당 공원면적) 월별 통계 2005_2020", "1인당공원면적")
pre_processing("서울시 구별 화장시설 월별 통계 2005_2020", "화장시설(개)")
pre_processing("서울시 구별 구치소 월별 통계 2005_2020", "구치소(개)")
pre_processing("서울시 교원 1인당 학생수 월별 통계 2007_2020", "교원1인당 학생(명)")
pre_processing("서울시 대학교 수 월별 통계 2007_2021", "대학교(개)")
pre_processing("서울시 구별 인구 천명당 사설학원 수", "학원(개)")
pre_processing("서울시 구별 인구 천명당 의료기관 수 월별 2005_2020", "의료기관(개)")
pre_processing("서울시 대형마트 및 백화점  월별 통계 2005_2020", "대형마트 및 백화점(개)")
pre_processing("서울시 박물관 월별 통계 2005_2020", "박물관(개)")
pre_processing("서울시 구별 인구밀도 월별 통계 2007~2020", "인구밀도")


########## 아파트 거래량 및 미분양 물량 전처리 ##########
mibunyang = pd.read_csv("data/아파트 거래량 및 미분양 물량.csv", encoding="CP949")
mibunyang

### 필요없는 행 삭제
mibunyang.drop([50, 51, 52], inplace=True)

### NaN값 0으로 채우기
mibunyang = mibunyang.fillna(0)

### '행졍구역(구별)' -> '구별'
mibunyang.rename(columns = {'행정구역(구별)':'구별'}, inplace=True)

### 구별 column 공백 없애기
mibunyang["구별"] = mibunyang["구별"].str.strip()

### 구별, 항목별 정렬
mibunyang.sort_values(["구별", "항목"], inplace=True)
mibunyang.reset_index(drop=True, inplace=True)

### 날짜, 항목별 그룹화
mibunyang = mibunyang.groupby(['구별', '항목']).sum()
mibunyang_T = mibunyang.T.stack(level=0)

### to_csv
mibunyang_T.to_csv("data/아파트 거래량 및 미분양 물량_전처리.csv")


########## 인구밀도 전처리 ##########
density = pd.read_csv("data/서울시 구별 인구밀도 월별 통계 2007~2020_전처리.csv")

### 천단위 콤마 빼고 float 형식으로 바꾸기
density["인구밀도"] = density["인구밀도"].str.replace(',', '').astype('float')
density["구별"] = density["구별"].str.strip()
density.to_csv("data/서울시 구별 인구밀도 월별 통계 2007~2020_전처리.csv", index=False)


########## 데이터 종합 ##########
### 날짜 column을 기준으로 하기 위해 날짜 형식 맞춰주기
def to_datetime(*filenames):
    for file in filenames:
        data = pd.read_csv("data/" + file + ".csv", encoding="utf-8")
        data["Unnamed: 0"] = pd.to_datetime(data["Unnamed: 0"], format="%Y년 %m월")
        data["Unnamed: 0"] = data["Unnamed: 0"].dt.strftime("%Y/%m")

        data.to_csv("data/" + file + "_final.csv", index=False)

to_datetime('floating_pop_gu',
            'trade_price',
            '아파트 거래량 및 미분양 물량_전처리',
            '서울시 공원 (1인당 공원면적) 월별 통계 2005_2020_전처리',
            '서울시 교원 1인당 학생수 월별 통계 2007_2020_전처리',
            '서울시 구별 인구 천명당 사설학원 수_전처리',
            '서울시 대학교 수 월별 통계 2007_2021_전처리',
            '서울시 구별 인구 천명당 의료기관 수 월별 2005_2020_전처리',
            '서울시 대형마트 및 백화점  월별 통계 2005_2020_전처리',
            '서울시 박물관 월별 통계 2005_2020_전처리',
            '서울시 구별 구치소 월별 통계 2005_2020_전처리',
            '서울시 구별 화장시설 월별 통계 2005_2020_전처리',
            '서울시 구별 인구밀도 월별 통계 2007~2020_전처리')