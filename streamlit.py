import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

# Sample data
data = {
    "Review ID": list(range(1, 31)),
    "Company": ["X"] * 10 + ["Y"] * 10 + ["Z"] * 10,
    "Category": [
        "Work Life Balance", "Compensation", "Work Life Balance", "Compensation", "Work Life Balance", "Company Culture", 
        "Management", "Work Life Balance", "Company Culture", "Compensation",
        "Work Life Balance", "Compensation", "Work Life Balance", "Compensation", "Work Life Balance", "Company Culture", 
        "Management", "Work Life Balance", "Company Culture", "Compensation",
        "Work Life Balance", "Compensation", "Work Life Balance", "Compensation", "Work Life Balance", "Company Culture", 
        "Management", "Work Life Balance", "Company Culture", "Compensation"
    ],
    "Aspect:Sentiment:Category": [
        [{'Aspect': 'working hours', 'Sentiment': 'negative', 'Category': 'work life balance'}, {'Aspect': 'holidays', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'salary', 'Sentiment': 'positive', 'Category': 'compensation'}],
        [{'Aspect': 'remote work', 'Sentiment': 'positive', 'Category': 'work life balance'}, {'Aspect': 'holidays', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'bonus', 'Sentiment': 'negative', 'Category': 'compensation'}],
        [{'Aspect': 'working hours', 'Sentiment': 'negative', 'Category': 'work life balance'}],
        [{'Aspect': 'company news', 'Sentiment': 'positive', 'Category': 'company culture'}],
        [{'Aspect': 'leadership', 'Sentiment': 'neutral', 'Category': 'management'}],
        [{'Aspect': 'remote work', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'company culture', 'Sentiment': 'positive', 'Category': 'company culture'}],
        [{'Aspect': 'salary', 'Sentiment': 'positive', 'Category': 'compensation'}, {'Aspect': 'bonus', 'Sentiment': 'negative', 'Category': 'compensation'}],
        [{'Aspect': 'workload', 'Sentiment': 'negative', 'Category': 'work life balance'}],
        [{'Aspect': 'benefits', 'Sentiment': 'positive', 'Category': 'compensation'}],
        [{'Aspect': 'flexible hours', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'salary', 'Sentiment': 'negative', 'Category': 'compensation'}],
        [{'Aspect': 'vacation', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'team events', 'Sentiment': 'positive', 'Category': 'company culture'}],
        [{'Aspect': 'management', 'Sentiment': 'neutral', 'Category': 'management'}],
        [{'Aspect': 'work from home', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'diversity', 'Sentiment': 'positive', 'Category': 'company culture'}],
        [{'Aspect': 'bonus', 'Sentiment': 'positive', 'Category': 'compensation'}],
        [{'Aspect': 'hours', 'Sentiment': 'negative', 'Category': 'work life balance'}],
        [{'Aspect': 'raises', 'Sentiment': 'positive', 'Category': 'compensation'}],
        [{'Aspect': 'remote work', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'pay', 'Sentiment': 'negative', 'Category': 'compensation'}],
        [{'Aspect': 'work hours', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'culture', 'Sentiment': 'positive', 'Category': 'company culture'}],
        [{'Aspect': 'management', 'Sentiment': 'negative', 'Category': 'management'}],
        [{'Aspect': 'remote work', 'Sentiment': 'positive', 'Category': 'work life balance'}],
        [{'Aspect': 'events', 'Sentiment': 'positive', 'Category': 'company culture'}],
        [{'Aspect': 'compensation', 'Sentiment': 'positive', 'Category': 'compensation'}, {'Aspect': 'promotion', 'Sentiment': 'negative', 'Category': 'compensation'}]
    ],
    "Review Text": [
        "The working hours are crazy, but we have good holidays. Overall, it's a mixed experience.",
        "The salary is good. I feel well-compensated.",
        "Remote work is highly encouraged and we have good holidays. It’s a flexible environment.",
        "The bonus structure is unfair. It's not motivating.",
        "The working hours are long. Sometimes, it’s hard to manage personal time.",
        "Company news is always exciting. The updates are very informative.",
        "Leadership is decent. They try to listen to employees.",
        "Remote work is highly encouraged. It makes balancing life easier.",
        "The company culture is great. Everyone is supportive.",
        "The salary is good but the bonus structure is unfair. It’s a mixed bag.",
        "Workload can be overwhelming. I often feel stressed.",
        "Benefits are excellent. They cover almost everything.",
        "Flexible hours are a plus. It helps manage work-life balance.",
        "Salary could be better. It doesn’t match industry standards.",
        "Vacation days are generous. It’s good to have time off.",
        "Team events are fun. They boost morale.",
        "Management is okay. They could be more proactive.",
        "Work from home is a great option. It saves commuting time.",
        "The company promotes diversity. It’s a welcoming place.",
        "Bonuses are good this year. It's encouraging.",
        "The hours are long. It’s often tiring.",
        "Raises are frequent. It's good for career growth.",
        "Remote work options are fantastic. It’s very flexible.",
        "Pay is not competitive. It needs improvement.",
        "Work hours are reasonable. It’s not too stressful.",
        "The culture here is positive. Everyone is friendly.",
        "Management needs improvement. They lack vision.",
        "Remote work is encouraged. It helps with work-life balance.",
        "Company events are frequent. They are enjoyable.",
        "Compensation is good, but promotions are slow. It’s frustrating."
    ],
    "Post Type": [
        "Employee Review", "Employee Review", "Social Media", "Employee Review", "Employee Review", "Social Media", 
        "Social Media", "Employee Review", "Social Media", "Employee Review",
        "Employee Review", "Employee Review", "Employee Review", "Employee Review", "Employee Review", "Social Media", 
        "Social Media", "Employee Review", "Social Media", "Employee Review",
        "Employee Review", "Employee Review", "Employee Review", "Employee Review", "Employee Review", "Social Media", 
        "Social Media", "Employee Review", "Social Media", "Employee Review"
    ],
    "Age": [29, 34, "", 40, 32, "", "", 27, "", 31, 28, 30, 35, 45, 33, "", "", 26, "", 29, 32, 38, 31, 44, 36, "", "", 29, "", 33],
    "Job Title": [
        "Software Engineer", "Manager", "", "Analyst", "Consultant", "", "", "HR", "", "Developer", 
        "Accountant", "Designer", "Developer", "Manager", "HR", "", "", "Engineer", "", "Technician", 
        "Executive", "Specialist", "Consultant", "Manager", "Analyst", "", "", "Engineer", "", "Accountant"
    ],
    "Latitude": [
        37.7749, 51.5074, 39.9042, 52.5200, 35.6895, 39.9042, 51.1657, 28.7041, 48.8566, 34.0522, 
        37.7749, 51.5074, 31.2304, 52.5200, 35.6895, 39.9042, 51.1657, 28.7041, 48.8566, 34.0522, 
        37.7749, 51.5074, 31.2304, 52.5200, 35.6895, 39.9042, 51.1657, 28.7041, 48.8566, 34.0522
    ],
    "Longitude": [
        -122.4194, -0.1278, 116.4074, 13.4050, 139.6917, 116.4074, 10.4515, 77.1025, 2.3522, -118.2437, 
        -122.4194, -0.1278, 121.4737, 13.4050, 139.6917, 116.4074, 10.4515, 77.1025, 2.3522, -118.2437, 
        -122.4194, -0.1278, 121.4737, 13.4050, 139.6917, 116.4074, 10.4515, 77.1025, 2.3522, -118.2437
    ],
    "Language": [
        "English", "English", "Chinese", "German", "Japanese", "Chinese", "German", "Hindi", "French", "English", 
        "English", "English", "Chinese", "German", "Japanese", "Chinese", "German", "Hindi", "French", "English", 
        "English", "English", "Chinese", "German", "Japanese", "Chinese", "German", "Hindi", "French", "English"
    ]
}

# Add random dates
start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 1, 1)
date_range = end_date - start_date
data["Date"] = [start_date + timedelta(days=random.randint(0, date_range.days)) for _ in range(30)]

df = pd.DataFrame(data)

# Explode the 'Aspect:Sentiment:Category' column
df_exploded = df.explode('Aspect:Sentiment:Category')
df_exploded['Aspect'] = df_exploded['Aspect:Sentiment:Category'].apply(lambda x: x['Aspect'])
df_exploded['Sentiment'] = df_exploded['Aspect:Sentiment:Category'].apply(lambda x: x['Sentiment'])
df_exploded['Category'] = df_exploded['Aspect:Sentiment:Category'].apply(lambda x: x['Category'])

# Streamlit app
st.title("Company Review Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
company_filter = st.sidebar.multiselect("Select Company", options=df["Company"].unique(), default=df["Company"].unique())

# Main dashboard
st.header("Location Hotspot with Sentiment")
filtered_df = df[df["Company"].isin(company_filter)]
df_exploded_filtered = df_exploded[df_exploded["Company"].isin(company_filter)]

fig = px.scatter_mapbox(
    df_exploded_filtered, lat="Latitude", lon="Longitude", color="Sentiment",
    color_discrete_map={"positive": "green", "negative": "red", "neutral": "grey"},
    size_max=15, zoom=1, height=500
)
fig.update_traces(marker=dict(size=15))
fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# Drilldown: Category -> Aspect -> Reviews
st.header("Drilldown into Reviews")

category_filter = st.selectbox("Select Category", options=df_exploded_filtered["Category"].unique())
aspect_filter = st.selectbox("Select Aspect", options=df_exploded_filtered[df_exploded_filtered["Category"] == category_filter]["Aspect"].unique())
filtered_reviews = df_exploded_filtered[(df_exploded_filtered["Category"] == category_filter) & (df_exploded_filtered["Aspect"] == aspect_filter)]

st.subheader("Reviews")
for review in filtered_reviews["Review Text"].unique():
    st.write(f"- {review}")

# Sentiment Analysis Dashboard
st.header("Sentiment Analysis")

# Word Cloud
st.subheader("Word Cloud")
aspect_text = ' '.join(df_exploded_filtered["Aspect"])
wordcloud = WordCloud(background_color="rgba(255, 255, 255, 0)", mode="RGBA").generate(aspect_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

# Sentiment Summary
st.subheader("Sentiment Summary")
sentiment_summary = df_exploded_filtered["Sentiment"].value_counts()
fig_sentiment = px.bar(sentiment_summary, x=sentiment_summary.index, y=sentiment_summary.values, color=sentiment_summary.index, color_discrete_map={"positive": "green", "negative": "red", "neutral": "grey"})
st.plotly_chart(fig_sentiment)

# User Demographics Dashboard
st.header("User Demographics")
df_demo = df[df["Company"].isin(company_filter)]

# Job Title Distribution
st.subheader("Job Title Distribution")
job_title_distribution = df_demo["Job Title"].value_counts()
fig_job_title = px.pie(job_title_distribution, names=job_title_distribution.index, values=job_title_distribution.values, title="Job Title Distribution")
st.plotly_chart(fig_job_title)

# Post Type Distribution
st.subheader("Post Type Distribution")
post_type_distribution = df_demo["Post Type"].value_counts()
fig_post_type = px.bar(post_type_distribution, x=post_type_distribution.index, y=post_type_distribution.values, title="Post Type Distribution")
st.plotly_chart(fig_post_type)

# Executive Summary for a Selected Company
st.header("Executive Summary")
company_summary = st.selectbox("Select a Company for Summary", options=df["Company"].unique())

# Hardcoded summaries for each company
summaries = {
    "X": "Company X shows mixed reviews. Employees appreciate the work-life balance and remote work options, but there are concerns about long working hours and an unfair bonus structure. Company culture is generally positive, with good holidays and supportive colleagues.",
    "Y": "Company Y is praised for its flexible work environment, particularly remote work options. Compensation is seen as fair, but there are some negative sentiments about salary and pay structure. The company is noted for promoting diversity and having a positive culture.",
    "Z": "Company Z receives positive feedback for its company culture and team events. Compensation is considered good, but there are complaints about slow promotions and long working hours. Management is seen as needing improvement, with some negative reviews about leadership."
}

# Display the summary for the selected company
st.write(f"Executive Summary for {company_summary}: {summaries[company_summary]}")


# Time Series Analysis of Sentiments
st.header("Time Series Analysis")
df_time_series = df_exploded[df_exploded["Company"].isin(company_filter)]
df_time_series['Sentiment Score'] = df_time_series['Sentiment'].map({"positive": 1, "neutral": 0, "negative": -1})

# Combine sentiment progression into one line
df_time_series_grouped = df_time_series.groupby(df_time_series["Date"].dt.to_period("M"))['Sentiment Score'].sum()
df_time_series_grouped.index = df_time_series_grouped.index.to_timestamp()

fig_time_series = px.line(df_time_series_grouped, x=df_time_series_grouped.index, y=df_time_series_grouped.values, title="Monthly Sentiment Progression", labels={"index": "Date", "value": "Sentiment Score"})
st.plotly_chart(fig_time_series)
