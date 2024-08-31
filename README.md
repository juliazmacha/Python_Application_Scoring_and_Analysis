# Python_Application_Scoring_and_Analysis
This Python script processes application data to calculate and analyze application scores based on various criteria. It reads data from CSV files, cleans and transforms the data, calculates scores for each application, and visualizes the average scores on a weekly basis

# Requirements
- Pandas
- NumPy
- Matplotlib

# Files
applications.csv: Contains data about applications including applicant details and external ratings.
industries.csv: Contains industry-specific scores to be merged with application data.

# Code Walkthrough
## 1. Data Loading
The script loads data from two CSV files into Pandas DataFrames:

applications = pd.read_csv(r'C:\Users\Acer\Desktop\DA\PYTHON\ZADANIE_3\applications.csv')
industries = pd.read_csv(r'C:\Users\Acer\Desktop\DA\PYTHON\ZADANIE_3\industries.csv')

## 2. Data Cleaning
Remove Duplicates: Removes duplicate rows based on the applicant_id column.

applications = applications.drop_duplicates(subset='applicant_id')

### Fill Missing Values:

Replace missing values in the External Rating column with zeros.
Replace missing values in the Education level column with "Secondary".

applications['External Rating'] = applications['External Rating'].fillna(0)
applications['Education level'] = applications['Education level'].fillna('Secondary')

## 3. Data Merging
Add industry scores to the applications DataFrame by merging it with the industries DataFrame:

applications = applications.merge(industries, on='Industry', how='left')

## 4. Score Calculation
A custom function calculate_score computes a score for each application based on various criteria:

- Age between 35 and 55 years
- Application made on a weekday
- Candidate is married
- Candidate lives in Warsaw or the Masovian Voivodeship
- Add industry score
- Adjust score based on External Rating

def calculate_score(row):
    # Score calculation logic
    ...
Apply this function to each row in the DataFrame:
applications['Score'] = applications.apply(calculate_score, axis=1)

## 5. Filter Accepted Applications
Filter the applications to keep only those with a score greater than zero:
accepted_applications = applications[applications['Score'] > 0].copy()

## 6. Weekly Average Score Calculation
Convert the Applied at column to datetime and extract the week number:
accepted_applications['Applied at'] = pd.to_datetime(accepted_applications['Applied at'], dayfirst=True)
accepted_applications['Week'] = accepted_applications['Applied at'].apply(lambda x: x.isocalendar()[1])

Group the data by week and calculate the average score:
weekly_avg_scores = accepted_applications.groupby('Week')['Score'].mean()

## 7. Visualization
Plot the average scores of accepted applications for each week using Matplotlib:

plt.figure(figsize=(10, 6))
weekly_avg_scores.plot(kind='bar')
plt.title('Average Scores of Accepted Applications Each Week')
plt.xlabel('Week')
plt.ylabel('Average Score')
plt.show()
