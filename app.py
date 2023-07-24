import streamlit as st
import pandas as pd
import prepocessor, helper
import plotly.express as px
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region = pd.read_csv('noc_regions.csv')

df = prepocessor.preprocess(df, region)

# Include Olympics logo- full width, on top
st.image('olympics.png')



st.sidebar.title('Summer Olympics')
menu = st.sidebar.radio(
    'Select an option:',
    ('At a Glance', 'Medal Tally', 'Country-wise analysis', 'Athlete analysis')
)

if menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, countries = helper.year_country_list(df)

    yr = st.sidebar.selectbox('Select Year', years)
    country = st.sidebar.selectbox('Select Country', countries)
    medal_tally = helper.fetch_tally(df, yr, country)
    
    if yr == 'Overall' and country == 'Overall':
        st.title('Overall Tally')
    if yr != 'Overall' and country == 'Overall':
        st.title('Tally in ' + str(yr) + ' Olympics')
    if yr == 'Overall' and country != 'Overall':
        st.title('Overall Tally for ' + country)
    if yr != 'Overall' and country != 'Overall':
        st.title('Tally for ' + country + ' in ' + str(yr) + ' Olympics')
    
    st.table(medal_tally)

if menu == 'At a Glance':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('At a Glance')

    c1, c2, c3 = st.columns(3)
    with c1:
        st.header('Editions')
        st.title(editions)
    with c2:
        st.header('Host Cities')
        st.title(cities)
    with c3:
        st.header('Sports')
        st.title(sports)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.header('Sporting Events')
        st.title(events)
    with c2:
        st.header('Participating Nations')
        st.title(nations)
    with c3:
        st.header('Athletes')
        st.title(athletes)

    cot, eot, at = helper.olympics_over_time(df)
    # Participating Countries over the years
    st.title('Participating Countries over the years')
    fig = px.line(cot, x='Year', y='No. of Countries')
    st.plotly_chart(fig)

    # Events over the years
    st.title('Events over the years')
    fig = px.line(eot, x='Year', y='No. of Events')
    st.plotly_chart(fig)

    # Athletes over the years
    st.title('Athletes over the years')
    fig = px.line(at, x='Year', y='No. of Athletes')
    st.plotly_chart(fig)

    # List of most successful athletes across all olympics
    st.title('Top 10 athletes across sports')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.header('Select a sport:')
    sport = st.selectbox('', sport_list)
    alist = helper.get_top_10(df, sport)
    st.table(alist)

if menu == 'Country-wise analysis':
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country = st.sidebar.selectbox('', country_list)
    
    st.title(country + ' Over The Years')

    # Show total gold, silver and bronze for the country
    gold, silver, bronze = helper.country_medal_tally(df, country)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.header('Gold:')
        st.title(gold)
    with c2:
        st.header('Silver:')
        st.title(silver)
    with c3:
        st.header('Bronze:')
        st.title(bronze)

    st.header('Top 10 athletes')
    st.table(helper.country_top_performers(df, country))

    country_df = helper.country_event_heatmap(df, country)
    st.header('Medal tally')
    st.table(country_df)

    st.header('Performance of ' + country + ' over the years')
    fig = px.line(helper.plot_performance(df, country), x='Year', y='Medal')
    st.plotly_chart(fig)

    # Plot which sports a country has won most medals in
    st.header('Sport-wise performance of ' + country)
    # st.table(helper.country_sport_heatmap(df, country))
    # Show the value in the heatmap as well
    fig = px.bar(helper.country_sport_heatmap(df, country), x='Medal', y='Sport', color='Medal', barmode='group', height=600, text_auto='.0s')
    st.plotly_chart(fig)


if menu == 'Athlete analysis':
    st.title('Athlete Analysis')
    # This is because we need unique names, but an athlete may have participated
    #in multiple years of Olympics
    athletes = df.drop_duplicates(subset=['Name', 'region'])
    a_age = athletes['Age'].dropna()
    g = athletes[athletes['Medal'] == 'Gold']['Age'].dropna()
    s = athletes[athletes['Medal'] == 'Silver']['Age'].dropna()
    b = athletes[athletes['Medal'] == 'Bronze']['Age'].dropna()

    # Plot the distribution of age in general, and also based on medal
    st.header('Medal distribution by age')
    st.markdown('''
                * The average age of Olympic medalists is 25 years, with the youngest being 10 years old and the oldest being 72 years old.
                * The average age of Gold medalists is 25 years, with the youngest being 13 years old and the oldest being 64 years old.
                * The average age of Silver medalists is 25 years, with the youngest being 10 years old and the oldest being 71 years old.
                * The average age of Bronze medalists is 26 years, with the youngest being 11 years old and the oldest being 72 years old.
                ''')
    # User note to double-click on legend to isolate a particular medal
    hist_data = [a_age, g, s, b]
    group_labels = ['Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False)
    st.plotly_chart(fig)
    st.markdown('**Note:** Double-click on legend to isolate a particular medal')

    # Plot age distribution for medals by sport
    st.header('Gold medalists by age across sports')
    t = [] 
    name = []
    sports = ['Archery', 'Athletics', 'Badminton', 'Baseball', 'Basketball', 'Boxing', 'Cycling', 'Fencing', 'Football', 'Gymnastics', 'Hockey', 'Rowing', 'Sailing', 'Shooting', 'Table Tennis', 'Tennis', 'Volleyball', 'Weightlifting', 'Wrestling']
    for sport in sports:
        temp = athletes[athletes['Sport'] == sport]
        t.append(temp[temp['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    # Show bullets for readers to interpret
    st.markdown('''
    * The plot shows the distribution of age of gold medalists in different sports
    * Hover over the plot to see the exact age distribution for each sport  
    * A steep curve indicates that the gold medalists in that sport are of similar age
    * A flat curve indicates that the gold medalists in that sport are spread across a wide range of ages
    ''')    
    fig = ff.create_distplot(t, name, show_hist=False, show_rug=False)
    st.plotly_chart(fig)
    st.markdown('**Note:** Double-click on legend to isolate a particular medal')
    
    # Plot height and weight distribution for medals by sport
    st.header('Height and weight distribution for medalists by sport')
    # Create a heatmap for height and weight
    # Create a dropdown for sport
    sports.insert(0, 'Overall')
    sport = st.selectbox('', sports)
    st.markdown('''
    The plot shows the distribution of height and weight of medalists in different sports
    ''')
    if sport == 'Overall':
        fig = px.scatter(athletes, x='Height', y='Weight', color='Medal', opacity=0.8, hover_data=['Name'])
        fig.update_layout(xaxis_title='Height (cm)', yaxis_title='Weight (kg)')
    else:
        temp = athletes[athletes['Sport'] == sport]
        fig = px.scatter(temp, x='Height', y='Weight', color='Medal', opacity=0.8, hover_data=['Name'])
        fig.update_layout(xaxis_title='Height (cm)', yaxis_title='Weight (kg)', title=sport)
    st.plotly_chart(fig)

    # Plot male and female participation of a sport over the years
    men = athletes[athletes['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athletes[athletes['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    # f = men.merge(women,on='Year',how='left')
    # f.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    # f = f.fillna(0)

    # Add 'Overall' in the sport list as well
    st.header('Men/Women participation over the years')
    sports.insert(0, 'Overall')
    sport = st.selectbox('Select a sport', sports)

    men_women = helper.men_women(df, sport)
    # Plot the line chart
    fig = px.line(men_women, x='Year',y=['Male','Female'])
    st.plotly_chart(fig)