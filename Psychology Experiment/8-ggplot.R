# Load necessary libraries
library(ggplot2)
library(lme4)

# Load the data
setwd('/Users/huangfei/Downloads/Psychology Experiment')
data <- read.csv('work_data.csv')

# Preprocess the data (as per your provided R script)
data <- na.omit(data)
data <- data[data$correct_response == 'TRUE',]
outlier1 <- mean(data$reading_time) + 2.5 * sd(data$reading_time)
outlier2 <- mean(data$reading_time) - 2.5 * sd(data$reading_time)
data <- data[data$reading_time > outlier2,]
data <- data[data$reading_time < outlier1,]
data$paragraph_type <- as.factor(data$paragraph_type)
data$is_dyslexic <- as.factor(data$is_dyslexic)
data$paragraph_type <- relevel(data$paragraph_type, ref="plain")
data$is_dyslexic <- relevel(data$is_dyslexic, ref="FALSE")

# Create the interaction effect plot using ggplot2
p <- ggplot(data, aes(x=paragraph_type, y=reading_time, color=is_dyslexic)) +
  geom_point(position=position_jitter(width=0.2, height=0), alpha=0.5) + 
  stat_summary(fun=mean, geom="line", aes(group=is_dyslexic)) + 
  stat_summary(fun=mean, geom="point", size=3) +
  labs(title="Interaction Effect of Paragraph Type and Dyslexia on Reading Time",
       x="Paragraph Type", y="Average Reading Time (seconds)") +
  theme_minimal()

ggsave("interaction_plot.png", plot = p, width = 10, height = 6, dpi = 300)