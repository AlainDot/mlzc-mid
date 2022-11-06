#!/usr/bin/env python
# coding: utf-8

import pandas as pda
import numpy as npy
import pickle
from IPython.display import display
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score
import xgboost as xgb
from pydantic import BaseModel
import bentoml

# #### Reload data from previous notebooks

# use TRAin FULL dataset
strFil = '.\pickle\dstTraFul.bin'
with open(strFil, 'rb') as filIn: 
    dfrTraFul, y_TraFul = pickle.load(filIn)

# use TRAin dataset
strFil = '.\pickle\dstTra.bin'
with open(strFil, 'rb') as filIn: 
    dfrTra, y_Tra = pickle.load(filIn)

# check wil VALidation dataset
strFil = '.\pickle\dstVal.bin'
with open(strFil, 'rb') as filIn: 
    dfrVal, y_Val = pickle.load(filIn)
dfrVal.shape , len(y_Val)

# use TST dataset
strFil = '.\pickle\dstTst.bin'
with open(strFil, 'rb') as filIn: 
    dfrTst, y_Tst = pickle.load(filIn)
dfrTst.shape , len(y_Tst)

strFil = '.\pickle\strTar.bin'
with open(strFil, 'rb') as filIn: 
    strTar = pickle.load(filIn)

strFil = '.\pickle\dfrFea.bin'
with open(strFil, 'rb') as filIn: 
    dfrFea = pickle.load(filIn)

dfrTraFul = dfrTraFul.drop( ['death_event'] , axis=1)

# ### xgboost: Final    T R A I N I N G

dvt = DictVectorizer(sparse=False)
dicTraFul = dfrTraFul.to_dict(orient='records')
X_TraFul = dvt.fit_transform(dicTraFul)
dmaTraFul = xgb.DMatrix(X_TraFul, label=y_TraFul )

dicTst = dfrTst.to_dict(orient='records')
X_Tst = dvt.transform(dicTst)
dmaTst = xgb.DMatrix(X_Tst)

xgb_params = { 
    'eta': 0.5, 
    'max_depth': 2,
    'min_child_weight': 2,
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'nthread': 8, 'seed': 1, 'verbosity': 1  }

modXgb = xgb.train(xgb_params, dmaTraFul, num_boost_round=125 )


# ### Save xgboost using BENTOML

modBen = bentoml.xgboost.save_model(
    'patient_death_risk',
    modXgb,
    custom_objects={
        'dictVectorizer': dvt
    })

print(modBen.info.to_dict())

print(modBen.path)

print(modBen.custom_objects)

