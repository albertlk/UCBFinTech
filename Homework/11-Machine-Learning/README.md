# Mortgage Predictions

The goal of this project was to create a series of machine-learning models to predict whether or not to extend credit to a borrower. Two techniques were used: resampling and ensemble learning.

## Resampling

For the resampling methods, we used Random Oversampler and SMOTE to oversample (due to the imbalanced data), cluster centroids to undersample, and SMOTEENN to both over and undersample the data. Then we applied a simple regression model for predictions.

After the models were fit and predictions were made, key metrics were calculated for each model to compare models to one another. They are shown in the below table:

|                   | RandomOversampler | SMOTE | ClusterCentroids | SMOTTEEN |
|:-----------------:|:-----------------:|:-----:|:----------------:|:--------:|
| Balanced Accuracy |        0.65       |  0.65 |       0.52       |   0.62   |
|       Recall      |        0.67       |  0.66 |       0.42       |   0.55   |
|   Geometric Mean  |        0.65       |  0.65 |       0.51       |   0.61   |

As we can see in the table:

**RandomOversampler** had the best balanced accuracy score
**RandomOversampler** also had the best recall score
**RandomOversampler and SMOTE** were tied for the best geometric mean score

From this comparison, I would select RandomOversampler to conduct the predictions though I would not be too reliant on the results as even the best scores are relatively low.

## Ensemble Learning

For the ensemble learning methods, we used Balanced Random Forest Classifier and Easy Ensemble Classifier to make predictions.

After the models were fit and predictions were made, key metrics were calculated for each model to compare models to one another. They are shown in the below table:

|                   |  BRF  | Easy Ensemble |
|:-----------------:|:-----:|:-------------:|
| Balanced Accuracy | 0.800 |     0.925     |
|       Recall      |  0.92 |      0.94     |
|   Geometric Mean  |  0.79 |      0.93     |

As we can see in the table:

**Easy Ensemble Classifier** had the best balanced accuracy, recall, and geometric mean score, though Balanced Random Forest Classifier still performed much better than any of our resampling and simple regression models did.

From the Balanced Random Forest Classifer, we can see that the top three features were:

1. total_rec_prncp
2. total_pymnt
3. total_rec_int

The features that contributed next to nothing to the predictions at the tail end of the list are also useful to know as we can remove them from future analyses to reduce the amount of noise.

