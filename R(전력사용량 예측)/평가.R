smape <- function(actual, forecast) {
  n <- length(actual)
  sum_abs_diff <- sum(abs(actual - forecast))
  sum_actual <- sum(abs(actual) + abs(forecast))
  smape_value <- (2 * sum_abs_diff) / sum_actual
  return(smape_value)
}

saveRDS(smape, file = "smape.rds")
smape <- readRDS("smape.rds")


# SMAPE 계산
score <- smape(actual, forecast)
print(score)
