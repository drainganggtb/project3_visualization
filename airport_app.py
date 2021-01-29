import pandas as pd

### import prepared data
df_melt = pd.read_csv("df_melt.csv")

# re-format date column to date format
if 'date' in df_melt:
    df_melt['date'] = pd.to_datetime(df_melt['date'])

df_table = df_melt.copy()
df_table['latitude'] = df_table['latitude'].map('{:,.2f}'.format)
df_table['longitude'] = df_table['longitude'].map('{:,.2f}'.format)
df_table['date'] = df_table['date'].astype(str).str.strip('T00:00:00')

airports = df_melt['airport'].unique().tolist()
#print(airports)
type_of_traffic = df_melt['type of traffic'].unique().tolist()
#print(type_of_traffic)

years = df_melt['date'].dt.year.unique().tolist()
#print(years)

months = df_melt['date'].dt.month.unique().tolist()
months=sorted(months)
#print(months)

months_alpha = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Des"]


