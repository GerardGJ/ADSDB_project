library(DBI)
library(RPostgres)
library(MASS)
library(car)
library(FactoMineR)
library(dplyr)
library(factoextra)
library(ggplot2)
library(Boruta)

postgres_driver <- dbDriver("Postgres")
con <- dbConnect(drv = postgres_driver,
                  user = 'biel.caballero',
                  password = 'DB130201',
                  host = 'postgresfib.fib.upc.edu',
                  port = '6433',
                  dbname = 'ADSDBbiel.caballero')

df <- dbGetQuery(con, "SELECT * from trainingtable")

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
#Now we will perform the Advanced Topic on Feature Selection for b365w

boruta_output <- Boruta(b365w ~ ., data=na.omit(df), doTrace=0)
boruta_signif <- getSelectedAttributes(boruta_output, withTentative = TRUE)
print(boruta_signif)

roughFixMod <- TentativeRoughFix(boruta_output)
boruta_signif <- getSelectedAttributes(roughFixMod)
print(boruta_signif)

imps <- attStats(roughFixMod)
imps2 = imps[imps$decision != 'Rejected', c('meanImp', 'decision')]
head(imps2[order(-imps2$meanImp), ])  # descending sort

plot(boruta_output, cex.axis=.7, las=2, xlab="", main="Variable Importance")  
#The variables selected are loser_rank, date and match num.

#Now we will perform the Advanced Topic on Feature Selection for b365l

boruta_output <- Boruta(b365l ~ ., data=na.omit(df), doTrace=0)
boruta_signif <- getSelectedAttributes(boruta_output, withTentative = TRUE)
print(boruta_signif)

roughFixMod <- TentativeRoughFix(boruta_output)
boruta_signif <- getSelectedAttributes(roughFixMod)
print(boruta_signif)

imps <- attStats(roughFixMod)
imps2 = imps[imps$decision != 'Rejected', c('meanImp', 'decision')]
head(imps2[order(-imps2$meanImp), ])  # descending sort

plot(boruta_output, cex.axis=.7, las=2, xlab="", main="Variable Importance")  
#The variables selected are b365w, winner_rank, loser_rank, loser_age, winner_rank_points, diff_age and diff_rank_points.













