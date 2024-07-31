
# NY_Vacations Project: Hotel Price Analysis and Prediction


Welcome to our Data Project repository! This project is part of the Fundamentals of Data Science course and focuses on analyzing and predicting hotel prices using data from Booking.com and Expedia.com.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Collection](#data-collection)
3. [Data Exploration and Preprocessing](#data-exploration-and-preprocessing)
4. [Price Prediction Models](#price-prediction-models)
5. [Price Difference Analysis](#price-difference-analysis)
6. [Reverse Engineering Sorting Algorithms](#reverse-engineering-sorting-algorithms)
7. [Results and Findings](#results-and-findings)
8. [Contributors](#contributors)

## Project Overview
In this project, we explore hotel price behaviors on Booking.com and Expedia.com. We aim to:
- Scrape hotel price data.
- Explore and preprocess the data.
- Build and evaluate machine learning models to predict hotel prices.
- Analyze price differences between Booking.com and Expedia.com.
- Reverse engineer the sorting algorithms used by these websites.

## Data Collection
### Web Scraping
We used Python libraries like `Selenium` and `BeautifulSoup` to scrape hotel search results from Booking.com and Expedia.com. Our scraping criteria included:
- Location: New York
- Search Parameters: Various combinations of TTT (Time to Travel) and LOS (Length of Stay)
- Dates: Multiple snapshot dates to capture data diversity

We collected data on various attributes, including hotel name, rating, price, distance from city center, room type, cancellation policy, and more. 

## Data Exploration and Preprocessing
### Exploratory Data Analysis (EDA)
We performed EDA to understand the distributions and relationships within our data:
- Distributions of review counts, ratings, and prices
- Identification and handling of outliers
- Conversion of ordinal and nominal variables into numerical formats using techniques like one-hot encoding

### Data Cleaning
We cleaned the data by:
- Removing outliers using the Tukey method
- Handling missing values and inconsistent data entries
- Normalizing and scaling the features for better model performance

## Price Prediction Models
We implemented several regression algorithms to predict hotel prices based on our collected data:
- Linear Regression
- Decision Tree Regressor
- Gaussian Process Regressor
- Random forest Regressor
- SVR
- Neural networks Regressor
  
We split our data into training and testing sets, experimented with various hyperparameters, and evaluated model performance using metrics such as MAE, MSE, RMSE, and R².

## Price Difference Analysis
We built models to predict price differences between Booking.com and Expedia.com for identical hotel bookings. This involved:
- Identifying common hotels between the two platforms
- Using features from both websites to train the models
- Evaluating the models based on prediction accuracy and error metrics

## Reverse Engineering Sorting Algorithms
To understand how Booking.com and Expedia.com rank hotels in their search results, we:
- Developed algorithms to replicate the sorting mechanism
- Used machine learning techniques to analyze the impact of different features on hotel rankings
- Measured the algorithm's performance by comparing our predicted rankings with the actual ones

## Results and Findings
Our analysis provided insights into:
- Key factors influencing hotel prices
- Differences in pricing strategies between Booking.com and Expedia.com
- Effectiveness of various regression models in predicting prices
- Sorting criteria used by online travel agencies



## Contributors
- [Omri5790](https://github.com/Omri5790)
- [ronelis199](https://github.com/ronelis199)
- [liavermias](https://github.com/liavermias)


We hope this project provides valuable insights into hotel pricing dynamics and helps you understand the machine learning techniques used in this analysis. Feel free to explore the repository and reach out with any questions or feedback!



