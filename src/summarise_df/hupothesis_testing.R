library(ggplot2)
library("ggpubr")
library(tidyverse)
library(ggpubr)
library(rstatix)

attempt_df <- read.csv(url("https://hvrlxy.github.io/assets/datasets/sbg_csv/attempts.csv"))

bx <- ggplot(data = attempt_df, aes(x = factor(is_passed), y = year )) + 
  geom_boxplot(fill = "blue") + 
  ggtitle("Distribution of Gas Mileage") +
  ylab("year") + 
  xlab("is_passed") 
bx

attempts_tibble <- attempt_df %>% as_tibble()

#percentage_checkpoint
#summary
attempts_tibble %>%
  group_by(is_passed) %>%
  get_summary_stats(percentage_checkpoint, type = "mean_sd")

#plot the distribution
ggboxplot(attempts_tibble, x = "is_passed", y = "percentage_checkpoint")

#outliers
attempts_tibble %>% 
  group_by(is_passed) %>%
  identify_outliers(percentage_checkpoint)

#Shapiro test for normality
attempts_tibble %>%
  group_by(is_passed) %>%
  shapiro_test(percentage_checkpoint)

#perform the test
t.test (percentage_checkpoint ~ is_passed, var.equal=TRUE, data = attempt_df)

attempt_2 <- attempt_df[attempt_df$checkpoint_no > 15, ]
t.test (percentage_checkpoint ~ is_passed, var.equal=TRUE, data = attempt_2)


#Shapiro test for normality
attempts_tibble %>%
  group_by(is_passed) %>%
  shapiro_test(average_attempt)

#plot the distribution
ggplot(data = attempt_df, aes(x = average_attempt)) + 
  geom_histogram(bins = 20) + 
  ggtitle("Distribution of average attempts by Passing Status") +
  xlab("Average Attempts") + 
  ylab("") + 
  facet_grid(. ~ is_passed)

#perform the test
res.aov <- aov(average_attempt ~ is_passed, data = attempt_df)
t.test (average_attempt ~ is_passed, var.equal=TRUE, data = attempt_df)
summary(res.aov)

#number of attempts so far
attempt_2 <- attempt_df[attempt_df$no_attempt != -1, ]
#plot the distribution
ggplot(data = attempt_2, aes(x = no_attempt)) + 
  geom_histogram(bins = 20) + 
  ggtitle("Distribution of number of attempts by Passing Status") +
  xlab("Number of  Attempts") + 
  ylab("") + 
  facet_grid(. ~ is_passed)

#perform the test
t.test (no_attempt ~ is_passed, var.equal=TRUE, data = attempt_df)
res.aov <- aov(no_attempt ~ is_passed, data = attempt_df)
summary(res.aov)

attempt_2 <- attempt_df[attempt_df$office_hours != 0, ]
t.test (office_hours ~ is_passed, var.equal=TRUE, data = attempt_2)

#background test
#confidence level
#plot the distribution
attempt_2 <- attempt_df[attempt_df$confidence != -1, ]
ggplot(data = attempt_2, aes(x = confidence)) + 
  geom_histogram(bins = 20) + 
  ggtitle("Distribution of number of attempts by Passing Status") +
  xlab("Number of  Attempts") + 
  ylab("") + 
  facet_grid(. ~ is_passed)
#perform the t-test
t.test (confidence ~ is_passed, var.equal=TRUE, data = attempt_df)

#class year
#plot the distribution
attempt_2 <- attempt_df[attempt_df$year != -1, ]
ggplot(data = attempt_2, aes(x = year)) + 
  geom_histogram(bins = 20) + 
  ggtitle("Distribution of number of attempts by Passing Status") +
  xlab("Number of  Attempts") + 
  ylab("") + 
  facet_grid(. ~ is_passed)
#t-test
attempt_2 <- attempt_df[attempt_df$year != -1, ]
t.test (year ~ is_passed, var.equal=TRUE, data = attempt_df)

#duration (semester) from the last mathematics course
attempts_tibble <- attempts_tibble %>% mutate(
  within_a_year = duration < 2
)

#do chi squared test
chisq.test(attempts_tibble$is_passed, attempts_tibble$within_a_year, correct=FALSE)
#plot the distribution
attempt_2 <- attempt_df[attempt_df$duration != -1, ]
ggplot(data = attempt_2, aes(x = duration)) + 
  geom_histogram(bins = 20) + 
  ggtitle("Distribution of number of attempts by Passing Status") +
  xlab("Number of  Attempts") + 
  ylab("") + 
  facet_grid(. ~ is_passed)

#t-test
t.test (duration ~ is_passed, var.equal=TRUE, data = attempt_df)


