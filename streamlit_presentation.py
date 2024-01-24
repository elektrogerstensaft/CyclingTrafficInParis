import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pickle
from urllib.request import urlopen

# in rare cases there might be a SSL error:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# import the main dataframe and the barometer dataframe
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://fwpn.uber.space/media/CyclingTrafficInParis_eng.csv")
df_barom = load_data("https://fwpn.uber.space/media/reponses-departement-75.csv")

@st.cache_resource
def load_model(filename):
    model = pickle.load(open(filename, 'rb'))
    return model

#st.set_page_config(layout="wide")   #this eliminates margins left and right on wider screens, but some plots do not work well with it 

st.image("Header.png", caption="Image generated by Midjourney AI")
st.title("A DATA ANALYSIS OF THE CYCLING TRAFFIC IN PARIS")
st.header("From October 2022 to November 2023")

## table of contents
st.sidebar.title("Table of contents")
pages=["Summary", "Cycling Traffic", "Weather & Traffic", "Interview / Barometer", "Machine Learning", "Conclusion"]
page=st.sidebar.radio("Go to", pages)

## about
st.sidebar.markdown("---")
st.sidebar.markdown(
  """
  <div style="background-color: #285562; border: 1px solid #85d2db; padding: 10px; border-radius: 5px;">

  **Authors:**
  - Martin Kruse
  - Andy Soydt
  - Marine Bajard-Malfondet

  **Data sources:**
  - [Comptage vélo | Open Data | Ville de Paris](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/information/?disjunctive.id_compteur&disjunctive.nom_compteur&disjunctive.id&disjunctive.name) 
  - [Observation météorologique historiques France | OpenDataSoft](https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/export/?q=paris&refine.nom=ORLY&q.timerange.date=date:%5B2022-09-30T22:00:00Z+TO+2023-10-31T22:59:59Z%5D&sort=date&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJ0YyIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiNGRjUxNUEifV0sInhBeGlzIjoiZGF0ZSIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6ImRheSIsInNvcnQiOiIiLCJjb25maWciOnsiZGF0YXNldCI6ImRvbm5lZXMtc3lub3AtZXNzZW50aWVsbGVzLW9tbSIsIm9wdGlvbnMiOnsicSI6InBhcmlzIiwicmVmaW5lLm5vbSI6Ik9STFkiLCJxLnRpbWVyYW5nZS5kYXRlIjoiZGF0ZTpbMjAyMi0wOS0zMFQyMjowMDowMFogVE8gMjAyMy0xMC0zMVQyMjo1OTo1OVpdIiwic29ydCI6ImRhdGUifX19XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D)
  - [Baromètres Parlons vélo | OpenData](https://barometre.parlons-velo.fr/)

  </div>
  """,
  unsafe_allow_html=True
)

## pages /w content

if page == pages[0]:  # Summary
  st.title("Summary")
  st.markdown(
    """
    ### Introduction

    This data analysis conducts a comprehensive examination of cycling traffic within the city of Paris, utilizing publicly available data on cycling counts, meteorological conditions, and national holidays. The study yields insightful observations and valuable outcomes.

    ### Data Gathering and Processing

    In gathering and processing the data, a variety of factors were considered, going beyond the surface to understand the dynamics of traffic. This section delves into a careful analysis of counts and explores their interplay with changing weather patterns. The outcomes are presented through vivid traffic overview maps and a variety of charts, creating a clear and logical picture of the cycling scenario in Paris.

    ### Predictive Modeling with Machine Learning

    Leveraging the capabilities of machine learning, we designed predictive models that successfully anticipate cycling traffic patterns. This section details our approach, sharing insights gained from our models. The predictions provide a glimpse into the potential future cycling trends in the city.

    ### Executive Summary

    This executive summary aims to provide a brief yet precise overview of our comprehensive data analysis. It serves as a starting point for a deeper exploration within the complete report.
    """
  )


if page == pages[1]:  # Cycling traffic
    st.title("Cycling Traffic")
  
    df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc= True)

    weekdays = {
        0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    df["weekday_of_count"] = df["weekday_of_count"].map(weekdays)

    monthReduceDict = {
        "2022-10": "Oct / Nov 22",
        "2022-11": "Oct / Nov 22",
        "2022-12": "Dec 22 / Jan 23",
        "2023-01": "Dec 22 / Jan 23",
        "2023-02": "Feb / Mar 23",
        "2023-03": "Feb / Mar 23",
        "2023-04": "Apr / May 23",
        "2023-05": "Apr / May 23",
        "2023-06": "Jun / Jul 23",
        "2023-07": "Jun / Jul 23",
        "2023-08": "Aug / Sep 23",
        "2023-09": "Aug / Sep 23",
        "2023-10": "Oct / Nov 23",
        "2023-11": "Oct / Nov 23"
        }
    df["Months reduced"] = df["Month and year of count"].map(monthReduceDict)

    # finding the top 3 counters and creating a dataframe only with them
    df_top3 = df.groupby(["Counter name"],as_index= False)["Hourly count"].sum().sort_values("Hourly count", ascending = False).head(3)

    top3 = []
    for x in df_top3["Counter name"]:
        top3.append(x)
    df_top3 = df.loc[df["Counter name"].isin(top3)]

    st.write("### Cycling Traffic")
    st.write("#### Initial Data")
    # presentation of the data (volume, architecture, etc.)
    # data analysis using DataVizualization figures
    st.write("The initial data are the hourly counts of bicycles at different counting sites in Paris from October 2022 to November 2023. \
            For every hour and every counter a line was added to the dataset. The target variable is *Hourly Count*. As metadata was added to every line, \
            the file is bloated with repetetive information like URL of photographs or installation dates. Irrelevant metadata was removed. \
            Each counting site can have two *counters* - one for each direction of a street. The direction is encoded in the counter name and was translated into a separate column \
            The *date and time* information is stored in a single variable and was processed into: date, time, ISO week and year, day (of month), day of week. Month of year was already present \
            The *geographic coordinates* were present in a combined column and were separated into latitude and longitude.            ")
    st.write("#### Data Cleaning")
    st.write("Some entries appeared to be older than the timeframe and were removed. Counts with 0 or more than 2000 bicycles were also removed.")

    fig = px.box(df_top3, y ="Hourly count", x = "Months reduced", title = "All counters hourly counts")
    fig.update_layout(font=dict(size=20))
    st.plotly_chart(fig)

    st.write("The time domain shows a distribution related to working days vs. weekends and to the hour of day. Daily commutes appear very well in the heatmap.")
    # Heatmap of days and hours with most traffic
    order = ["Sunday", "Saturday", "Friday", "Thursday", "Wednesday", "Tuesday","Monday"]

    grouped_multiple = df_top3.groupby(["hour_of_day", "weekday_of_count"]).agg({"Hourly count": ["mean", "median","sum"]})
    grouped_multiple.columns = ["Hourly_count_mean", "Hourly_count_median","Hourly_count_sum"]
    grouped_multiple = grouped_multiple.reset_index()

    fig = go.Figure(
        data = go.Heatmap(
            z = grouped_multiple["Hourly_count_sum"],
            x = grouped_multiple["hour_of_day"],
            y = grouped_multiple["weekday_of_count"]
        )
    )
    fig.update_xaxes(title = "Hour of day")
    fig.update_yaxes(title = "Weekday", categoryarray = order)
    fig.update_layout(
        title="Heatmap of daytimes per weekday with most bicycle traffic",
        font=dict(size=20))
    st.plotly_chart(fig)

    st.write("As the heatmap shows, traffic is highest in the moring and has a second peak in the afternoon on working days. A third peak can be observed in the evening, at 9pm. \
             We assume the first peak is caused by commuters riding to work and the second peak consists of them riding back. It remains unclear why the first peak is 30-40% smaller \
             than the second. As the top 2 counters are oriented in opposite directions of the same counting site, the simple assumption of people going in one direction \
             in the morning and returning in the afternoon does not line up with the different sized peaks. Either cyclists avoid the counter sites in mornings, \
             or a part of the cyclists who travel in one direction midday also travel back in the afternoon.")
    fig = px.line(df.loc[(df["Counter name"].isin(top3)) & (df["week_year"] == "2023-23")].sort_values("Date and time of count"),
    x="Date and time of count",
    y="Hourly count",
    color = "Counter name")
    fig.update_layout(
        title ="Hourly count of bicycles at top 3 counters",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        font = dict(size=20))
    st.plotly_chart(fig)

    st.write("#### Vacation Dates")
    st.write("As weekends have less traffic, it was estimated, that other vacation days (e.g. christmas or summer holidays) also influence the traffic. ")
    df_w = pd.read_csv("WeatherAndTraffic.csv", sep = ",")

    grouped_multiple = df_top3.groupby(["date","holiday"]).agg({"Hourly count": "sum"})
    grouped_multiple = grouped_multiple.reset_index()

    g = sns.lineplot(data=grouped_multiple, x = "date", y= "Hourly count")

    #sns.scatterplot(data=grouped_multiple, x = "date", y= "Hourly count")
    g2 = sns.scatterplot(data=grouped_multiple, x = "date", y= "holiday", ax = g.axes.twinx())
    g.set(xlabel = "Date", ylabel = "Daily count", title ="Number of bicycles per day and holiday")
    sns.set(font_scale=1.25)
    new_ticks = [i.get_text() for i in g.get_xticklabels()]
    plt.xticks(range(0, len(new_ticks), 30), new_ticks[::30])
    g.set_xticklabels(g.get_xticklabels(), rotation=45)
    st.pyplot(g.get_figure())

    st.write("The counting sites are spread heterogeneous over the city: \n      \
              the North-South axis (Gare du Nord/ Gare de l’Est – Châtelet – Odéon) and the Seine banks are best covered \n \
              the north of Paris and the ring (in particular West/ North) have fewer counter sites \n \
              some arrondissements not having in addition any counter site at all \n \
              The dot size on the map indicates how many bicycles were counted. It appears that traffic is higher in the centre. The three counters with the most traffic are:" \
              , df_top3["Counter name"].unique())
    #st.write(df_top3["Counter name"].unique())
    df_counter= pd.read_csv("Counters.csv", sep= ",")
    df_counter.set_index("Counter name", inplace = True)
    df_reduced = df.drop(["Counter ID","Counting site installation date","Geographic coordinates", "Counting site ID"], axis = 1)   
    df_reduced.rename({"Hourly count":"Total count"}, axis="columns", inplace=True)

    #grouping by the Counter name, aggregation by sum of hourly counts 
    df_reduced = df_reduced.groupby(["Counter name"],as_index= True)["Total count"].sum()

    # merge the previous df with the Counter metadata df
    df_geo = pd.concat([df_reduced, df_counter], axis=1)
    df_geo.dropna(inplace=True)
    df_geo.set_index("Counter ID", inplace = True)

    # generating a GeoDataFrame 
    gdf = gpd.GeoDataFrame(
        df_geo, geometry=gpd.points_from_xy(df_geo.Longitude, df_geo.Latitude), crs="EPSG:4326"
    )

    # creating a scatter plot on a map background
    fig = px.scatter_mapbox(gdf,
                            lat=gdf.geometry.y,
                            lon=gdf.geometry.x,
                            size = "Total count",
                            color = "Total count",
                            hover_name="Counting site name",
                            hover_data="Total count",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            zoom=10.9,
                            title = "Total counted bicycles in Paris")
    fig.update_layout(mapbox_style="carto-positron",
                    margin={"r":0,"t":0,"l":0,"b":0},
                    font=dict(size=18, color="Black"))
    st.plotly_chart(fig)


## THE FOLLOWING PAGE IS NOT FINISHED YET

if page == pages[2]:  # Weather & Traffic 
  st.title("Weather & Traffic")

  df_W = load_data("https://fwpn.uber.space/media/Weather_eng_final.csv")

  df_W = df_W.drop(columns = ["date", "year", "month", "year_month", "day", "time"]) #prevents duplicated columns with x / y

  # Weather DF: deleting substring "T" within column "Date_original" and renaming column "Date" for merging purposes
  df_W.rename({"Date_original": "Date and time of count"}, axis=1, inplace=True)
  df_W["Date and time of count"] = pd.to_datetime(df_W["Date and time of count"].str.replace("T"," "), utc=True)
  print(df_W.head())
  df["Date and time of count"] = pd.to_datetime(df["Date and time of count"], utc=True)


  # Concatenating the two datasets based on column ‘Date and time of count’
  df_final_W = df.merge(right = df_W, on = "Date and time of count", how = "left")

  ## Temp + Rain infos only different hours not always corresponding to traffic cycling DF > Following strategy: fill in missing values with next precedent available information
  # Sorting final DF based on columns "Counter ID" and ‘Date and time of count" and resetting index
  df_final_W.sort_values(by=["Counter ID","Date and time of count"], inplace = True)
  df_final_W = df_final_W.reset_index()
  df_final_W=df_final_W.drop("index", axis="columns")

  # Filling in missing values with the next previous information available
  df_final_W = df_final_W.fillna(method="ffill")
  #print(df_final_W.head())

  # Last check on NaN
  nan_count = df_final_W.isna().sum()
  #print(nan_count)

  # Replacing in final DF Cycling + weather -0.1mm precipitation with 0.00 (as cannot exist)
  #print(df_final_W["Rain_last3H"].unique())
  df_final_W["Rain_last3H"].replace(-0.1, 0, inplace=True)

  df_final_W.info()
  percent_missing = df.isnull().sum() * 100 / len(df)

  # Min/ Max on temperatures + precipitation
  print(df["Temp_°C"].min())
  print(df["Temp_°C"].max())
  df = df[df["Temp_°C"] >= 35]
  df = df[df["Temp_°C"] <= -6]

  print(df["Rain_last3H"].min())
  print(df["Rain_last3H"].max())

  df = df[df["Rain_last3H"] >= 0]
  df = df[df["Rain_last3H"] <= 14.9]


  # Calculating correlation coefficient between 
  np.corrcoef(df["Temp_°C"], df["Hourly count"])
  np.corrcoef(df["Rain_last3H"], df["Hourly count"])


  # Satistical tests on weather
  #1)	Temp and hourly count

  from scipy.stats import pearsonr
  pearsonr(x = df["Temp_°C"], y = df["Hourly count"]) 

  print("p-value: ", pearsonr(x = df["Temp_°C"], y = df["Hourly count"])[1])
  print("coefficient: ", pearsonr(x = df["Temp_°C"], y = df["Hourly count"])[0])

  #2)	precipitations and hourly count

  from scipy.stats import pearsonr
  pearsonr(x = df["Rain_last3H"], y = df["Hourly count"]) 

  print("p-value: ", pearsonr(x = df["Rain_last3H"], y = df["Hourly count"])[1])
  print("coefficient: ", pearsonr(x = df["Rain_last3H"], y = df["Hourly count"])[0])


  # Impact of temp and precipitations on average hourly count
  # Impact of temperatures < 5°C and viz
  Temp = [] 

  for row in df["Temp_°C"]:
     if row < 5 : Temp.append("< 5°C") 
     else: Temp.append("> 5°C") 

  df["Temp"] = Temp 
  print(df.head())

  df_temp = df.groupby("Temp", as_index=False)["Hourly count"].mean()

  plt.rcParams["figure.figsize"] = (4, 5)
  ax = sns.barplot(x = "Temp", y = "Hourly count", data = df_temp, errorbar=("ci", False))
  ax.bar_label(ax.containers[0], label_type="edge")

  plt.xlabel("Temperatures")
  plt.ylabel("Average hourly count")
  plt.title("Impact of temperatures on cycling traffic")
  plt.show()


  # Impact of temperatures > 25°C and viz
  Temp2 = [] 

  for row in df["Temp_°C"]:
    if row > 25: Temp2.append("> 25°C") 
    else: Temp2.append("< 25°C") 

  df["Temp2"] = Temp2 
  print(df.head())


  df_temp2 = df.groupby("Temp2", as_index=False)["Hourly count"].mean()

  plt.rcParams["figure.figsize"] = (4, 5)
  ax = sns.barplot(x = "Temp2", y = "Hourly count", data = df_temp2, errorbar=("ci", False))
  ax.bar_label(ax.containers[0], label_type="edge")

  plt.xlabel("Temperatures")
  plt.ylabel("Average hourly count")
  plt.title("Impact of temperatures on cycling traffic")

  plt.show()

  # Impact of precipitations and viz

  df_rain = df.groupby("Rain_classes", as_index=False)["Hourly count"].mean()

  plt.rcParams["figure.figsize"] = (6, 6)
  ax = sns.barplot(x = "Rain_classes", y = "Hourly count", data = df_rain, errorbar=("ci", False))
  ax.bar_label(ax.containers[0], label_type="edge")

  plt.xlabel("Precipitation classes")
  plt.ylabel("Average hourly count")
  plt.title("Impact of precipitations on cycling traffic")

  plt.show()


if page == pages[3]:  # Interview & Barometer
  st.title("### Interview & Barometer")
  st.header("#### Data Collection and Pre-Processing")
   
  # presentation of the data (volume, architecture, etc.) and cleaning steps
  
  st.write(
    "We retrieved bike user's opinions from the last survey on the bikers-cities in France made available for year 2021 and carried out by the \
    French bicycle users federation (Fédération des Usagers de la Bicyclette – FUB). In this survey, there was a total of 29 questions asked to users split \
    into five different topics from their general feeling in terms of security and comfort to the current infrastructure and amenities as well the current \
    public policies to promote bike use where participants express their opinion on a scale of 6 points (for example on security matters 1 being \
    'not feeling safe' and 6 being 'feeling safe'). A global note was then calculated from the average of each five topics.\
    We could retrieve for the city of Paris alone 9,116 responses which we further analyze, after having resized the dataset and added some information \
    (total sum,etc...). ") 

  st.dataframe(df_barom.head(10))

  
  # data analysis using DataVizualization figures
  # Viz on evolution and general feeling scores for city of Paris

  page_names = ["General evolution score","General feeling scores","Individual feeling topic scores"]
  page = st.radio("Barometer general results 2021", page_names)

  if page == "General evolution score":
    df_barom = df_barom.drop(columns=["uid", "q01"])
    df_barom_evol = df_barom.groupby("q13", as_index=False)["q13"].value_counts()
    df_barom_evol["percent"] = ((df_barom_evol["count"] /
                  df_barom_evol["count"].sum()) * 100).round(2)
    list_evol = {1: "Highly deteriorated",
                 2: "Slightly deteriorated",
                 3: "Identical",
                 4: "Slightly ameliorated",
                 5: "Highly ameliorated"}
    df_barom_evol["q13_name"] = df_barom_evol["q13"].map(list_evol)

    fig = plt.figure()
    plt.rcParams["figure.figsize"] = (10, 6)
    ax = sns.barplot(x = "q13_name", y = "percent", data = df_barom_evol, errorbar=("ci", False))
    ax.bar_label(ax.containers[0], label_type="edge",fmt="%.1f%%")

    plt.xlabel("Situation")
    plt.ylabel("%")
    plt.title("General evolution score")
    st.pyplot(fig)

    st.write("From this general evolution score, we observe that 81,7% of the respondents found the situation has slightly or highly positively evolved \
    whereas 8,8% are of the opinion that it has deteriorated either highly or slightly. 9.5% of the respondents perceived an identical situation with \
    no amelioration or deterioration.")

  if page == "General feeling scores":

    df_barom = df_barom.drop(columns=["uid", "q01"])
    
    General_feeling = df_barom[["q14", "q15", "q16", "q17","q18","q19"]].sum().sum() / (9116*6)
    Security = df_barom[["q20", "q21", "q22", "q23","q24","q25"]].sum().sum() / (9116*6)
    Comfort = df_barom[["q26", "q27", "q28", "q29","q30"]].sum().sum() / (9116*5)
    Efforts = df_barom[["q31", "q32", "q33", "q34"]].sum().sum() / (9116*4)
    Services_and_parking_lots = df_barom[["q35", "q36", "q37", "q38","q39"]].sum().sum() / (9116*5)
    Global_score = df_barom[["q14", "q15", "q16", "q17","q18","q19","q20", "q21", "q22", "q23","q24","q25","q26", "q27", "q28", "q29","q30","q31", "q32", "q33", "q34","q35", "q36", "q37", "q38","q39"]].sum().sum() / (9116*26)

    data = {"Topics": ["General feeling","Security","Comfort","Efforts", "Services and parking lots", "Global score"],
        "Score": [3.27,3.06,3.31,3.61,3.40,3.31]}
    df_barom_gen = pd.DataFrame(data)

    fig = plt.figure()
    plt.rcParams["figure.figsize"] = (12, 6)
    ax = sns.barplot(x = "Topics", y = "Score", data = df_barom_gen, errorbar=("ci", False))
    ax.bar_label(ax.containers[0], label_type="edge")

    plt.ylim(0, 6)
    plt.xlabel("")
    plt.ylabel("Score")
    plt.title("Barometer general results overview")
    st.pyplot(fig)

    st.write("From this general feeling scores, the city of Paris got a global score of 3.31 on a scale of 0 to 6 alongside with all five topics \
    scoring between 3.06 and 3.61: Security scores the worst with 3.06 whereas efforts score the best with 3.61. This proves that the municipality efforts \
    are recognized, but not sufficient in terms of security for exampel for bike users. ")

  else:
    st.subheader("Individual feeling topic scores")
    pages_names_indiv = ["General feeling","Security","Comfort","Efforts","Service and parking lots"]
    page_indiv = st.radio("Individual feeling topic scores", page_names_indiv)

    if page == "General feeling":
      data_feel = {"General feeling": ["In my opinion, bike usage in my municipality is",
                                       "The cycle route network of my municipality allows me to go everywhere quickly and directly",
                                       "Cycling in your municipality is",
                                       "Conflicts between individuals cycling and walking are",
                                       "When cycling, individuals driving motorized vehicles respect me", 
                                       "When cycling, I find motorized traffic (volume and speed) to be"],
                   "Score": [4.22,3.89,3.60,2.88,2.54,2.47]}

      df_barom_feel = pd.DataFrame(data_feel)

      fig = plt.figure()
      plt.rcParams["figure.figsize"] = (12, 6)
      ax = sns.barplot(x = "Score", y = "General feeling", data = df_barom_feel, errorbar=("ci", False))
      ax.bar_label(ax.containers[0], label_type="edge")

      plt.xlabel("Score")
      plt.ylabel("")
      plt.title("Individual topics score - General feeling")
      st.pyplot(fig)


    st.write("From a general feeling , the city of Paris got a global score of 3.31 on a scale of 0 to 6 alongside with all five topics \
    scoring between 3.06 and 3.61: Security scores the worst with 3.06 whereas efforts score the best with 3.61. This proves that the municipality efforts \
    are recognized, but not sufficient in terms of security for exampel for bike users. ")

  # We can then conclude from this general analysis that the city of Paris on a scale from 0 to 6 does not score well with a global score of 3.31: 
  # Even if the cycling traffic is progressing, users still perceived security to be an important issue, in particular when crossing a junction or a 
  # round-about (score of 1.98 on this question) or for children and seniors (score of 2.51 on this question). 
  # The efforts made by the municipality were however highlighted with a score of 3.61: in particular, efforts made towards cycling and communication 
  # in favor of cycling with respective scores of 4.60 and 4.09 were positively perceived, although motorized vehicles parking on cycle lanes is still 
  # being very negatively perceived and seen as a real issue encountered too many times (score of 1.92).

    if page == "Security":
      data_secu = {"Security": ["I can cycle in security in residential streets",
                            "I can safely cycle on the major traffic routes ",
                            "In general, when cycling in my municipality I feel",
                            "I can safely reach by bicycle neighboring communities",
                            "In my opinion, crossing a junction or a roundabout is", 
                            "For children and seniors, cycling is"],
                   "Score": [3.84,3.64,3.26,3.15,2.51,1.98]}

      df_barom_secu = pd.DataFrame(data_secu)

      fig = plt.figure()
      plt.rcParams["figure.figsize"] = (12, 6)
      ax = sns.barplot(x = "Score", y = "Security", data = df_barom_secu, errorbar=("ci", False))
      ax.bar_label(ax.containers[0], label_type="edge")

      plt.xlabel("Score")
      plt.ylabel("")
      plt.title("Individual topics score - Security")
      st.pyplot(fig)


    if page == "Comfort":
      data_com = {"Comfort": ["When cycling, I am allowed to use one-way roads against the traffic",
                              "In my opinion, cycling routes are",
                              "The maintenance of cycling routes is",
                              "Cycling directions are correctly indicated by panels",
                              "When maintenance work on cycle routes is carried out, a safe alternative is suggested"],
                  "Score": [4.47,3.52,3.28,2.97,2.30]}

      df_barom_com = pd.DataFrame(data_com)

      fig = plt.figure()
      plt.rcParams["figure.figsize"] = (12, 6)
      ax = sns.barplot(x = "Score", y = "Comfort", data = df_barom_com, errorbar=("ci", False))
      ax.bar_label(ax.containers[0], label_type="edge")

      plt.xlabel("Score")
      plt.ylabel("")
      plt.title("Individual topics score - Comfort")
      st.pyplot(fig)

    if page == "Efforts":
      data_eff = {"Efforts": ["In my opinion, efforts made by the municipality in favor of cycling are",
                              "Communication made in favor of cycling mobility is",
                              "City hall is listening to cycling users needs, involve them into their reflections on mobility and urban development projects",
                              "In my opinion, parking of motorized vehicles (cars, trucks, motorcycles...) on cycling routes is"],
                  "Score": [4.60,4.09,3.82,1.95]}

      df_barom_eff = pd.DataFrame(data_eff)

      fig = plt.figure()
      plt.rcParams["figure.figsize"] = (12, 6)
      ax = sns.barplot(x = "Score", y = "Efforts", data = df_barom_eff, errorbar=("ci", False))
      ax.bar_label(ax.containers[0], label_type="edge")

      plt.xlabel("Score")
      plt.ylabel("")
      plt.title("Individual topics score - Efforts")
      st.pyplot(fig)
    
    else:
      data_park = {"Parking": ["Near or within the municipality, to find a cycling store or a repair shop is" ,
                               "To rent a bike for a few hours or months is",
                               "Near or within the municipality, to find a parking lot adapted to my specific needs is",
                               "To park its bike at a railway station or a public transportation station is",
                               "In my opinion, bicycle thefts are"],
                   "Score": [4.60,4.51,3.11,2.80,1.95]}

      df_barom_park = pd.DataFrame(data_park)

      fig = plt.figure()
      plt.rcParams["figure.figsize"] = (12, 6)
      ax = sns.barplot(x = "Score", y = "Parking", data = df_barom_park, errorbar=("ci", False))
      ax.bar_label(ax.containers[0], label_type="edge")

      plt.xlabel("Score")
      plt.ylabel("")
      plt.title("Individual topics score - Services and parking lots")
      st.pyplot(fig)


if page == pages[4] :
  model_file = "RFR.sav"
  model = load_model(model_file)
  st.title("Machine Learning")
  st.write("### Data Preprocessing")
  st.write("#### Train, Test, Split")
  st.write("Before applying any normalisation or encoding, the complete data frame was divided into feature variables and the target variable *hourly counts*. \
           With train_test_split from the scikit learn library the inputs were divided into  a train set and a test set.")
  code = """feats = df[["hour_of_day", "weekday_of_count", "Month and year of count", "day", "Latitude", "Longitude", "Humidity", "Temp_°C", "Rain_last3H", "direction","holiday"]]
target = df["Hourly count"]

X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25, random_state=42)
  """
  st.code(code, language="python")
  st.write("The feature were split into 3 variable types: categorical, numerical and cyclical.")
  code="""cat = ["direction", "Month and year of count","holiday"]
    num = ["day", "Latitude", "Longitude","Humidity","Temp_°C","Rain_last3H"]
    circular = ["hour_of_day", "weekday_of_count"]"""
  st.code(code, language= "python")

  st.write("#### Normalisation")  
  st.write("The numerical variables were treated with the scikit learn standard scaler method.")
  code="""from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train[num] = sc.fit_transform(X_train[num])
    X_test[num] = sc.transform(X_test[num])"""
  st.code(code, language= "python")

  st.write("#### Encoding")
  st.write("The categorical variables were treated with the scikit learn one hot encoder method.")
  code="""from sklearn.preprocessing import OneHotEncoder
    ohe = OneHotEncoder(drop="first",  sparse_output=False)
    X_train_Cat = pd.DataFrame(ohe.fit_transform(X_train[cat]))
    X_train_Cat.columns= ohe.get_feature_names_out()"""
  st.code(code, language= "python")

  st.write("The cyclical variables were treated with sine and cosine functions like this:")
  code="""circular_train.loc[:, "sin_hour"] = circular_train.loc[:, "hour_of_day"].apply(lambda h : np.sin(2 * np.pi * h / 24))
    circular_train.loc[:, "cos_hour"] = circular_train.loc[:, "hour_of_day"].apply(lambda h : np.cos(2 * np.pi * h / 24))"""
  st.code(code, language= "python")
 


  st.write("### Algorithms")
  st.write("Since the target variable is numerical and not binary, the prediction is a regression problem. The following regression algorithms were tested:")
  lst = ["Linear Regression","Decision Tree Regression","K-Nearest-Neighbor (KNN)","Multilayer perceptron (MLP)","Random Forest Regression","Gradient Boosting Regression"]
  for i in lst:
    st.markdown("- " + i)
  st.write("The scores of the algorithms were used to determine which algorithms to look further into.")
  
  st.write("### Predictions")
  
  
if page == pages[5]:  # Conclusion
  st.title("Conclusion")
  st.markdown(
    """
    ### Introduction

    Lorem ipsum dolor sit amet

    ### Data Gathering and Processing

    Lorem ipsum dolor sit amet

    ### Predictive Modeling with Machine Learning

    Lorem ipsum dolor sit amet
    """
  )
