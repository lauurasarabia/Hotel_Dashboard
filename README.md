# IRONHACK FINAL PROJECT
## Hotel Dashboard Analysis
These last years are really interesting for analyzing a business performance as the environment has significantly changed. For this reason, my final project is a business analysis of a hotel located in Spain. 
The period I decided to collect the data is from 2019 to 2022.

### Extraction
Firstly, I collected monthly data making requests through an API. 
Once I got all the information I needed for my analysis, I visualized these json files in Pandas and started to anonymize, clean and transform the data. After that, I concatenated month files creating a unique csv file for each year.

### Cleaning and transformation
As the main idea is to create a dashboard in which the user can visualize the data in a simple and good understanding way, once I collected all the data, I decided to create different tables with important information which will help later on when I start working with Power BI.

I have done all the cleaning via an executable Python file in which I created and determined all the functions I would like to use and a Jupyter Notebook file.

I created a unique table called 'reservations' in which I concatenated the whole period and used this DataFrame for cleaning data. 
After that, I could detect some outliers and anomalies which I could fix properly so as to not impact unfavourably to the data.

At the end of this process I created the following tables:
- ***Reservations:*** reservation_id, country_code, arrival, departure, accommodation_amount, board_amount, service_amount, total_amount, status, board, room_id, room_type_id, room_type_name, adult, booker_name, nights.
- ***Rooms:*** room_code, room_type, room_type_name.
- ***Continents:*** country, country_code, alpha-3, continent.
- ***Calendar:*** date, day, month, year, weekday, weekday_number, month_name, week.
- ***Occupancy:*** date, reservation_id, country_code, status, board, room_code, adult, booker_name, nights. 


### Features
* API
* Python
* Jupyter Notebook
* Pandas
* Power BI
* Machine Learning
