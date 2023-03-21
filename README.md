# Hotel Analysis / Dashboard
## IRONHACK FINAL PROJECT

These last years are really interesting for analyzing a business performance as the environment has significantly changed. For this reason, my final project is a business analysis of a hotel located in Spain. 
The period I decided to collect the data is from 2019 to 2022. I have chosen this period because I wanted to know how the origin of the guests that receive this specific hotel changed through these years and how it affected to their income.

### Extraction
Firstly, I collected monthly data making requests through an API. 
Once I got all the information I needed for my analysis, I visualized these json files in Pandas and started to anonymize, clean and transform the data. After that, I concatenated month files creating a unique csv file for each year.

### Cleaning and transformation
As the main idea is to create a dashboard in which the user can visualize the data in a simple and good understanding way, once I collected all the data, I decided to create different tables with important information which will help later on when I start working with Power BI.

I have done all the cleaning via an executable Python file in which I created and determined all the functions I would like to use and a Jupyter Notebook file in which I applied these functions.

I created a unique table called 'reservations' in which I concatenated the whole period and used this DataFrame for cleaning data. 
After that, I could detect some outliers and anomalies which I could fix properly so as to not impact unfavourably to the data.

At the end of this process I had the following tables:
- **Reservations:** reservation_id, country_code, arrival, departure, accommodation_amount, board_amount, service_amount, total_amount, status, board, room_id, room_type_id, room_type_name, adult, booker_name, nights.
- **Rooms:** room_code, room_type, room_type_name.
- **Continents:** country, country_code, alpha-3, continent.
- **Calendar:** date, day, month, year, weekday, weekday_number, month_name, week.
- **Occupancy:** date, reservation_id, country_code, status, board, room_code, adult, booker_name, nights. 

### Power BI
I imported all the csv files and created relations between all these tables in order to be able to filter the information as easy as I could and started creating my dashboard. 

#### Overview
This page is showing an overview of the data in terms of general income, total rooms, opening days... and all the data and useful measures to know the status of the hotel filtering by the period of time you decide.

![OverviewGIF](https://github.com/lauurasarabia/Hotel_Dashboard/blob/main/images/GIF_Overview.gif?raw=true)


#### Customer Origin -> Map
In this map, you as a user, have the possibility to filter by continent (or country if you need to be more specific) and year (and/or month) in order to see how the provenience of your guests has changed during these past years and which is the amount they have provided you. 

![MapGIF](https://github.com/lauurasarabia/Hotel_Dashboard/blob/main/images/GIF_Map.gif?raw=true)

#### KPI
KPIs are important because they give you the key to compare against your current performance. KPIs clearly illustrate if you really are reaching your goals. Implementing them in your company means you can set goals, you can set a strategy to reach your goals, and above all, you can evaluate your performance along the way. 
For that reason, I have built this KPI page in which the user can find a detail of how is the performance going. If it is not going well, he may find the reason why in this page. 

![KPIGIF](https://github.com/lauurasarabia/Hotel_Dashboard/blob/main/images/GIF_KPI.gif?raw=true)

#### Rooms
It shows different KPIs in relation to the type of room and the accommodation amount divided also by type of room. 


![Rooms](https://github.com/lauurasarabia/Hotel_Dashboard/blob/main/images/Screenshot_rooms.png?raw=true)

#### Occupancy vs Cancellation
I have decided to create this page so as to be able to see the difference between the occupancy rate and cancellation rate in these last 4 years, as from my point of view, it is really important to analyze how the market has changed because of external matters and how the hotel has confront this. 

![Occupancyvscancellation](https://github.com/lauurasarabia/Hotel_Dashboard/blob/main/images/Screenshot_occupancy_cancel.png?raw=true)

#### Prediction
In this last page, I created a visualization in relation to the occupancy rate prediction for the following 6 months. I have done this prediction in Python using Gradient Boosting, a machine learning model technique. 

![Prediction](https://github.com/lauurasarabia/Hotel_Dashboard/blob/main/images/GIF_prediction.gif?raw=true)


### Features
* API
* Python
* Jupyter Notebook
* Pandas
* Power BI
* Machine Learning
