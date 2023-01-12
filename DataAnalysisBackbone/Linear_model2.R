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

df <- dbGetQuery(con, "SELECT * from featuresselected")

#Fist we will need to change the type of the data to its correct type:
str(df)

summary(df)
df <- na.omit(df)

#After this we will look at the coorelations between our target variable and the rest of numerical vars

#Fist we will start building the model using only numerical data:
#ALL numerical with no differences
m1 <- lm(b365w ~  loser_age + winner_rank + winner_rank_points + loser_rank + loser_rank_points, data = df)
summary(m1)

m2 <- lm(b365w ~ diff_weight + diff_rank_points, df)
summary(m2)

m3 <- lm(b365w ~  loser_age + winner_rank + winner_rank_points + loser_rank + loser_rank_points + diff_weight + diff_rank_points, data = df)


AIC(m1,m2,m3,k=log(nrow(df))) #BIC

#After looking at the AIC we can conclude the best model is m1 which is the one with the loser_age + winner_rank + loser_rank + loser_rank_points

inflm.m1 <- influence.measures(m1)
summary(inflm.m1)
df.noinflu <- df[-which(apply(inflm.m1$is.inf, 1, any)),]


m1.1 <- lm(b365w ~  loser_age + winner_rank + winner_rank_points + loser_rank + loser_rank_points, data = df)
plot(m1.1)

b <-boxcox(m1.1)
lambda <- b$x[which.max(b$y)];lambda

m1.2 <- lm(I(b365w^-1) ~ loser_age + winner_rank + poly(winner_rank_points,4)+ loser_rank + poly(loser_rank_points,4), data = df.noinflu)
anova(m1.1,m1.2)



df.test <- dbGetQuery(con, "SELECT * from testingtable")
str(df.test)
df.test$winner_rank <- as.numeric(df.test$winner_rank)
df.test$loser_rank <- as.numeric(df.test$loser_rank)
pred <- predict(m1.2,newdata = df.test)

sum((pred-df$b365w)^2)
