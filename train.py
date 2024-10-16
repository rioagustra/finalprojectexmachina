import streamlit as st
import pickle
import numpy as np

# Load the Logistic Regression model
with open('Logistic_Regression_Model.pkl', 'rb') as file:
    logistic_regression_model = pickle.load(file)

# Print out the feature names expected by the Logistic Regression model
print(f"Number of expected features: {logistic_regression_model.n_features_in_}")
print("Expected feature names (if available):")
try:
    print(logistic_regression_model.feature_names_in_)
except AttributeError:
    print("Feature names not stored in the model. Please ensure feature order matches.")

# Web App Design
html_temp = """<div style="background-color:#4CAF50;padding:10px;border-radius:10px">
                <h1 style="color:white;text-align:center">Customer Segmentation Prediction App</h1>
              </div>"""

def main():
    st.markdown(html_temp, unsafe_allow_html=True)
    st.sidebar.header("Customer Information")

    # Input Fields
    gender = st.sidebar.selectbox('Gender', ['Male', 'Female'])
    married = st.sidebar.selectbox('Ever Married', ['Yes', 'No'])
    age = st.sidebar.slider('Age', 18, 100, 30)
    graduated = st.sidebar.selectbox('Graduated', ['Yes', 'No'])
    work_experience = st.sidebar.number_input('Work Experience (years)', min_value=0, max_value=50, value=1)
    spending_score = st.sidebar.selectbox('Spending Score', ['Low', 'Average', 'High'])
    family_size = st.sidebar.number_input('Family Size', min_value=1, max_value=10, value=3)
    profession = st.sidebar.selectbox('Profession', 
                                      ['Artist', 'Doctor', 'Engineer', 'Entertainment', 
                                       'Healthcare', 'Homemaker', 'Lawyer', 'Marketing'])
    var1 = st.sidebar.selectbox('Var_1', ['Cat_1', 'Cat_2', 'Cat_3', 'Cat_4', 'Cat_5', 'Cat_6', 'Cat_7'])

    if st.button("Predict Segmentation"):
        result = predict_segmentation(gender, married, age, graduated, work_experience, 
                                      spending_score, family_size, profession, var1)
        st.success(f"The predicted customer segmentation is: {result}")

# Prediction Function
def predict_segmentation(gender, married, age, graduated, work_experience, 
                         spending_score, family_size, profession, var1):
    # Encode Inputs
    gender = 1 if gender == 'Male' else 0
    married = 1 if married == 'Yes' else 0
    graduated = 1 if graduated == 'Yes' else 0
    spending_score_map = {'Low': 0, 'Average': 1, 'High': 2}
    spending_score = spending_score_map[spending_score]

    # One-hot encoding for Profession and Var_1
    profession_map = {'Artist': 0, 'Doctor': 1, 'Engineer': 2, 'Entertainment': 3,
                      'Healthcare': 4, 'Homemaker': 5, 'Lawyer': 6, 'Marketing': 7}
    var1_map = {'Cat_1': 0, 'Cat_2': 1, 'Cat_3': 2, 'Cat_4': 3, 
                'Cat_5': 4, 'Cat_6': 5, 'Cat_7': 6}

    profession_encoded = np.zeros(8)
    var1_encoded = np.zeros(7)
    profession_encoded[profession_map[profession]] = 1
    var1_encoded[var1_map[var1]] = 1

    # Create the input vector
    input_data = np.concatenate(([gender, married, age, graduated, work_experience, 
                                  spending_score, family_size], profession_encoded, var1_encoded))

    # Make Prediction
    prediction = logistic_regression_model.predict([input_data])[0]
    segmentation_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    return segmentation_map[prediction]

if __name__ == "__main__":
    main()
