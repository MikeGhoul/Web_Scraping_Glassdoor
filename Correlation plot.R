# Correlation plot for glassdoor reviews
library(corrplot)

glassdoor <- read.csv('glassdoor.csv')

# removal of non-numerical columns:
gd_corr<- glassdoor[ , -c(1:3, 5, 7:13, 15)]

# removal of incomplete observations:
gd_corr<- gd_corr[complete.cases(gd_corr[ , ]) ,]

# calculation of the correlations:
gd_corr <- cor(gd_corr)

# plot of the correlations:
gd_corr_graph <- corrplot(gd_corr)
