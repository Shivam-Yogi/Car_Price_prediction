import streamlit as st
# import pandas as pd
import numpy as np
import pickle
import mysql.connector

db_connection = mysql.connector.connect(
    user='root',
    password='Shivam@123',
    host='localhost',
    database='feedback',
    auth_plugin='mysql_native_password'
)
db_cursor = db_connection.cursor()

st.set_page_config(page_title="Elites Price Predictor", layout="wide")
st.title("Data Elites")
st.markdown("*Empower Your Car Decisions with Data Elites - Where Insights Drive Confidence.*")
st.image("Screenshot 2023-08-25 150653.png")


def set_custom_dark_theme():
    custom_dark_theme = """
    <style>
    body {
        background-color: #1a1a1a;
        color: #ffffff;
        font-family: Arial, sans-serif;
    }
    .stButton {
        background-color: #FF9900;
        color: #FF0000;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
    }
    </style>
    """
    st.markdown(custom_dark_theme, unsafe_allow_html=True)


def main():
    set_custom_dark_theme()

    menu = ['Home', 'Contact Us', 'About']
    choice = st.sidebar.selectbox('Select a page', menu)

    if choice == 'Home':
        home_page()
    elif choice == 'Contact Us':
        contact_page()
    elif choice == 'About':
        about_page()


def home_page():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)

    st.title("Car Price Prediction")

    def prediction(horsepower, size_of_vehicle, torque, combined_fuel_economy, legroom, year, mileage):
        try:
            selected_features = np.array([[horsepower, size_of_vehicle, torque, combined_fuel_economy, legroom, year,  mileage]])
            prediction = model.predict(selected_features)
            return float(prediction[0])
        except Exception as e:
            return str(e)

    st.header("Enter Car Details")
    horsepower = st.number_input("Horsepower")
    size_of_vehicle = st.number_input("Size of vehicle")
    torque = st.number_input("Torque")
    combined_fuel_economy = st.number_input("Combined Fuel Economy")
    legroom = st.number_input("Legroom")
    year = st.slider("Year", min_value=2000, max_value=2023, step=1, value=2020)
    #daysonmarket = st.number_input("Days on Market")
    mileage = st.number_input("Mileage")
    #major_options_count = st.number_input("Major Options Count")
    #maximum_seating = st.number_input("Maximum Seating")

    if st.button("Predict", key='prediction_button'):
        result = prediction(horsepower, size_of_vehicle, torque, combined_fuel_economy, legroom, year,  mileage)
        st.subheader("Predicted Price")
        st.write("${:.2f}".format(result))

    st.text("© 2023 Car Price Prediction App")


def contact_page():
    create_table_query = ''' CREATE TABLE IF NOT EXISTS FEED(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255),
    user_email VARCHAR(255),
    inquiry_message TEXT)'''
    db_cursor.execute(create_table_query)
    db_connection.commit()

    st.header('Contact Us')
    user_name = st.text_input('Your Name')
    user_email = st.text_input('Your Email')
    inquiry_message = st.text_area('Message')

    db_cursor.execute(create_table_query)
    db_connection.commit()

    if st.button('Submit Inquiry'):
        insert_query = 'INSERT INTO FEED (user_name,user_email,inquiry_message) VALUES(%s,%s,%s)'
        data = (user_name,user_email,inquiry_message)
        db_cursor.execute(insert_query,data)
        db_connection.commit()

        if user_name and user_email and inquiry_message:
            st.success('Inquiry sent successfully!')
        else:
            st.error('Please fill in all fields.')

def about_page():
        st.title("About Data Elites")
        st.markdown(
            """
        At Data Elites, we are at the forefront of innovation in data-driven solutions, dedicated to empowering car enthusiasts and buyers with accurate and reliable information. Our flagship product, "Car's Price Prediction," is a testament to our commitment to making informed car purchasing decisions a seamless reality.
        """
        )
        st.header("Our Vision")

        st.markdown(
            """
        We envision a future where individuals can effortlessly access crucial insights that enable them to make confident decisions when buying or selling a car. In an era characterized by rapidly evolving automotive technology and market trends, our goal is to provide users with a tool that leverages the power of data to predict car prices with unmatched precision.
        """
        )

        st.header("The Power of Data-Driven Insights")

        st.markdown(
            """
        "Car's Price Prediction" harnesses the capabilities of cutting-edge machine learning and artificial intelligence technologies. By analyzing a comprehensive range of car features, historical market data, and relevant trends, our platform generates accurate price predictions. We understand that every car is unique, and our solution takes into account factors such as make, model, year, mileage, condition, and additional features to deliver customized predictions.
        """
        )

        st.header("Why Choose Car's Price Prediction?")

        st.markdown(
            """
        - **Accuracy**: Our algorithms are built upon vast datasets and refined through continuous learning, ensuring that the predictions are as close to reality as possible.
        - **Convenience**: No need for tedious manual research or relying solely on the expertise of dealers. With Car's Price Prediction, you can access price estimates from the comfort of your home.
        - **Transparency**: We believe in providing users with insights into how our predictions are generated. Our platform offers a transparent view of the data and factors that contribute to each prediction.
        - **Empowerment**: Making an informed decision empowers car buyers and sellers. Car's Price Prediction empowers users to negotiate confidently, optimize their selling strategy, or make a purchase that aligns with their budget.
        """
        )

        st.header("Our Team")

        st.markdown(
            """
        Data Elites is comprised of a diverse team of data scientists, machine learning experts, automotive enthusiasts, and software engineers. Our collective passion for technology and cars drives us to continually enhance and refine our product, ensuring that it remains at the cutting edge of data-driven innovation.
        """
        )

        st.header("Join Us on the Journey")

        st.markdown(
            """
        Whether you're a seasoned car buyer, a seller looking to optimize your pricing strategy, or simply someone who values data-backed insights, Data Elites invites you to join us on our mission. Together, let's revolutionize the way we approach car transactions, one prediction at a time.
        """
        )

                # st.markdown("*Empower Your Car Decisions with Data Elites - Where Insights Drive Confidence.*")


if __name__ == "__main__":
    main()
