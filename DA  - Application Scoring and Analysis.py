#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# Load data into DataFrame objects - Wczytaj dane do obiektów DataFrame
applications = pd.read_csv(r'C:\Users\Acer\Desktop\DA\PYTHON\ZADANIE_3\applications.csv')
industries = pd.read_csv(r'C:\Users\Acer\Desktop\DA\PYTHON\ZADANIE_3\industries.csv')


# In[3]:


# Remove duplicate data based on 'applicant_id' - Usuń zduplikowane dane applicant_id
applications = applications.drop_duplicates(subset='applicant_id')


# In[4]:


# Fill missing values in the 'External Rating' field with zeros - Uzupełnij brakujące wartości zerami w polu 'External Rating'
applications['External Rating'] = applications['External Rating'].fillna(0)


# In[5]:


# Fill missing values in the 'Education level' field with the text "Secondary" - Uzupełnij brakujące wartości w polu 'Education level' tekstem "Średnie"
applications['Education level'] = applications['Education level'].fillna('Średnie')


# In[6]:


# Add industry scores to the DataFrame - Dodaj punkty branż do DataFrame
applications = applications.merge(industries, on='Industry', how='left')


# In[8]:


# Calculate the application score - Oblicz ocenę aplikacji

# Replace missing values in the 'Location' column with an empty string - as 'Location' had NaN values treated as float, making 'in' operation impossible - Zastąpienie brakujących wartości w kolumnie 'Location' pustym ciągiem znaków - poniewaz 'Location' znajdwaly sie warosci NaN traktowane jako float unimozliwiajace zastosowanie'in'
applications['Location'] = applications['Location'].fillna('')

def calculate_score(row):
    score = 0

    # Missing 'Amount' or 'External Rating' = 0 - Brak wartości 'Amount' lub 'External Rating' = 0
    if pd.isna(row['Amount']) or row['External Rating'] == 0:
        return 0
    
    # Age between 35 and 55 years - Wiek od 35 do 55 lat
    if 35 <= row['Age'] <= 55:
        score += 20
    
    # Application made on a weekday, not on the weekend - Aplikacja złożona w tygodniu, poza weekendem
    applied_at = pd.to_datetime(row['Applied at'], dayfirst=True)
    if applied_at.weekday() < 5:
        score += 20
    
    # Candidate is married - Kandydat pozostaje w związku małżeńskim
    if row['Marital status'] == 'Married':
        score += 20
    
    # Candidate lives in Warsaw or the Masovian Voivodeship - Kandydat mieszka w Warszawie lub województwie mazowieckim
    if 'Warszawa' in row['Location'] or 'mazowieckie' in row['Location']:
        score += 10
    
    # Add Score from the industries table - Dodaj Score z tabeli industries
    score += row['Score']
    
    # External Rating >= 7 - External Rating >= 7
    if row['External Rating'] >= 7:
        score += 20
    
    # External Rating <= 2 - External Rating <= 2
    if row['External Rating'] <= 2:
        score -= 20
    
    return score

applications['Score'] = applications.apply(calculate_score, axis=1)


# In[12]:


# Keep only applications with a score greater than zero - Pozostaw tylko aplikacje z oceną większą od zera
accepted_applications = applications[applications['Score'] > 0].copy()


# In[13]:


# Group data by the week in which the application was submitted and calculate the average score of accepted applications - Pogrupuj dane według tygodnia, w którym złożono aplikację i oblicz średnią ocenę zaakceptowanych aplikacji
accepted_applications['Applied at'] = pd.to_datetime(accepted_applications['Applied at'], dayfirst=True)
accepted_applications['Week'] = accepted_applications['Applied at'].apply(lambda x: x.isocalendar()[1])


# In[14]:


# Plot the average score of accepted applications for each week - Wykres średniej ocen zaakceptowanych aplikacji w każdym tygodniu
plt.figure(figsize=(10, 6))
weekly_avg_scores.plot(kind='bar')
plt.title('Średnia ocen zaakceptowanych aplikacji w każdym tygodniu')
plt.xlabel('Tydzień')
plt.ylabel('Średnia ocena')
plt.show()


# In[ ]:




