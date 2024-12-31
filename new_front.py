import streamlit as st
st.set_page_config(
     page_title="HEART PREDICTION APP",
     page_icon="❤"
)       
import numpy as np
import pickle

# Load the trained model 
model = pickle.load(open('model.pkl', 'rb'))

# Set up the Streamlit app
st.title("🏥 Heart Disease Prediction App")
st.write("Enter the following details to predict if you are at risk of heart disease:")

st.write("")
st.write("")

# Create and layout the input fields for user data to minimize vertical space
# Row 1: Age, Gender
col1, col2 = st.columns(2)
age = col1.number_input('Age', min_value=1, max_value=120, value=None)
sex = {"Male": 1, "Female": 0}.get(col2.selectbox('Gender',["Male","Female"],None))

# Row 2: Chest Pain Type, Resting BP , Serum Cholesterol
col3, col4 ,col5 = st.columns(3)
cp = {"Typical Angina": 0, "Atypical Angina": 1, "Non-anginal Pain": 2, "Asymptomatic": 3}.get(col3.selectbox('Chest Pain Type',["Typical Angina","Atypical Angina","Non-anginal Pain","Asymptomatic"], None))
trestbps = col4.number_input('Resting Blood Pressure (mm Hg)', min_value=50, max_value=250, value=None)
chol = col5.number_input('Serum Cholesterol (mg/dl)', min_value=100, max_value=600, value=None)

# Row 3: Fasting Blood Sugar, Resting ECG, Max Heart Rate
col6, col7, col8 = st.columns(3)
fbs = {"True":0, "False":1}.get(col6.selectbox('Fasting Blood Sugar > 120 mg/dl',["True", "False"],None))
restecg = {"Normal":0, "Having ST-T wave abnormality":1, "Probable or definite left ventricular hypertrophy":2} .get (col7.selectbox( 'Resting Electrocardiographic Results',["Normal", "Having ST-T wave abnormality", "Probable or definite left ventricular hypertrophy"],None))    
thalach = col8.number_input('Maximum Heart Rate Achieved', min_value=50, max_value=250, value=None)

# Row 4: Exercise Angina, ST Depression, Slope
col9, col10 ,col11 = st.columns(3)
exang = {"Yes": 0,"No": 1}.get(col9.selectbox('Exercise Induced Angina',["Yes","No"],None)) 
oldpeak = col10.number_input('ST Depression Induced by Exercise', min_value=0.0, max_value=10.0, value=None)
slope = {"Upsloping":0, "Flat":1, "Downsloping":2}.get(col11.selectbox('Slope of the Peak Exercise ST Segment',               ["Upsloping","Flat","Downsloping"],None)) 

#Row 5: Major Vessels, Thalassemia
col12, col13 = st.columns(2)
ca = col12.number_input('Number of Major Vessels (0-4)', min_value=0, max_value=4, value=None)
thal = {"Normal":0, "Fixed Defect":1, "Reversable Defect":2}.get(col13.selectbox('Thalassemia',["Normal", "Fixed Defect", 
                                                                                                "Reversable Defect"],None))

# Collect input data into an array
def input_data():
    return np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

# Predict heart disease based on user input
if st.button('Predict'):
    errors = []
    if age is None:
       errors.append("Please fill in the Age field.")
    elif sex is None:
         errors.append("Please select a Gender.")
    elif cp is None:
         errors.append("Please select a Chest Pain Type.")
    elif trestbps is None:
         errors.append("Please fill in the Resting Blood Pressure (mm Hg) field.")
    elif chol is None:
         errors.append("Please fill in the Serum Cholesterol (mg/dl) field.")
    elif fbs is None:
         errors.append("Please select Fasting Blood Sugar > 120 mg/dl.")
    elif restecg is None:
         errors.append("Please select Resting Electrocardiographic Results.")
    elif thalach is None:
         errors.append("Please fill in the Maximum Heart Rate Achieved field.")
    elif exang is None:
         errors.append("Please select Exercise Induced Angina.")
    elif oldpeak is None:
         errors.append("Please fill in the ST Depression Induced by Exercise field.")
    elif slope is None:
         errors.append("Please select Slope of the Peak Exercise ST Segment.")
    elif ca is None:
         errors.append("Please fill in the Number of Major Vessels (0-4) field.")
    elif thal is None:
         errors.append("Please select Thalassemia.")
     
    if errors:
        for error in errors:
            st.error(error)
    else:   
        try:
            # Call the function to get input data
            prediction = model.predict(input_data())
            if prediction[0] == 1:
                st.error("Warning! You might be at risk of heart disease.")
            else:
                st.success("Good news! You are unlikely to have heart disease.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
