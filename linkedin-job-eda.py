
#imports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import datetime

#Set display option
pd.set_option('display.max_columns', None)

#load data
df_skills = pd.read_csv("job_skills.csv")
df_posts  = pd.read_csv("linkedin_job_postings.csv")

#inspecting data
print(df_posts.head())
print(df_posts.tail())
print(df_posts.info())
print(df_posts.columns)

#data cleaning

# mask = df_posts.isnull()
# print(mask)
print(df_posts.isnull().sum())
df_posts.dropna(inplace=True)
print(df_posts.isnull().sum())
# company_count= df_posts["company"].value_counts()
# print(company_count)
job_location = df_posts["job_location"].value_counts()
print(job_location)

del df_posts["got_summary"]
del df_posts["got_ner"]
del df_posts["is_being_worked"]

print(df_posts.duplicated(subset=df_posts.columns))
df_posts.drop_duplicates(subset=df_posts.columns,inplace=True)
print(df_posts.shape)


# uniq_job_link = df_posts["job_link"].unique()
# print(uniq_job_link.size)
# print(df_posts.nunique())
# job_link               1348424
# last_processed_time     722737
# job_title               584534
# company                  90604
# job_location             29153
# first_seen                   6
# search_city               1018
# search_country               4
# search_position           1993
# job_level                    2
# job_type                     3
# dtype: int64

# print(df_posts.head())
df_posts["last_processed_time"] = pd.to_datetime(df_posts["last_processed_time"],errors="coerce")

df_posts["times"] = df_posts["last_processed_time"].dt.time
df_posts["Date"] = df_posts["last_processed_time"].dt.date

df_posts["hour"] = df_posts["last_processed_time"].dt.hour
df_posts["day_of_week"] = df_posts["last_processed_time"].dt.day_name()
df_posts["month"] = df_posts["last_processed_time"].dt.month
print(df_posts['Date'].nunique())
print(df_posts['Date'].value_counts())

df_posts.drop(columns=["last_processed_time"], inplace=True)
# print(df_posts.head())

df_posts["job_title"] = df_posts["job_title"].str.lower().str.strip()
# print(df_posts["job_title"].head())


#top 10 jobs
top_jobs = df_posts["job_title"].value_counts().head(10)
# print(top_jobs)

plt.figure(figsize=(10,6))
plt.barh(top_jobs.index,top_jobs.values,color="steelblue")
plt.title("Top 10 Most Posted Job Titles")
plt.xlabel("Number of Postings")
plt.ylabel("Job Title")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

#top 10 companies
top_companies =df_posts["company"].value_counts().head(10)
# print(top_companies)

plt.figure(figsize=(10,6))
plt.barh(top_companies.index,top_companies.values,color="mediumseagreen")
plt.title("Top 10 Companies by Job Postings")
plt.xlabel("Number of Postings")
plt.ylabel("Company")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

job_types = df_posts["job_type"].value_counts()
# print(job_types)

#top 10 job locarions
top_job_locations = df_posts["job_location"].value_counts().head(10)
# print(top_job_locations)

plt.figure(figsize=(11,6))
bars = plt.barh(top_job_locations.index, top_job_locations.values, color="mediumslateblue")
plt.title("Top 10 Job Locations by Number of Postings")
plt.xlabel("Number of Postings")
plt.ylabel("Job Location")
plt.gca().invert_yaxis()
for bar in bars:
    width = bar.get_width()
    plt.text(width + 200, bar.get_y() + bar.get_height()/2, str(width), va='center')
plt.tight_layout()
plt.show()

job_position = df_posts["job_level"].value_counts()
# print(job_position)


# daily_trend = df_posts.groupby("Date").size()
# plt.figure(figsize=(12,5))
# plt.plot(daily_trend.index.strftime('%m-%d'), daily_trend.values, marker='o')
# plt.title("Daily Job Posting Trend")
# plt.xlabel("Date")
# plt.ylabel("Number of Jobs")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1000)}K'))
# plt.show()

#number og job postings by days of week/Which day has the higher number of job postings?
order = ["Friday","Saturday","Sunday"]
day_counts = df_posts["day_of_week"].value_counts().reindex(order, fill_value=0)
plt.figure(figsize=(7,7))
plt.pie(day_counts.values,labels=day_counts.index,autopct="%1.1f%%",startangle=90,colors=["#66b3ff", "#99ff99", "#ffcc99"],explode=(0.05, 0.05, 0.05))
plt.title("Job Postings Distribution for Friday, Saturday, Sunday")
plt.tight_layout()
plt.show()

#hourly trend
#shows at what time a most of the jobs are posted
hour_counts = df_posts["hour"].value_counts().sort_index()

plt.figure(figsize=(10,5))
plt.plot(hour_counts.index, hour_counts.values, marker='o', linestyle='-', color='mediumseagreen')
plt.title("Hourly Job Postings")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Jobs")
plt.xticks(range(0,24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

#job type vs job level
cross_tab = pd.crosstab(df_posts["job_type"], df_posts["job_level"])
cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0)
cross_tab_percent.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Job Type vs Job Level (Percentage)")
plt.ylabel("Proportion")
plt.xticks(rotation=45)
plt.legend(title="Job Level")
plt.show()

#top job skills
df_skills["job_skills"] = df_skills["job_skills"].fillna("").str.lower().str.strip()
df_skills["job_skills"] = df_skills["job_skills"].str.split(",")
df_skills_exploded = df_skills.explode("job_skills")
df_skills_exploded["job_skills"] = df_skills_exploded["job_skills"].str.strip()
df_skills_exploded = df_skills_exploded[df_skills_exploded["job_skills"] != ""]

df_skills_exploded.drop_duplicates(inplace=True)

# print("Unique skills:", df_skills_exploded["job_skills"].nunique())
# print(df_skills_exploded["job_skills"].value_counts().head(20))

top_skills = df_skills_exploded["job_skills"].value_counts().head(20)
plt.figure(figsize=(10,8))
plt.barh(top_skills.index, top_skills.values, color='skyblue')
plt.xlabel("Frequency")
plt.title("Top 20 Most In-Demand Skills")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
