
# import pandas
import pandas as pd

# read the data into your workspace
ba_data = pd.read_csv("datasets/breath_alcohol_ames.csv")

# quickly inspect the data
print(ba_data.head())

# obtain counts for each year 
ba_year = ba_data['year'].value_counts()
ba_year

# Alternative method:
# ba_data.set_index(["year", "month", "day", "hour", "location", "gender"]).count(level="year")

# use value_counts to tally up the totals for each department
pds = ba_data['location'].value_counts()
pds

# Alternative method:
# ba_data.set_index(["year", "location", "gender"]).count(level="location")


%matplotlib inline

# count by hour and arrange by descending frequency
# hourly = ba_data.groupby(['hour'])['location'].count().sort_values(ascending=False)
hourly = ba_data.groupby(['hour']).size()
print(len(hourly))

hourly.plot.bar(x='hour') # TODO this plot is not in decending frequency


# count by month and arrange by descending frequency
# monthly = ba_data.groupby(['month'])['location'].count().sort_values(ascending=False)
monthly = ba_data.groupby(['month']).size()
print(len(monthly))

# use plot.bar to make the appropriate bar chart
monthly.plot.bar(x='month')

# count by gender (may not be relevent in this work flow)
counts_gender = ba_data['gender'].value_counts()

# create a dataset with no NAs in gender 
gen = ba_data.dropna(subset=['gender'])

# create a mean test result variable
mean_bas = gen.assign(meanRes=(gen.Res1+gen.Res2)/2)
# gen['meanRes'] = (gen.Res1+gen.Res2)/2

# create side-by-side boxplots to compare the mean blood alcohol levels of men and women
mean_bas.boxplot(['meanRes'], by = 'gender')


# Filter the data
duis = ba_data[(ba_data.Res1 > 0.08) | (ba_data.Res2 > 0.08)]

# proportion of tests that would have resulted in a DUI
p_dui = duis.shape[0] / ba_data.shape[0]
p_dui

# Create date variable
# ba_data = ba_data.assign(date = pd.to_datetime(ba_data[['year', 'month', 'day']]))
ba_data['date'] = pd.to_datetime(ba_data[['year', 'month', 'day']])

# Create a week variable
# ba_data = ba_data.assign(week= ba_data['date'].dt.week)
ba_data['week'] = ba_data['date'].dt.week

# Check your work
ba_data.head()


# create the weekly data set (most similar to original project)
# weekly1 = ba_data[['year', 'week', 'gender']]
# weekly1.groupby(['week','year']).count().unstack().plot()

# choose the variables of interest, count 
timeline = ba_data.groupby(['week','year']).count()['Res1']

# unstack and plot
timeline.unstack().plot(title='VEISHEA DUIs', legend=True)
print(len(timeline))




# ## Run this code to create the plot 
# ba_data.groupby(['week','year']).count()['Res1'].unstack().plot(legend=True)

# veishea= ba_data.loc[(ba_data.week < 20) & (ba_data.week > 10)]

# veishea.groupby(['week','year']).count()['Res1'].unstack().plot(title='VEISHEA Weeks',legend=True) 

## Was it right to permanently cancel VEISHEA? TRUE or FALSE?  
canceling_VEISHEA_was_right = False

