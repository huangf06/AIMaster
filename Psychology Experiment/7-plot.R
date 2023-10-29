setwd('/Users/huangfei/Downloads/Psychology Experiment')
data <- read.csv('work_data.csv')

p <- ggplot(data, aes(x=highlight_speed, y=reading_time, color=factor(is_dyslexic))) +
  geom_point() +
  labs(x="Highlight Speed", y="Reading Time", color="Is Dyslexic") +
  theme_minimal() # 添加简洁的主题

ggsave(filename = "my_scatterplot.png", plot = p, width = 6, height = 4)