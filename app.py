# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:13:14 2021

@author: HP
"""
from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
model = pickle.load(open("insu_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

         #Area_Service
        Area_Service=request.form['Area_Service']
        if(Area_Service=='Hudson Valley'):
            Area_Service=3
        elif(Area_Service=='Western NY'):
           Area_Service=6
        elif(Area_Service=='Central NY'):
           Area_Service=1
        elif(Area_Service=='Capital/Adirond'):
            Area_Service=0
        elif(Area_Service=='Finger Lakes'):
            Area_Service=2
        elif(Area_Service=='New York City'):
            Area_Service=4
        else:
            Area_Service=5
            
        
        #Age
        Age=request.form['Age']
        if(Age=='70 or Older'):
            Age=4
        elif(Age=='50 to 69'):
            Age=3
        elif(Age=='30 to 49'):
            Age=2
        elif(Age=='0 to 17'):
            Age=0
        else:
            Age=1
            
            
        # Gender
        Gender=request.form['Gender']
        if(Gender=='F'):
            Gender=0
        elif(Gender=='M'):
            Gender=1
        else:
           Gender=2
           
           
         # Cultural Group    
        Cultural_group=request.form['Cultural_group']
        if(Cultural_group=='White'):
            Cultural_group=3
            
        elif(Cultural_group=='Black/African American'):
            Cultural_group=0
            
            
        elif(Cultural_group=='Other Race'):
            Cultural_group=1
            
        else:
            Cultural_group=2
            
            
        #Ethnicity
        ethnicity=request.form['ethnicity']
        if(ethnicity=='Not Span/Hispanic'):
            ethnicity=0
            
        elif(ethnicity=='Spanish/Hispanic'):
            ethnicity=1
            
        else:
           ethnicity=2
           
           
          #Days_spend_hsptl
        Days_spend_hsptl = float(request.form["Days_spend_hsptl"])
        
        
        
        # Admission_Type
        Admission_type=request.form['Admission_type']
        if(Admission_type=='Emergency'):
            Admission_type=1
            
        elif(Admission_type=='Elective'):
            Admission_type=0
            
        elif(Admission_type=='Urgent'):
            Admission_type=5
            
        elif(Admission_type=='Newborn'):
            Admission_type=2
            
        elif(Admission_type=='Trauma'):
            Admission_type=4
            
        else:
            Admission_type=3
        
        
        #home_self_care    
        home_self_care=request.form['home_self_care']
        if(home_self_care=='Home or Self Care'):
            home_self_care=7
        elif(home_self_care=='Home w/ Home Health Services'):
            home_self_care=8
        elif(home_self_care=='Skilled Nursing Home'):
            home_self_care=18
        elif(home_self_care=='Expired'):
            home_self_care=4
        elif(home_self_care=='Short-term Hospital'):
            home_self_care=17
        elif(home_self_care=='Inpatient Rehabilitation Facility'):
            home_self_care=12
        elif(home_self_care=='Left Against Medical Advice'):
            home_self_care=13
        elif(home_self_care=='Psychiatric Hospital or Unit of Hosp'):
            home_self_care=16
        elif(home_self_care=='Hospice - Medical Facility'):
            home_self_care=11
        elif(home_self_care=='Hospice - Home'):
            home_self_care=10
        elif(home_self_care=='Another Type Not Listed'):
            home_self_care=0
        elif(home_self_care=='Facility w/ Custodial/Supportive Care'):
            home_self_care=5
        elif(home_self_care=='Court/Law Enforcement'):
            home_self_care=2
        elif(home_self_care=='Medicare Cert Long Term Care Hospital'):
           home_self_care=15
        elif(home_self_care=="Cancer Center or Children's Hospital"):
            home_self_care=1
        elif(home_self_care=='Hosp Basd Medicare Approved Swing Bed'):
            home_self_care=9
        elif(home_self_care=='Federal Health Care Facility'):
            home_self_care=6
        elif(home_self_care=='Critical Access Hospital'):
            home_self_care=3
        else:
            home_self_care=14
        
        
        
        #ccs_diagnosis_code    
        ccs_diagnosis_code = float(request.form["ccs_diagnosis_code"])
        
        
        #ccs_procedure_code
        ccs_procedure_code = float(request.form["ccs_procedure_code"])
        
        
        #code_illness
        Code_illness = int(request.form['Code_illness'])
        
        
         #mortality_risk
        mortality_risk = float(request.form["mortality_risk"])
        
        
        #Surgical description
        Surg_Description=request.form['Surg_Description']
        if(Surg_Description=='Medical'):
            Surg_Description=0
        elif(Surg_Description=='Surgical'):
            Surg_Description=2
        else:
            Surg_Description=1
            
            
        #Emergrncy Department
        emergency_dept_yes_no=request.form['emergency_dept_yes_no']
        if(emergency_dept_yes_no=='Y'):
            emergency_dept_yes_no=1
        else:
            emergency_dept_yes_no=0
            
            
        #Tot_charg
        Tot_charg = float(request.form["Tot_charg"])
        
        
          
        #Tot_cost
        Tot_cost = float(request.form["Tot_cost"])
        
        
         #Payment Typology
        Payment_Typology = int(request.form['Payment_Typology'])
                
         
        
        prediction=model.predict([[Area_Service,Age, Gender, Cultural_group,ethnicity, Days_spend_hsptl,Admission_type,home_self_care,ccs_diagnosis_code,ccs_procedure_code,Code_illness,mortality_risk,Surg_Description,emergency_dept_yes_no,Tot_charg,Tot_cost, Payment_Typology]])
           
        output=prediction

        if output>0:
            return render_template('home.html',prediction_text='The Claim for the Insurance is "FRAUDULENT"')
        else:
            return render_template('home.html',prediction_text='The Claim for the Insurance is "GENUINE"')
        
    else:
        return render_template("home.html")
       
   


if __name__ == "__main__":
    app.run(debug=True)