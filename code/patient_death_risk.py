print('***** Starting patient_death_risk.py 11.54 *****')

import numpy as npy
import bentoml
from bentoml.io import JSON
from pydantic import BaseModel
from typing import List

print('*** Import completed ***')

class Patient(BaseModel):
    age: float
    anaemia: str
    creatinine_phosphokinase: int
    diabetes: str
    ejection_fraction: int
    high_blood_pressure: str
    platelets: float
    serum_creatinine: float
    serum_sodium: int
    sex: str
    smoking: str
    time: int

print('*** Get model ***')
modBnt = bentoml.xgboost.get("patient_death_risk:rcznhj22xwjg4nht")
dvt = modBnt.custom_objects['dictVectorizer']

print('*** Run mmodel ***')
modBntRun = modBnt.to_runner()
svc = bentoml.Service("patient_death_risk_service", runners=[modBntRun])

@svc.api(input=JSON(), output=JSON())
# Next option will not allow error handling: better to check later pydantic model with parse_obj !
#@svc.api(input=JSON(pydantic_model=Patient), output=JSON())

async def classify(patient):
    print('\n\n*** in classify ***')

    # should be a dict
    print('*** type(patient) :' , type(patient)) 
    # "must be like { "val1" : val1 , ...}"
    print('*** patient :' , patient)

    print('*** parsing patient with pydantc Class')
    try:
        booOK = False
        Patient.parse_obj(patient)
        print('*** parsing patient OK')
        booOK = True
    except Exception as err:
        strErr = str(err).replace('\n' , ' : ')
        print("*** parsing patient NOT OK *** Error: \n" , strErr )
    

    if booOK:
        X_pat = dvt.transform(patient)
        print('*** X:' , X_pat)

        print('*** predict... beg' )
        prd = await modBntRun.predict.async_run( X_pat )
        print('*** predict... end' )

        if prd > 0.5:
            strPrd = 'Death probable'
        else:
            strPrd = 'Death NOT probable' 
    else:
        # in case of error return -1
        prd = -1
        strPrd = strErr
    
    print('>*** prd = ' , prd , ' - interpret :' , strPrd  )
    return( { "prediction" : prd , "interpret" : strPrd  })