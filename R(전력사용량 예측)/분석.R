library(dplyr)


## 02. 워킹데이별 건물별 전력사용량 분포
# diff.yes <- 1이면 차이가 있고, 0이면 차이가 없음

for (i in 1:100){
  a <- tn %>% 
    filter(BID == i & WorkD == 1) %>% 
    select(PC)
  b<- tn %>% 
    filter(BID == i & WorkD == 0) %>%
    select(PC)
  t_test_result <- t.test(a,b, alternative ="two.sided")
  bi$diff.yes[i] <- ifelse(t_test_result$p.value < 0.05, 1, 0)
}

tn <- left_join(tn, bi, by = "BID")


## 건물번호 1번 데이터셋 만들기(b1)
b1 <- tn %>% 
  filter(BID==1) %>% 
  select(PC, Temp, Rain, WS, HM, Time, WorkD, DateTime)

## 훈련 세트, 테스트 세트 분리하기
b1_train <- b1 %>% 
  filter(DateTime < "2022-08-18 00:00:00")

b1_test <- b1 %>% 
  filter(DateTime >= "2022-08-18 00:00:00")
names(b1)
############################################################# 상관관계 분석
cor_matrix <- cor(b1[-8])
cor(b1[-c(8)])
dev.off()
heatmap(cor_matrix,
        col = colorRampPalette(c("blue", "white", "red"))(50),
        scale="none",
        symm = TRUE,
        margins = c(10,10))

plot(b1[-c(8,10)])

install.packages("corrplot")
library(corrplot)

############################################################# 의사결정트리
################# smape = 0.1152409
names(b1_train)
library(rpart)
model_DT <- rpart(PC ~ Temp+Rain+WS+HM+Time+WorkD, data=b1_train)
prediction_DT <- predict(model_DT, newdata=b1_test)

actual <- b1_test$PC
forecast <- prediction_DT
############################################################# 회귀분석(stepwise)
################# smape = 0.08393538

model_LR <- lm(PC~., data=b1_train)
model_LR <- step(model_LR, direction="both")
prediction_LR <- predict(model_LR, newdata=b1_test)
forecast <- prediction_LR


############################################################# 서포트벡터회귀
################# smape = 0.08756288
install.packages("e1071")
library(e1071)
model_SVM <- svm(PC~., data=b1_train, kernel="linear")
prediction_SVM <- predict(model_SVM, newdata = b1_test)
forecast <- prediction_SVM

############################################################# 랜덤포레스트회귀
################# smape = 0.08638105
install.packages("randomForest")
library(randomForest)
model_RF <- randomForest(PC~., data=b1_train)
prediction_RF <- predict(model_RF, newdata = b1_test)
forecast <- prediction_RF

############################################################# 그래디언트부스팅
################# smape = 0.09123818
install.packages("gbm")
library(gbm)
b1_train$Time <- as.factor(b1_train$Time)
names(b1_train)
model_GBM <- gbm(PC~Temp+Rain+WS+HM+Time+WorkD, data=b1_train, distribution="gaussian",
                 n.trees=100, interaction.depth=5)
prediction_GBM <- predict(model_GBM, newdata = b1_test)
forecast <- prediction_GBM

############################################################# XG부스트
################# smape = 0.2677512
install.packages("xgboost")
library(xgboost)
str()
data_matrix <- as.matrix(b1_train[,-c(1,6,8)])
label_vector <- b1_train$PC

str(b1_train)
model_XGB <- xgboost(data=data_matrix, label=label_vector, nrounds=100, objective="reg:squarederror")
new_data_matrix=as.matrix(b1_test[,-c(1,6,8)])
prediction_XGB <- predict(model_XGB, newdata=new_data_matrix)
forecast <- prediction_XGB

############################################################# LSTM
################# smape =
install.packages("keras")
library(keras)
install.packages("reticulate")
install.packages("tensorflow")
reticulate::install_miniconda()
library(tensorflow)
library(dplyr)

set.seed(123)
time_series <- ts(rnorm(100), frequency = 1)
model <- keras_model_sequential()
