import numpy as np

# --------------- S1 - Medal Tally ------------------

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    medal_tally.reset_index(inplace=True)

    medal_tally['Total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    return medal_tally

def year_country_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0,'Overall')

    return years, countries

def fetch_tally(df, yr, country):
    flag = 0
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    
    if yr=='Overall' and country=='Overall':
        temp = medal_df
    if yr=='Overall' and country!='Overall':
        flag = 1
        temp = medal_df[medal_df['region'] == country]
    if yr!='Overall' and country=='Overall':
        temp = medal_df[medal_df['Year'] == int(yr)]
    if yr!='Overall' and country!='Overall':
        temp = medal_df[(medal_df['Year'] == int(yr)) & (medal_df['region'] == country)]
    
    if flag == 1:   
        t = temp.groupby('Year').sum(numeric_only=True)[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        t = temp.groupby('region').sum(numeric_only=True)[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    t['Total'] = t['Gold'] + t['Silver'] + t['Bronze']
    
    return t

# --------------- S2 - Olympics at a glance ------------------

def olympics_over_time(df):
    #Participating countries over the years
    cot = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')
    cot.rename(columns={'index':'Year','Year': 'No. of Countries'},inplace=True)
    
    #Events over the years
    eot = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
    eot.rename(columns={'index':'Year','Year': 'No. of Events'},inplace=True)
    
    #Athletes over the years
    at = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('index')
    at.rename(columns={'index':'Year','Year': 'No. of Athletes'},inplace=True)

    return cot, eot, at

# Get list of top 10 athletes across sports
def get_top_10(df, sport):
    temp = df.dropna(subset = ["Medal"])
    
    if sport != 'Overall':
        temp = temp[temp['Sport'] == sport]
        
    t = temp['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[['index','Name_x','Sex', 'region']].drop_duplicates()
    t.rename(columns={'index':'Name', 'Name_x':'Medals'},inplace=True)
    
    return t

# --------------- S3 - Country-wise analysis ------------------

# Get medals list for a country
def country_event_heatmap(df, country):
    # Remove the names (entire row) which did not win medals
    cwp = df.dropna(subset=['Medal'])

    # Now, we need to tackle the problem which we faced earlier as well
    # - a team-sport is considered as a single medal for the country
    cwp = cwp.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    ip = cwp[cwp['region'] == country]
    fip = ip.groupby('Year').count()['Medal'].reset_index()

    return fip

# Return df to plot country's performance over time
def plot_performance(df, country):
    temp = df.dropna(subset=['Medal'])
    temp = temp.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    temp = temp[temp['region'] == country]
    temp = temp.groupby('Year').count()['Medal'].reset_index()
    temp['Year'] = temp['Year'].astype(int)
    
    return temp

# Plot which sports a country has won most medals in
def country_sport_heatmap(df, country):
    csp = df.dropna(subset=['Medal'])
    csp = csp.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    csp = csp[csp['region'] == country]

    csp = csp.groupby('Sport').count()['Medal'].reset_index().sort_values('Medal',ascending=False)

    return csp


# Get top 10 athletes for a country
def country_top_performers(df, country):
    temp = df.dropna(subset=['Medal'])
    temp = temp[temp['region'] == country]

    temp = temp.groupby('Name').count()['Medal'].reset_index().sort_values('Medal',ascending=False).head(10)
    # temp.rename(columns={'Medal':'Medals'},inplace=True)
    return temp

# Medal tally of a country over the years
def country_medal_tally(df, country):
    # Count no. of gold, silver and bronze medals for a given country
    temp = df.dropna(subset=['Medal'])
    temp = temp[temp['region'] == country]
    temp = temp.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    # temp = temp.groupby('Year').count()['Medal'].reset_index()
    temp = temp.groupby('Year').sum()[['Gold','Silver','Bronze']].reset_index()
    gold = temp['Gold'].sum()
    silver = temp['Silver'].sum()
    bronze = temp['Bronze'].sum()

    return gold, silver, bronze

# --------------- S4 - Athlete-wise analysis ------------------
def men_women(df, sport):
    athletes = df.drop_duplicates(subset=['Name','region'])

    if sport != 'Overall':
        athletes = athletes[athletes['Sport'] == sport]
        men = athletes[athletes['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
        women = athletes[athletes['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    
        final = men.merge(women, on='Year', how='left')
        final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
        return final 
    else:
        men = athletes[athletes['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
        women = athletes[athletes['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

        final = men.merge(women, on='Year', how='left')
        final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
        return final
