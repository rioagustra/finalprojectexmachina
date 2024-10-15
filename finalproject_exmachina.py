import streamlit as st
import streamlit.components.v1 as stc
import pickle

with open('Random_Forest_Model.pkl', 'rb') as file:
    Random_Forest_Model = pickle.load(file)

html_temp = """<div style="background-color:#000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Loan Eligibility Prediction App</h1> 
                <h4 style="color:#fff;text-align:center">Made for: Credit Team</h4> 
                """

desc_temp = """ ### Multiclass Classification App 
                Aplikasi data science untuk menentukan class atau kategori seseorang ketika ingin membeli mobil
                dengan pendekatan Random Forest Model
                #### Data Source
                Rio Agustra - SPE
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#fff">Multiclass Classification</h1>
                </div
             """
    st.markdown(design, unsafe_allow_html=True)
    left, right = st.columns((2,2))
    Gender = left.selectbox('Gender', ('Male', 'Female'))
    Ever_Married = right.selectbox('Ever_Married', ('Yes', 'No'))
    Age = left.number_input('Age')
    Graduated = right.selectbox('Graduated', ('Yes', 'No'))
    Profession  = left.selectbox('Profession', ('Artist', 'Healthcare', 'Entertainment', 'Engineer', 'Doctor', 'Lawyer', 'Executive', 'Marketing', 'Homemaker'))
    Spending_Score = right.selectbox('Spending_Score', ('low', 'medium', 'high'))
    Work_Experience = left.number_input('Work_Experience')
    Family_Size = left.number_input('Family_Size')
    Var_1  = left.selectbox('Var_1', ('A', 'B', 'C', 'D', 'E', 'F', 'G'))
    button = st.button("Guess a Class")

    #If button is clicked
    if button:
        result = predict(Gender, Ever_Married, Age, Graduated, Profession, Spending_Score, Work_Experience, Family_Size, Var_1)

        if result == 'Eligible':
            st.success(f'You are {result} as your class')
        else:
            st.warning(f'You are {result} sorry')

def predict(Gender, Ever_Married, Age, Graduated, Profession, Spending_Score, Work_Experience, Family_Size, Var_1):
    #Process user input
    gen = 0 if Gender == 'Male' else 1
    mar = 0 if Ever_Married == 'No' else 1
    spen = 0 if Spending_Score == 'low' else 1 if Spending_Score == 'medium' else 2
    gra = 0 if Graduated == 'No' else 1
    prof = 0 if Profession == 'Artist' else 1 if Profession == 'Doctor' else 2 if Profession == 'Engineer' else 3 if Profession == 'Entertainment' else 4 if Profession == 'Executive' else 5 if Profession == 'Healthcare' else 6 if Profession == 'Homemaker' else 7 if Profession == 'Lawyer' else 8
    var = 0 if Var_1 == 'A' else 1 if Var_1 == 'B' else 2 if Var_1 == 'C' else 3 if Var_1 == 'D' else 4 if Var_1 == 'E' else 5 if Var_1 == 'F' else 6

    #Making prediction
    prediction = Random_Forest_Model.predict([[gen,mar,Age,gra,prof,spen,Work_Experience,Family_Size,var]])
    result = 'A' if prediction == 0 else 'B' if prediction == 1 else 'C' if prediction == 2 else 'D'
    return result

if __name__ == "__main__":
    main()