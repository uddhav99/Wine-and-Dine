# Wine and Dine
A project which scrapes data from the Yelp and Zomato API's and creates interactive visualisations such as choropleth maps, scatter plots, among others. You can change the location to the city of your liking and see some the popular trends in the food industry! 

## Local Usage 
After cloning the repository, follow these steps to get it running yourself -:

Clone the repo and run the python scripts.
```
$ git clone https://github.com/uddhav99/Wine-and-Dine.git
$ cd Wine-and-Dine
```
If you want to change the location of the city (default set to New York City), please make sure you have SQLite installed on your device.
- delete restaurants.sqlite
- create own sqlite database according to previous format
- open yelp_api.py
- go to line 66 and change 'NYC' to city of your liking and re run the python script
- open zomato_api.py
- go to line 68 and change coordinates to city of your liking and re run python script
- then re run visualisations_uddhav.py
## Technologies
Python, SQLite, HTML

## Report 
Read the SI_206_Final_Project_Report.pdf to know more about the goals, challenges, accomplishments of this project. 

## Team
- Uddhav Bhagat
- Alexander Cotignola
