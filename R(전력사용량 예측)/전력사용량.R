## 데이터 불러오기
train_df = read.csv('C:/k_digital/data/train.csv')
building_info = read.csv('C:/k_digital/data/building_info.csv')
test_df = read.csv('C:/k_digital/data/test.csv')

## 데이터 구조 확인
str(train_df)
str(building_info)
str(test_df)

## head
head(train_df)
head(building_info)
head(test_df)

## 사본만들기
train <- train_df
build <- building_info
test <- test_df

## 컬럼확인
names(train_df)
names(test_df)
names(building_info)
### test에는 일조, 일사, 전력소비량이 없다

## 컬럼이름 영어로 바꾸기
library(dplyr)
train <- rename(train_df, 
                   building_number = `건물번호`, 
                   date_time = `일시`, 
                   temperature = "기온.C.", 
                   rainfall = "강수량.mm.", 
                   windspeed = `풍속.m.s.`, 
                   humidity = `습도...`, 
                   sunshine = `일조.hr.`, 
                   solar_radiation = `일사.MJ.m2.`, 
                   power_consumption = `전력소비량.kWh.`)

test <- rename(test_df,
                 building_number = `건물번호`, 
                 date_time = `일시`, 
                 temperature = "기온.C.", 
                 rainfall = "강수량.mm.", 
                 windspeed = `풍속.m.s.`, 
                 humidity = `습도...`)

building <- rename(building_info,
  building_number = '건물번호',
  building_type = '건물유형',
  total_area = '연면적.m2.',
  cooling_area = '냉방면적.m2.',
  solar_power_capacity = '태양광용량.kW.',
  ess_capacity = 'ESS저장용량.kWh.',
  pcs_capacity = 'PCS용량.kW.'
)

## 건물유형들 한글->영어
building$building_type <- ifelse(building[, 'building_type'] == '건물기타', 'Other Buildings',
                   ifelse(building[, 'building_type'] == '공공', 'Public',
                          ifelse(building[, 'building_type'] == '대학교', 'University',
                                 ifelse(building[, 'building_type'] == '데이터센터', 'Data Center',
                                        ifelse(building[, 'building_type'] == '백화점및아울렛', 'Department Store and Outlet',
                                               ifelse(building[, 'building_type'] == '병원', 'Hospital',
                                                      ifelse(building[, 'building_type'] == '상용', 'Commercial',
                                                             ifelse(building[, 'building_type'] == '아파트', 'Apartment',
                                                                    ifelse(building[, 'building_type'] == '연구소', 'Research Institute',
                                                                           ifelse(building[, 'building_type'] == '지식산업센터', 'Knowledge Industry Center',
                                                                                  ifelse(building[, 'building_type'] == '할인마트', 'Discount Mart',
                                                                                         ifelse(building[, 'building_type'] == '호텔및리조트', 'Hotel and Resort',
                                                                                                building[, 'building_type']))))))))))))


## 날짜 데이터처리
train$date <- as.Date(train$date_time, '%Y%m%d')
train$month <- as.numeric(substr(as.character(train$date_time), 5, 6))
train$day <- as.numeric(substr(as.character(train$date_time), 7, 8))
train$hour <- as.numeric(substr(as.character(train$date_time), 10, 11))
train$weekday <- weekdays(train$date)
train <- train[,-c(1,3)]

## 건물 결측치 변경
building$solar_power_capacity <- ifelse(building$solar_power_capacity=='-', 0, building$solar_power_capacity)
building$ess_capacity <- ifelse(building$ess_capacity=='-', 0, building$ess_capacity)
building$pcs_capacity <- ifelse(building$pcs_capacity=='-', 0, building$pcs_capacity)
building$solar <- ifelse(building$solar_power_capacity==0,0,1)
building$ess <- ifelse(building$ess_capacity==0,0,1)
building$pcs <- ifelse(building$pcs_capacity==0,0,1)

## 날짜결측치 변경
train$sunshine <- ifelse(is.na(train$sunshine), 0, train$sunshine)
train$solar_radiation <- ifelse(is.na(train$solar_radiation), 0, train$solar_radiation)
train$rainfall <- ifelse(is.na(train$rainfall), 0, train$rainfall)

### windspeed와 humidity 결측치 변경
library(zoo)
train$windspeed <- na.approx(train$windspeed)
train$humidity <- na.approx(train$humidity)

## 건물 데이터 변환
train$building_number <- as.factor(train$building_number)
train$weekday <- as.factor(train$weekday)
building$building_number <- as.factor(building$building_number)
building$building_type <- as.factor(building$building_type)
building$solar_power_capacity <- as.numeric(building$solar_power_capacity)
building$ess_capacity <- as.numeric(building$ess_capacity)
building$pcs_capacity <- as.numeric(building$pcs_capacity)


## 건물별로 데이터 보기
total <- left_join(train, building, by = "building_number")
names(total)
str(total)
total$building_number <- as.numeric(total$building_number)
str(total)
total$holiday <- 1
total$holiday <- ifelse(total$weekday %in% c("토요일", "일요일"), 0, ifelse(total$date %in% c("2022-06-01", "2022-06-06", "2022-08-15"), 0, 1))
##---------------------------------------------------------------------------------

########## 사본 생성
t1 <- total

#### 숫자형 아닌 데이터 지우고 상관성 확인
t1 <- t1 %>% 
  select(!weekday&!date)
t2 <- t1 %>% 
  select(!building_type)
a <- cor(t2)
t2_cor <- as.data.frame(a)
write.csv(t2_cor, "C:/k_digital/data/t2_cor.csv", row.names = TRUE)


## 상관성이 높은 변수들 골라내기
total <- total %>% 
  select(!ess_capacity&!ess&!cooling_area&!sunshine)

## 건물번호 별로 리스트 만들기
t2_list <- split(t2, t2$building_number)
as.data.frame(t2_list)
for(i in 1:100) {
  assign(paste0("c", i), t2_list[[as.character(i)]])
}

total_list <- split(total, total$building_number)
as.data.frame(total_list)
for(i in 1:100) {
  assign(paste0("b", i), total_list[[as.character(i)]])
}


#  각 건물의 시간대별 평균 (연면적 대비 전력) 소비량 계산하기
avg_power_list <- lapply(total_list, function(bldg) {
  bldg$power_per_area <- bldg$power_consumption / bldg$total_area
  avg_power <- aggregate(power_per_area ~ hour, data = bldg, mean)
})

# 각 건물의 시간대별 평균 (연면적 대비)전력 소비량을 하나의 데이터 프레임으로 합칩니다.
avg_power_df <- do.call(rbind, avg_power_list)
as.data.frame(avg_power_df)
write.csv(avg_power_df,'C:/k_digital/data/avg_power_df.csv', row.names=T)


set.seed(123)  # 재현성을 위한 seed 설정
clusters <- kmeans(avg_power_df, centers = 7)  

# 클러스터 결과를 데이터 프레임에 추가합니다.
## 시간별로 평균 나눈 것으로 그룹번호 매기기
avg_power_df$cluster <- as.factor(clusters$cluster)

######## avg_power_df의 열은 3개뿐이라 원래있던 데이터에 병합을 해야합니다.
######## b1~b100에 병합기준 공통열 'no'을 만듭니다. (나중에 봤더니 avg_power_df에서 공통 열로 할 수 있는 열의 이름은 'hour'라서 이후에 고칩니다.)
for(j in 1:100) {
  # 문자열을 사용하여 동적 변수 이름 생성
  data_name <- paste0("b", j)
  
  # 해당 데이터 프레임 가져오기
  df <- get(data_name)
  
  # hour 값을 no 열에 할당
  for(i in 0:24) {
    df$no[df$hour == i] <- i
  }
  
  # 변경된 데이터 프레임 할당
  assign(data_name, df)
}


##### avg_power_df를 건물별로 0~24시로 나눠 b1~b100에 할당할 수 있게 만듭니다.
# 데이터프레임 리스트 초기화
df_list <- list()

# 데이터프레임 분할
num_chunks <- nrow(avg_power_df) / 24
for(i in 1:num_chunks) {
  df_list[[i]] <- avg_power_df[((i-1)*24 + 1):(i*24), ]
}

# df_list에는 각 24행씩 분할된 데이터프레임들이 저장되어 있습니다.

##### b1~b100에 원래 있던 hour을 삭제하고 아까 만든 no를 hour로 바꿔줍니다.
df_list[[1]]

for (i in 1:100) {
  df_name <- paste0("b", i)
  
  # hour 열 삭제
  assign(df_name, subset(get(df_name), select = -hour))
  
  # no 열 이름을 hour로 변경
  assign(df_name, rename(get(df_name), hour = no))
}


####### 공통 열 hour를 통해 조인을 b1~b100까지 반복합니다.
merged_dfs <- list()

for (i in 1:100) {
  b_df <- get(paste0("b", i))  # b1부터 b100까지 데이터프레임 가져오기
  merged_df <- inner_join(b_df, df_list[[i]], by = "hour")  # hour를 기준으로 합치기
  merged_dfs[[i]] <- merged_df  # 결과를 리스트에 저장
}

####### 최종 b1~ b100을 하나의 데이터프레임으로 합칩니다.
final_merged_df <- bind_rows(merged_dfs)

####### 건물 번호, pcs 유무, holiday, solar장치 유무는 1과 0이기에 factor로 바꿉니다.
final_merged_df$building_number <- as.factor(final_merged_df$building_number)
final_merged_df$pcs <- as.factor(final_merged_df$pcs)
final_merged_df$holiday <- as.factor(final_merged_df$holiday)
final_merged_df$solar <- as.factor(final_merged_df$solar)

write.csv(final_merged_df,'C:/k_digital/data/final_merge.csv', row.names =T)

####### 이후 cluster 그룹번호로 데이터를 분할합니다.
split_df_list <- split(final_merged_df, final_merged_df$cluster)

####### 데이터 분할한 것을 a1~a7까지로 지정합니다.
for (i in 1:7) {
  assign(paste0("a", i), split_df_list[[as.character(i)]])
}

for (i in 1:7) {
  as.data.frame(paste0("a", i))
}

colnames(a1)
ab <- final_merged_df
ab1 <- ab %>% 
  filter(! cluster==1)
names(ab1)
abb1 <- glm(cluster~ ., family=binomial,data=ab1)
summary(abb1)

step(abb1, direction = 'both' )

str(ab)
ncol(ab)
nrow(ab)
