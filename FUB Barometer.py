## Analysis + viz on FUB Barometer
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

df_barom = pd.read_csv("reponses-departement-75.csv", sep = ",")

print(df_barom.head())
print(df_barom.tail())
print(df_barom.info())


# resizing the DF
df_barom = df_barom.drop(columns=['uid', 'q01'])


# First viz on evolution for city of Paris
df_barom_evol = df_barom.groupby('q13', as_index=False)['q13'].value_counts()

df_barom_evol['percent'] = ((df_barom_evol['count'] /
                  df_barom_evol['count'].sum()) * 100).round(2)

list_evol = {1: 'Highly deteriorated',
             2: 'Slightly deteriorated',
             3: 'Identical',
             4: 'Slightly ameliorated',
             5: 'Highly ameliorated'}

df_barom_evol['q13_name'] = df_barom_evol['q13'].map(list_evol)

print(df_barom_evol.head())

plt.rcParams["figure.figsize"] = (10, 6)
ax = sns.barplot(x = 'q13_name', y = 'percent', data = df_barom_evol, errorbar=('ci', False))
ax.bar_label(ax.containers[0], label_type='edge',fmt='%.1f%%')


plt.xlabel("Situation")
plt.ylabel("%")

plt.title("General evolution score")

plt.show()


# Second viz on general score and scores on five topics from barometer
General_feeling = df_barom[['q14', 'q15', 'q16', 'q17','q18','q19']].sum().sum() / (9116*6)
Security = df_barom[['q20', 'q21', 'q22', 'q23','q24','q25']].sum().sum() / (9116*6)
Comfort = df_barom[['q26', 'q27', 'q28', 'q29','q30']].sum().sum() / (9116*5)
Efforts = df_barom[['q31', 'q32', 'q33', 'q34']].sum().sum() / (9116*4)
Services_and_parking_lots = df_barom[['q35', 'q36', 'q37', 'q38','q39']].sum().sum() / (9116*5)
Global_score = df_barom[['q14', 'q15', 'q16', 'q17','q18','q19','q20', 'q21', 'q22', 'q23','q24','q25','q26', 'q27', 'q28', 'q29','q30','q31', 'q32', 'q33', 'q34','q35', 'q36', 'q37', 'q38','q39']].sum().sum() / (9116*26)

print(General_feeling)
print(Security)
print(Comfort)
print(Efforts)
print(Services_and_parking_lots)
print(Global_score)


# initialize data of lists
data = {'Topics': ['General feeling','Security','Comfort','Efforts', 'Services and parking lots', 'Global score'],
        'Score': [3.27,3.06,3.31,3.61,3.40,3.31]}
 
# Create DataFrame
df_barom_gen = pd.DataFrame(data)
df_barom_gen.head()

# Create plot
plt.rcParams["figure.figsize"] = (12, 6)
ax = sns.barplot(x = 'Topics', y = 'Score', data = df_barom_gen, errorbar=('ci', False))
ax.bar_label(ax.containers[0], label_type='edge')

plt.ylim(0, 6)

plt.xlabel("")
plt.ylabel("Score")

plt.title("Barometer general results overview")

plt.show()
