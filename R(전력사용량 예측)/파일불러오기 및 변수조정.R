## 패키지 불러오기
library(dplyr)
library(ggplot2)

## 파일 불러오기
train <- read.csv("C:/BEC/train.csv")
test <- read.csv("C:/BEC/test.csv")
building_info <- read.csv("C:/BEC/building_info.csv")

## 사본 만들기
tn <- as.data.frame(train)
tt <- as.data.frame(test)
bi <- as.data.frame(building_info)

## 변수명 변경 : 한글 -> 영어
colnames(tn) <- c("num_date_time",
                  "BID",
                  "DateTime",
                  "Temp",
                  "Rain",
                  "WS",
                  "HM",
                  "SS",
                  "SR",
                  "PC")
colnames(tt) <- c("num_date_time",
                  "BID",
                  "DateTime",
                  "Temp",
                  "Rain",
                  "WS",
                  "HM")
colnames(bi) <- c("BID",
                  "BType",
                  "Grossrea",
                  "CoolArea",
                  "SolarCapa",
                  "ESSCapa",
                  "PCSCapa")


## 데이터 구조 살펴보기 및 변경
str(tn)
str(tt)
tn$Time <- substr(tn$DateTime, 10,11)
tt$Time <- substr(tt$DateTime, 10,11)
tn$DateTime <- as.POSIXct(tn$DateTime, format="%Y%m%d %H")
tt$DateTime <- as.POSIXct(tt$DateTime, format="%Y%m%d %H")
tt$num_date_time <- NULL
tn$num_date_time <- NULL
               
## 결측치 처리하기 : Rain, SS, SR

## 결측치 처리 -----------------------------------------------------------------

#### SS, SR, Rain <- 값 자체가 없어서 측정이 안된 경우

tn$SS <- ifelse(is.na(tn$SS), 0, tn$SS)
tn$SR <- ifelse(is.na(tn$SR), 0, tn$SR)
tn$Rain <- ifelse(is.na(tn$Rain), 0, tn$Rain)

#### WS, HM <- 단순히 0으로 처리하기에 어려운 결측치
library(zoo)

tn$WS <- na.approx(tn$WS)
tn$HM <- na.approx(tn$HM)


## 변수 추가 : WeekD, WorkD
install.packages("lubridate")
library(lubridate)
tn$WeekD <- weekdays(tn$DateTime)
tn$WorkD <- ifelse(tn$WeekD %in% c("토요일", "일요일"), 0, ifelse(format(tn$DateTime, "%Y-%m-%d") %in% c("2022-06-01", "2022-06-06", "2022-08-15"), 0, 1))



#### 데이터셋 확인
str(tn)

## 빌딩 타입 조인
tn <- left_join(tn, bi, by = "BID")



## PC(Power Consumption) 시계열 확인(건물 번호별)

for (i in 1:100) {
  BType <- tn %>%
    filter(BID == i) %>%
    pull(BType)  # BType 값을 추출
  
  plot <- tn %>%
    filter(BID == i) %>%
    ggplot(aes(x = DateTime, y = PC)) +
    geom_line() +
    labs(title = paste("BType", BType, "BID", i, "전력소비량 시계열 그래프 (단위:1시간)"), x = "날짜(시간별)", y = "전력사용량")
  
  ggsave(paste(BType, "BID", i, "전력소비량 시계열 그래프 (1시간).png"), plot, width = 20, height = 6)
}


## 