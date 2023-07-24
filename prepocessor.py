import pandas as pd

# Preprocess the data that we did on the Jupyter notebook
def preprocess(df, region):
    # Take only summer olympics data
    df = df[df['Season'] == 'Summer']
    # Merge it with region data to get region names
    df = df.merge(region,on='NOC',how='left')
    # Drop the duplicates
    df.drop_duplicates(inplace=True)
    # One hot encode the medals, i.e., separate columns for each medal
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)

    return df
