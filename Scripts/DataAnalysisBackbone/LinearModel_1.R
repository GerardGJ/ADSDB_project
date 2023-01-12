library(DBI)
library(RPostgres)
library(MASS)
library(car)

postgres_driver <- dbDriver("Postgres")
con <- dbConnect(drv = postgres_driver,
                  user = 'biel.caballero',
                  password = 'DB130201',
                  host = 'postgresfib.fib.upc.edu',
                  port = '6433',
                  dbname = 'ADSDBbiel.caballero')

df <- dbGetQuery(con, "SELECT * from trainingtable")

#Fist we will need to change the type of the data to its correct type:
str(df)
df$tournament <- as.factor(df$tournament)
df$surface <- as.factor(df$surface)
df$draw_size <- as.factor(df$draw_size)
df$tourney_level <- as.factor(df$tourney_level)
df$winner_hand <- as.factor(df$winner_hand)
df$winner_ioc <- as.factor(df$winner_ioc)
df$loser_hand <- as.factor(df$loser_hand)
df$loser_ioc <- as.factor(df$loser_ioc)
df$best_of_x <- as.factor(df$best_of_x)
df$round_x <- as.factor(df$round_x)
df$series <- as.factor(df$series)
df$court <- as.factor(df$court)
df$location <- as.factor(df$location)
df$winner_ht <- as.numeric(df$winner_ht)
df$loser_ht <- as.numeric(df$loser_ht)
df$pl1_weight <- as.numeric(df$pl1_weight)
df$pl2_weight <- as.numeric(df$pl2_weight)
df$winningstreak <- as.numeric(df$winningstreak)
df$losingstreak <- as.numeric(df$losingstreak)
df$winner_rank <- as.numeric(df$winner_rank)
df$loser_rank <- as.numeric(df$loser_rank)
df$b365w <- as.numeric(df$b365w)
df$b365l <- as.numeric(df$b365l) #We won't use this variable as we only want to get the odds for 1 player
df$match_num <- as.numeric(df$match_num)
df$diff_rank_points <- as.numeric(df$diff_rank_points)
str(df)

summary(df)
df <- na.omit(df)

#After this we will look at the coorelations between our target variable and the rest of numerical vars

#Fist we will start building the model using only numerical data:
  #ALL numerical with no differences
m1 <- lm(b365w ~ match_num + winner_ht + winner_age + loser_ht + loser_age + winner_rank 
         + loser_rank + winner_rank_points + loser_rank_points + pl1_weight + pl2_weight 
         + winningstreak + losingstreak, data = df)

summary(m1)


m2 <- lm(b365w ~ match_num + diff_height + diff_age + diff_rank_points
         +diff_weight + winningstreak + losingstreak, data = df)
summary(m2)

m3 <- lm(b365w ~ match_num + winner_age + loser_age + winner_rank 
         + loser_rank + winner_rank_points + loser_rank_points + winner_bmi + loser_bmi  
         + winningstreak + losingstreak, data = df)
summary(m3)

m4 <- lm(b365w ~ match_num + diff_age + diff_rank_points
         + diff_bmi + winningstreak + losingstreak, 
         data = df)
summary(m4)

AIC(m1,m2,m3,m4,k=log(nrow(df))) #BIC

#After looking at the AIC we can conclude the best model is m4 which is the one with
#This model is the one that has the difference of the measurements between the winner and the loser. Also it is the one with the difference in BMI

#Now we will add the factors to the chosen models
m5 <- lm(b365w ~ (match_num + diff_age + diff_rank_points + diff_bmi + winningstreak + losingstreak) + (tournament + surface + draw_size + tourney_level
                 + winner_hand + winner_ioc + loser_hand + loser_ioc + best_of_x + round_x + series + court), data = df)
summary(m5)

anova(m4,m5) #As not sig we will keep the simpler model which is the one with out the factors
AIC(m4,m5,k=log(nrow(df))) # Also, m5 has a higher BIC than the m4 model 

par(mfrow = c(2,2))
plot(m4) 

#Looking at the Residuals vs Leverage plot we can see we have an influential data, this influential observation is 526 we need to delete it and will see how the model changes

inflm.m4 <- influence.measures(m4)
summary(inflm.m4)
df.noinflu <- df[-which(apply(inflm.m4$is.inf, 1, any)),]


m4.1 <- lm(b365w ~ match_num + diff_age + diff_rank_points + diff_bmi + winningstreak + losingstreak, data = df.noinflu)
plot(m4.1)

b <-boxcox(m4.1)
lambda <- b$x[which.max(b$y)];lambda

m4.2 <- lm(I(b365w^-1) ~ match_num + diff_age + diff_rank_points + diff_bmi + winningstreak + losingstreak, data = df.noinflu)
summary(m4.2)

m4.3 <- lm(I(b365w^-1) ~ match_num + diff_age + poly(diff_rank_points,6) + diff_bmi + winningstreak + losingstreak, data = df.noinflu)
summary(m4.3)
anova(m4.2,m4.3)
plot(m4.3)

inflm.m4 <- influence.measures(m4.3)
summary(inflm.m4)
df.noinflu <- df.noinflu[-which(apply(inflm.m4$is.inf, 1, any)),]

m4.4 <- lm(I(b365w^-1) ~ match_num + diff_age + poly(diff_rank_points,2) + diff_bmi + winningstreak + losingstreak, data = df.noinflu)
summary(m4.4)
anova(m4.3,m4.4)
plot(m4.3)
