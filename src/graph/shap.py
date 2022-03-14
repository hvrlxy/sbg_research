from sklearn.model_selection import train_test_split
import xgboost
import shap
import numpy as np
import matplotlib.pylab as pl
import pandas as pd
from xgboost import cv
# from shap.models._teacher_forcing import TeacherForcing

# print the JS visualization code to the notebook
# shap.initjs()

# print(shap.__version__)

attempts_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/attempts.csv")
attempts_df = attempts_df.drop(columns=['Unnamed: 0'])
attempts_df = attempts_df.dropna()

# print(list(attempts_df['office_hours']))

X = attempts_df.iloc[:, [i for i in range(1, 9)]]
y = attempts_df['is_passed']

# create a train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=7)
d_train = xgboost.DMatrix(X_train, label=y_train)
d_test = xgboost.DMatrix(X_test, label=y_test)

params = {
    "eta": 0.01,
    "objective": "binary:logistic",
    "subsample": 0.5,
    "base_score": np.mean(y_train),
    "eval_metric": "logloss"
}
model = xgboost.train(params, d_train, 5000, evals = [(d_test, "test")], verbose_eval=100, early_stopping_rounds=20)

xgb_cv = cv(dtrain=d_train, params=params, nfold=3,
                    num_boost_round=50, early_stopping_rounds=10, metrics="auc", as_pandas=True, seed=123)

print(xgb_cv)

xgboost.plot_importance(model, importance_type="gain")
pl.title('xgboost.plot_importance(model, importance_type="cover")')
# pl.show()

# this takes a minute or two since we are explaining over 30 thousand samples in a model with over a thousand trees
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

