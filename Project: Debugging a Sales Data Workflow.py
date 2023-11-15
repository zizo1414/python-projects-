import pandas as pd
import numpy as np

def load_and_check():
    data = pd.read_csv('sales.csv')  
    
    # Step 1: Check the loaded data
    
    # Correct the string to a number
    if data.shape[1] != 17:
        print("Please check that the data was loaded properly, different shape was expected.")
    else:
        print("Data loaded succesfully.")

    # Step 2: Data integrity check
    grouped_data = data.groupby(['Date'])['Total'].agg(['mean', 'std'])
    grouped_data['threshold'] = 3 * grouped_data['std']
    grouped_data['max'] = grouped_data['mean'] + grouped_data.threshold
    grouped_data['min'] = grouped_data[['mean', 'threshold']].apply(lambda row: max(0, row['mean'] - row['threshold']), axis=1)
    data = pd.merge(data, grouped_data, on='Date', how='left')
    data['Condition_1'] = (data['Total'] >= data['min']) & (data['Total'] <= data['max'])
    data['Condition_1'].fillna(False, inplace=True)

    data['Condition_2'] = round(data['Quantity'] * data['Unit price'] + data['Tax'], 1) == round(data['Total'], 1)
    
    # Do any necessary changes below this comment and before the if statement
    
    # Create a new column for calculated tax
    data['Tax_calculated'] = data['Total'] - data['Quantity'] * data['Unit price']
    
    # Create a new condition for the integrity check
    data['Condition_3'] = round(data['Tax_calculated'], 1) == round(data['Quantity'] * data['Unit price'] * 0.05, 1)
    
    # Add the new condition to the if statement using logic operators
    if (data['Condition_1'].sum() != data.shape[0])&((data['Condition_2'].sum() != data.shape[0])|(data['Condition_3'].sum() != data.shape[0])):
        print("Something fishy is going on with the data! Better check the pipeline!")
    else: 
        print("Data integrity check was succesful!")
        
    return data

data = load_and_check()
