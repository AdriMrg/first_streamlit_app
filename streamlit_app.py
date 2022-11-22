import streamlit 
import pandas
import snowflake.connector

fruit_choice_query = streamlit.text_input('What fruit would you like information about from SNOWFLAKE?','')
streamlit.write('The user entered ', fruit_choice_query)


#SNOWFLAKE
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("Select * from fruit_load_list where fruit_name = " + fruit_choice_query)
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list")
streamlit.dataframe(my_data_rows)

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#pick list
fruits_selected = streamlit.multiselect("Pick some fruit:", list(my_fruit_list.index), ['Cantaloupe', 'Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# ajoute un champs de saisie 
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#Appel l'API fruityvice avec la saisie en parametre
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# Formate le json 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Affiche le Json dans un joli tableau
streamlit.dataframe(fruityvice_normalized)
