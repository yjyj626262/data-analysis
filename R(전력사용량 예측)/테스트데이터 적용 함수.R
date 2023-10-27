## 테스트데이터 적용 모델
PC_forecast <- function(tt){

  library(lubridate)
  library(dplyr)
  library(rpart)
  library(e1071)
  library(randomForest)
  library(gbm)
  library(xgboost)
  
  tt <- rename(tt,
                 BID = `건물번호`, 
                 DateTime = `일시`, 
                 Temp = "기온.C.", 
                 Rain = "강수량.mm.", 
                 WS = `풍속.m.s.`, 
                 HM = `습도...`)
  tt$forecast <- NA
  tt$WorkD <- ifelse(substr(tt$DateTime, 1, 8) %in% c("20220827", "20220828"), 0, 1)
  tt$Time <- substr(tt$DateTime, 10,11)
  tt$Time <- as.factor(tt$Time)
  tt$DateTime <- ymd_h(tt$DateTime)
  tt$num_date_time <- NULL

  
for (i in 1:100){
  
  model <- model_eval$Model[i]
  data <- tt %>% 
    filter(BID==i)
  
  if (model == "DT") {
    loaded_model <- readRDS(paste0(i,"DT.rds"))
    tt$forecast <- predict(loaded_model, newdata=data)
  } else if (model=="LR") {
    loaded_model <- readRDS(paste0(i,"LR.rds"))
    tt$forecast <- predict(loaded_model, newdata=data)
  } else if (model=="SVM") {
    loaded_model <- readRDS(paste0(i,"SVM.rds"))
    tt$forecast <- predict(loaded_model, newdata=data)
  } else if (model=="RF") {
    loaded_model <- readRDS(paste0(i,"RF.rds"))
    tt$forecast <- predict(loaded_model, newdata=data)
  } else if (model=="GBoost") {
    loaded_model <- readRDS(paste0(i,"GBM.rds"))
    tt$forecast <- predict(loaded_model, newdata=data)
  } else if(model=="XGBoost") {
    loaded_model <- readRDS(paste0(i,"XGB.rds"))
    tt$forecast <- predict(loaded_model, newdata=data)
  }
  
}

return(tt)
}

a <- PC_forecast(test)



