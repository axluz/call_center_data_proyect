import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px



df = pd.read_csv('Call Center.csv')

#FASE 01: CLEANING THE DATA

# 1.0 identifing all of the empty cells of the data
print(df.info(),'\n')
emptyCells = df.isnull()
emptyCells = emptyCells.sum()
print(emptyCells, '\n')

# 1.1 changing the data type of a column and ignoring the empty cells
df['csat_score'] = pd.to_numeric(df['csat_score'], errors='coerce')

# 1.2 changin the data type to minutes
df['call duration in minutes'] = pd.to_numeric(df['call duration in minutes'], errors='coerce')

# 1.3 changing the data type of call_timestamp to a date data type
df['call_timestamp'] = pd.to_datetime(df['call_timestamp'], errors='coerce')

# 1.4 formating the date to day/month/year
df['call_timestamp'] = df['call_timestamp'].dt.strftime('%d/%m/%Y')

# 1.5 This is to put the new column 'Call_day' next to 'call_timestamp' column
df.insert(loc=5, column='Call_day', value=df['call_timestamp'].copy())

# 1.5 changing the 'Call_day' column to a date data type and formating the date
df['Call_day'] = pd.to_datetime(df['Call_day'],format='%d/%m/%Y', dayfirst=True, errors='coerce')

# 1.6 creating a new column that only has the day
df['Call_day'] = df['Call_day'].dt.day

# 1.7 printing the info just to check
print(df.info())

# 1.8 saving the clean csv file with a new name
df.to_csv('CallCenterDataButClean.csv', index=False)



# FASE 02: GRAPHING DATA

# 2.0 Counting the frequency of each value of the Call_day column
frequCallDay = df['Call_day'].value_counts().sort_index()

filterFrequCallDay = frequCallDay[frequCallDay.index <= 30]

# 2.1 Plot the line graph
plt.plot(filterFrequCallDay.index, filterFrequCallDay.values, marker='o')
plt.xlabel('Call Day')
plt.ylabel('Frecuency')
plt.title('FRECUENCY OF CALLS')
plt.show()

# 2.2 Counting the frquency of each value of the channel column
frequeChannel = df['channel'].value_counts()

# 2.3 plot a pie chart
frequeChannel.plot.pie(autopct='%1.1f%%')
plt.title('Doughnut (pie chart)')
plt.axis('equal')
plt.show()

# FASE 03: making choropleth map of the USA

# 3.0 first we need to creat a dictionary of the abriviation, so that plotly can read the data correctly
state_abbreviations = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# 3.1 Creating another column to map full state names to abbreviations
df['state_abbr'] = df['state'].map(state_abbreviations)

# 3.2 Generate state_counts data frame with the information that we need from the previous data frame 
state_counts = df['state_abbr'].value_counts().reset_index()
state_counts.columns = ['state', 'count']

# 3.3 Create choropleth map
fig = px.choropleth(state_counts, 
                    locations='state', 
                    locationmode='USA-states', 
                    color='count',
                    scope="usa",
                    title='Number of Calls per State in the USA',
                    color_continuous_scale='viridis',  # Choose color scale
                    labels={'count': 'Number of Calls'}
                   )
fig.show()






               
