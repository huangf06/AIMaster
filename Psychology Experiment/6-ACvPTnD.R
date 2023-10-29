library(lme4) # This is the package that we need for using LMMs

# First, specify the path to the datafile:
setwd('/Users/huangfei/Downloads/Psychology Experiment')
data <- read.csv('work_data.csv')

data <- na.omit(data)

# And we want to remove outliers:
outlier1 <- mean(data$reading_time) + 2.5 * sd(data$reading_time)
outlier2 <- mean(data$reading_time) - 2.5 * sd(data$reading_time)
data <- data[data$reading_time > outlier2,]
data <- data[data$reading_time < outlier1,]

# Transform the 'distractor' variable into a factor
data$paragraph_type <- as.factor(data$paragraph_type)
data$is_dyslexic <- as.factor(data$is_dyslexic)

data$paragraph_type <- relevel(data$paragraph_type, ref="plain")
data$is_dyslexic <- relevel(data$is_dyslexic, ref="FALSE")

Acc_model <- glmer(correct_response ~ paragraph_type * is_dyslexic + (1|subject), 
                   data = data, family = "binomial")

summary(Acc_model)