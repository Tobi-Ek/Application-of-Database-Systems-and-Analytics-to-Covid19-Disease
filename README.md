# Application of Database Systems and Analytics to Covid19 Disease

The Novel Coronavirus (Covid19), a virus that has effected approximately 3 Million people across the world has been analysed in this project.

- The analysis was performed by gathering related datasets of four (4) different formats: .xml, .json, .csv and web scrapped data.
- **Pre-processing**: web-scrapping data off the two websites, extracted XML data, stored these data into mongoDB, cleaned and saved the processed data into PostgreSQL
  - https://www.worldometers.info/coronavirus/
  - https://data.medicare.gov/widgets/xubh-q36u
  - CSV Dataset: https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset
  - XML dataset: https://opendata.ecdc.europa.eu/covid19/casedistribution/xml/
  - JSON dataset: https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
-	After fetching, pre-processing and combining all these datasets, visualization on the Covid19 data was carried out and a forecast on new cases and deaths was predicted using Auto-ARIMA model.
- The visualizationsprovides understanding of the patterns of the impact of Covid-19 outbreak over different Countries, number of deaths, number of people recovered, and regions highly effected. 

