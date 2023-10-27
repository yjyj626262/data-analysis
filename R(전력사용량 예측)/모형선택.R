## 패키지 불러오기
library(dplyr)
library(rpart)
library(e1071)
library(randomForest)
library(gbm)
library(xgboost)
## 평가 데이터프레임 만들기
model_eval2 <- data.frame(
  DT=numeric(100),
  LR=numeric(100),
  SVM=numeric(100),
  RF=numeric(100),
  GBoost=numeric(100),
  XGBoost=numeric(100)
)
tnset

str(model_eval2)
tnset$SR
for (i in 1:100){
  
  tnset <- tn %>% 
    filter(BID==i & DateTime < "2022-08-18 00:00:00") %>% 
    select(Temp, SR, WS, HM, Time, WorkD)
  tnset$Time <- as.factor(tnset$Time)
  tnset$WorkD <- as.factor(tnset$WorkD)
  
  ttset <- tn %>% 
    filter(BID==i & DateTime >= "2022-08-18 00:00:00") %>% 
    select(Temp, SR, WS, HM, Time, WorkD)
  ttset$Time <- as.factor(ttset$Time)
  ttset$WorkD <- as.factor(ttset$WorkD)
  
  # 예측값과 비교할 실제 데이터
  actual <- ttset$SR
  
  #############################################################################
  ## 의사결정트리
  model_DT <- rpart(SR ~ ., data=tnset)
  
  ## DT 평가점수 SMAPE
  forecast <- predict(model_DT, newdata=ttset)
 
  model_eval2[i,"DT"] <- smape(actual, forecast)
  ############################################################################
  ############################################################################
  ## 서포트벡터머신
  model_SVM <- svm(SR~., data=tnset, kernel="linear")
  forecast <- predict(model_SVM, newdata = ttset)
  model_eval2[i,"SVM"] <- smape(actual, forecast)
  ############################################################################
  ## 랜덤포레스트
  model_RF <- randomForest(SR~., data=tnset)
  forecast <- predict(model_RF, newdata = ttset)
  model_eval2[i,"RF"] <- smape(actual, forecast)
  ############################################################################
  ## 그래디언트부스팅
  model_GBM <- gbm(SR~., data=tnset, distribution="gaussian",
                   n.trees=100, interaction.depth=5)
  forecast <- predict(model_GBM, newdata = ttset)
  model_eval2[i,"GBoost"] <- smape(actual, forecast)
  ############################################################################
  ## XG부스팅
  data_matrix <- as.matrix(tnset[,-c(5,6)])
  label_vector <- tnset$SR
  model_XGB <- xgboost(data=data_matrix, label=label_vector, nrounds=100,  params = list(objective = "reg:squarederror", alpha = 1))
  new_data_matrix <- as.matrix(ttset[,-c(5,6)])
  forecast <- predict(model_XGB, newdata=new_data_matrix)
  model_eval2[i,"XGBoost"] <- smape(actual, forecast)

}
str(tnset)
summary(tnset)

## 각 건물별 최적의 모델을 출력

model_eval2$min_smape <- apply(model_eval2, 1, min)
models <- colnames(model_eval2)
min_models <- models[apply(model_eval2[,1:7], 1, which.min)]
model_eval2$Model <- min_models
model_eval2$min_smape <- as.numeric(model_eval2$min_smape)
str(model_eval2)

model_eval2$BID <- 1:100
model_eval2 <- model_eval2[, c("BID","Model","min_smape","DT","LR","SVM","RF","GBoost","XGBoost")]
