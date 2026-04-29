# Baseline Modeling Insights and Observations

## Best Performing Models
- Classification: Decision Tree (Accuracy=1.0000, F1=1.0000)
- Regression: Gradient Boosting Regressor (R2=0.9985, RMSE=0.0044)

## Overfitting and Underfitting Analysis
- Classification train-test accuracy gap: 0.0000. No strong overfitting signal in best classification model.
- Regression train-test R2 gap: 0.0015. No strong overfitting signal in best regression model.

## Impact of Feature Engineering
- Feature engineering increased signal density by combining EMI burden, credit behavior, and product quality indicators, while selection removed redundant correlated columns.
- Logistic Regression Accuracy before engineering: 0.9925
- Logistic Regression Accuracy after engineering: 0.9975
- Accuracy lift from engineering: 0.0050
- Linear Regression R2 before engineering: -2.1033
- Linear Regression R2 after engineering: 0.9775
- R2 lift from engineering: 3.0807
- Correlation-based filtering removed 6 redundant features.
- Final selected feature count: 31.

## Feature Selection Justification
- Selection combined two principles:
  1) Correlation filtering to reduce multicollinearity.
  2) Importance plus domain relevance to retain predictive financial indicators.
