# SQLAlchemy

Climate analysis on Honolulu, Hawaii.    

## Climate Analysis and Exploration

I began using Python and SQLAlchemy to do basic climate analysis and data exploration of my climate database. All of the following analysis was completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* To start I chose a start date and end date for my trip. 

* I used SQLAlchemy `create_engine` to connect to your sqlite database.

* Then I used SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* A query I designed was utilized to retrieve the last 12 months of precipitation data.

* Then I selected only the `date` and `prcp` values.

* Loading the query results into a Pandas DataFrame and set the index to the date column was the next step.

* Next I sorted the DataFrame values by `date`.

* Plotting the results using the DataFrame `plot` method.

* Pandas was used to print the summary statistics for the precipitation data.

### Station Analysis

* I then designed a query to calculate the total number of stations.

* Designing a query to find the most active stations followed in order to find:

  * List the stations and observation counts in descending order.

  * Which station has the highest number of observations?

* Finally I designed a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filtered by the station with the highest number of observations.

  * Plotted the results as a histogram with `bins=12`.


- - -

## Step 2 - Climate App

Now that the initial analysis was complete, I designed a Flask API based on the queries that I just developed.

* Flask was used to create my routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * I converted the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Then I returned the JSON representation of my dictionary.

* `/api/v1.0/stations`

  * A JSON list of stations from the dataset was then returned.

* `/api/v1.0/tobs`
  * I queried the dates and temperature observations of the most active station for the last year of data.
  
  * Returning a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Finally I returned a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, I calculated `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, I calculated the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

- - -



### Copyright

Trilogy Education Services © 2020. All Rights Reserved.
