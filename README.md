# NEM Data Challenge

## 1st phase guidelines

The participant will receive two files. The first one is a “csv” with 5 columns (“asset”, “date”, “time”, “variable” and “value”). The file contains the speed, velocity, temperature and pressure sensor measurements associated to the different wind turbines with a high measurement frequency (a measurement per second).

* The column “asset” contains the asset’s identification to which the measurement is associated.
* The date and time of each measurement is registered in two columns. The “date” one contains the date in the format “yyyy-mm-dd”, whereas the “time” one contains the time in the format “hh:mm:ss”
* The “variable” column registers the sensor’s identification of each asset and the value of the measurement obtained by the mentioned sensor is contained in the column “value”

Each sensor’s identifier is registered in a different way in each asset. The second file is an “xml” which contains the unification of each sensor’s identifiers among the different assets.

The participant will be asked to process that file and as a result, generate a new “csv” file. The file will have to contain a “timestamp” column with the date and time of each register in unix and all the values of each of the registered sensors in different columns.

The heading of each column will have to be the sensor’s unified identifier. The file will contain a row every ten minutes and the average of the registered measurements in those 10 minutes in each one of the cells. The timestamp associated to each interval will have to be the superior limit of each interval.

Once the data is processed, the participant will have to make a descriptive analysis of the quality of the data, together with distributions or relations among the different variables. Once the analysis is carried out, the participant will have to generate a report of no more than 5 pages where he/she will have to register in a visual way that information the participant considers most relevant.

The outcome of this test will be the source code used for the transformation of the files, the resultant “csv” file and a PDF with the report including the visual description of the information contained in the latter mentioned files. The objective of this test is to assess the participant’s capacity in the areas of data processing (ETL processes), data analysis (statistics and data mining) and information visualisation (visual analytics).

## 2nd phase guidelines

NEM Solutions will provide the candidates with two data sets:
* Historical data set: to be used by the candidates to define, train and test their proposals.
* Evaluation data set: to be used by NEM Solutions to evaluate the goodness of the candidates’ proposals.

**Historical data set description**

The historical data set is formed by two types of files: files with raw information from the assets and files with weather forecasting. Both types of files will contain information corresponding to one month. The historical data set will provide 5 months of data (April - August 2015), and hence, five raw information files and 5 weather forecasting files will be provided in separate folders.

**Raw information from the assets**

The raw information data will be provided as CSV files of approximately 10GB each in “vertical” format (asset, date, time, variable, value) with a secundal data frequency, and will contain the raw data extracted from five wind turbines belonging to the same wind farm. Each file will contain information from the five assets for a period of one month.

As in the 1st phase, an XML file will be provided with the variables mapping.

The historical data set is similar to the one the candidates were asked to process in the 1st phase. Candidates will likely use the solution proposed during the 1st phase to “horizontalize” the dataset calculating ten-minute averages. Since the volume of data in the 2nd phase is larger, those candidates having troubles to process the data could contact NEM to ask for an already daily processed data set. This additional dataset will not be available until one week after the 2nd phase starting day.

**Weather forecasting**

The weather forecasting data will be provided as CSV files in “horizontal” format (asset, timestamp, range, wind speed, ambient temperature) with a hourly data frequency. The timestamp column indicates the time at which the weather forecasting was obtained in UNIX time. The range column indicates the forecasting time as the number of seconds from the timestamp.

**Evaluation data set description**

The evaluation data set is formed by several sets of two files corresponding to different evaluation journeys:
* A CSV file containing 10-minute averages of the raw information in “horizontal” format, extracted from the five assets during a single journey (24 hours).
* A CSV file containing hourly weather forecasting for the next 7 days to the journey.

The candidates will be asked to make use of the evaluation data set to generate the deliverables for their submission to NEM.

**DELIVERABLES**

The candidates should develop a module capable of estimating the energy a wind turbine will produce during the next 7 days. The candidates should deliver the following items before the deadline:
* Energy predictions: for each journey in the evaluation data set, candidates should provide a CSV file in “vertical” format (asset, range, energy production), with the 10-minute predicted energy production of the five assets during the next 7 days.
* Source code: the source code implementing the module.
* Brief report: a PDF file, no longer than 5 pages, describing the proposed approach.

Note: if the candidates follow several approaches to predict the 10-minute energy production, they can send the “Energy predictions” for each approach in separate files, and describe the approaches in the “Brief report”.

**EVALUATION CRITERIA**

The candidates will be evaluated according to the following two criteria:
1. Prediction accuracy: several evaluation metrics such as the sum of squared residuals, the coefficient of determination (R2), etc. will be calculated on the Energy predictions. To that effect, NEM disposes of the actual Energy production measurements corresponding to the Evaluation data set. The actual Energy production measurements will not by any means be accessible to the candidates until the second phase is over.
2. Clarity of exposition: the capacity of the candidate to clearly explain the proposed approach in the Brief report.

<p align="center">
  <img src="https://github.com/ubarredo/NEM-DataChallenge/blob/master/reports/time_series.png">
  <img src="https://github.com/ubarredo/NEM-DataChallenge/blob/master/reports/distributions.png">
  <img src="https://github.com/ubarredo/NEM-DataChallenge/blob/master/reports/principal_components.png">
  <img src="https://github.com/ubarredo/NEM-DataChallenge/blob/master/reports/correlation_matrix.png">
  <img src="https://github.com/ubarredo/NEM-DataChallenge/blob/master/reports/top_correlations.png">
</p>