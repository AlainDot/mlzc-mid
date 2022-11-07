<img align="right" src="media/heart.png">

### mlzoomcamp-2022-11
*This is a Midterm project for ML Zoomcamp 2022*

# Heart failure clinical records

## Purpose of the project is to try to predict the probability of a patient to die in certain circumstances.

Heart failures are a very common cause of death.

The dataset contains 299 records of patients with heart failure ([Data Dictionnary](#data-dictionnary)). 

Each record describe the conditions of the patient and indication if the failure has caused death or not.
The idea is to try to identify the main factors causing the death and develop several models able to predict it.

- First the data were analysed to identify the main features.
- Then several models have been developed and fine tuned (parameters tuning).
- The best model (xgboost) after re-trained was exported and containerized using bentoml/docker.
- Docker image has been pushed to DockerHub and implemented in the could as a service.
- Progress are detailled in a series of consecutives jupyter notebooks ([Project](#project)). 

## Dataset source: 
- https://archive.ics.uci.edu/ml/datasets/Heart+failure+clinical+records 

## References:
- https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-020-1023-5


 

# Repository
- [bentoml](/bentoml/) :  model & docker
- [code](/code/) : python programs
- [data](/data/) : csv file from ICS
- [jupyter](/jupyter/) : follow-up of the project (step by step)
    - [pickle](/jupyter/pickle/) : pickle files storing objects between notebooks
- [media](/media/) : some media
- files : 
    - Pipfile
    - Pipfile.lock 
    - README.md (this file)


# Project
Consecutives notebooks (Data saved/loaded using picke):

- [01 Installation](/jupyter/01%20installation.md): step by step installation (pipenv)

- [02 Verify Configuration](/jupyter/02%20Verify%20Configuration.ipynb): package installed and version 
    
- [10 Load Data](jupyter/10%20Load%20Data.ipynb): very clean dataset (ready to use!)

- [11 Analyze all columns (features & target)](jupyter/11%20Analyze%20all%20columns%20(features%20&%20target).ipynb): 
    - data types, distribution of data, mean...
    - categorical vs numeric features    

- [15 Validation framework](jupyter/15%20Validation%20framework.ipynb): split dataset (sklearn)

- [16 Feature importance](jupyter/16%20Feature%20importance.ipynb): 
    - Risks of death by features
    - Features importance
    - Correlation
    - ROC AUC    

- [17 Basic Logistic Regression - Binary classification](jupyter/17%20Basic%20Logistic%20Regression%20-%20Binary%20classification.ipynb)
    - One-Hot-Encoding
    - Logistic regression (sklearn)     

- [20 Validation framework V2](jupyter/20%20Validation%20framework%20V2.ipynb): re-split the dataset after features adjustment    


- [21 Logistic Regression - Binary classification Optimization](jupyter/21%20Logistic%20Regression%20-%20Binary%20classification%20Optimization.ipynb): fine tune parameters
    - Solvers
    - Feature scaling + One-hot-encoding
    - C values

- [31Tree](jupyter/31Tree.ipynb): train model + tuning of
    - Decision tree Classifier
    - Random Forest
    - Xgboost   

- [41 Model selection - final Training - deployment](jupyter/41%20Model%20selection%20-%20final%20Training%20-%20deployment.ipynb)
    - Comparison of the 4 models developed - selection of Xgboost
    - Final training & evalution ([code/train_patient_death_risk.py](code/train_patient_death_risk.py)] also provided)
    - Build web service with pydantic - Test 
    - Save model with bentoml and produce docker file - Test   

- [51 Cloud Deployment (using mogenius cloud)](jupyter/51%20Cloud%20Deployment%20(using%20mogenius%20cloud).ipynb)
    - Dependencies described in pipfiles 
    - Docker image pushed to DockerHub:       
        https://hub.docker.com/r/alaindut/patient_death_risk_service/tags
    - Pull:      
        ```> docker pull alaindut/patient_death_risk_service:alaindut```
    - Implemented docker image in the Cloud at https://mogenius.com/home
    - Service runnig and tested:      
        https://alaindut-patie-prod-patient-death-risk-service-xejta4.mo5.mogenius.io/#/Service%20APIs/patient_death_risk_service__classify
    - Test data (input/output)
    	- Negatif: 
    		- *{"age": 55.0, "anaemia": "0", "creatinine_phosphokinase": 835, "diabetes": "0", "ejection_fraction": 40, "high_blood_pressure": "0", "platelets": 279000.0, "serum_creatinine": 0.7, "serum_sodium": 140, "sex": "1", "smoking": "1", "time": 147}*
    		- {'prediction': [0.02292894944548607], 'interpret': 'Death NOT probable'}
    	- Positif: 
    		- *{"age": 45.0, "anaemia": "0", "creatinine_phosphokinase": 2442, "diabetes": "1", "ejection_fraction": 30, "high_blood_pressure": "0", "platelets": 334000.0, "serum_creatinine": 1.1, "serum_sodium": 139, "sex": "1", "smoking": "0", "time": 129}*
    		- {'prediction': [0.9212774634361267], 'interpret': 'Death probable'}

**Note**: patient_death_risk_service will return **-1** in case of error (invalid data, field missing...).


# Data Dictionnary

- **Age**     	
Age of the patient (Years)

- **Anaemia**  
Decrease of red blood cells or hemoglobin [0, 1] 
   - *The hospital physician considered a patient having anaemia if haematocrit levels were lower than 36%*

- **High blood pressure**  	
If a patient has hypertension [0, 1]	

- **Creatinine phosphokinase (CPK)**  
Level of the CPK enzyme in the blood (mcg/L)
	 	 	 
- **Diabetes**  	
If the patient has diabetes	[0, 1]

- **Ejection fraction**  	
Percentage of blood leavingthe heart at each contraction (Percentage)
    - *That is the proportion of blood pumped out of the heart during a single contraction, given as a percentage with physiological values ranging between 50% and 75%.
    - Normal range: men=52–72% ; woman:54–74%. (https://www.healthline.com/health/ejection-fraction#ejection-fraction-results)* 

- **Sex**  
Woman or man [0, 1]
    - *Study covers 105 women and 194 men*

- **Platelets**  
Platelets in the blood (kiloplatelets/mL)

- **Serum creatinine**  	
Level of creatinine in the blood (mg/dL)	

- **Serum sodium**  	
Level of sodium in the blood (mEq/L)  

- **Smoking**  
If the patient smokes [0, 1]	

- **Time**  	
Follow-up period (Days)   

- **Death event**  
If the patient died during the follow-up period	[0, 1]



