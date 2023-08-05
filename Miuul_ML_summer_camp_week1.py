""""
******************************* Potential Customer Revenue Calculation with Rule-Based Classification *******************************

 A gaming company wants to create level-based new customer profiles (personas) using some characteristics of its customers and,
 based on these new customer profiles, estimate how much potential revenue new customers from these segments could bring to the company.

 For example, they want to determine the average revenue that a 25-year-old male user from Turkey, who uses IOS, could potentially generate.

"""

#Price: The amount of money spent by the customer.
#Source: The type of device the customer is using.
#Sex: The gender of the customer.
#Country: The country of the customer.
#Age: The age of the customer.

import pandas as pd

df = pd.read_csv(r"C:\Users\iremp\Desktop\persona.csv")

df.info()
df.head()
df.tail()
df.describe().T
df.shape
df.columns
df.index
df.isnull().values.any()

#Total earnings from sales by countries:
df.groupby('COUNTRY')['PRICE'].sum()

#PRICE averages by countries:
df.groupby(['COUNTRY']).agg({'PRICE': 'mean'})

#PRICE averages by SOURCE:
df.groupby(['SOURCE']).agg({'PRICE': 'mean'})

#COUNTRY-SOURCE breakdown of PRICE averages:
df.groupby(['SOURCE', 'COUNTRY']).agg({'PRICE': 'mean'})
agg_df = df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE']).agg({'PRICE': 'mean'})
agg_df.sort_values('PRICE', ascending=False)

#Convert the names in the index to variable names
agg_df = agg_df.reset_index()
agg_df.columns

#Convert the 'AGE' variable into a categorical variable and add it to agg_df
age_cat = [0, 18, 23, 30, 40, agg_df['AGE'].max()]
age_labels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df['AGE'].max())]

pd.cut(agg_df['AGE'], bins=age_cat, labels=age_labels)
agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], bins=age_cat, labels=age_labels)

#Define new level-based customers (personas) and add them to the data set as variables
agg_df.drop(['AGE', 'PRICE'], axis=1).values

list = ['A', 'B', 'C']
'-'.join(list)

agg_df["CUSTOMERS_LEVEL_BASED"] = ["_".join(i).upper() for i in agg_df.drop(['AGE', 'PRICE'], axis=1).values]
agg_df = agg_df[['CUSTOMERS_LEVEL_BASED', 'PRICE']]
agg_df = agg_df.groupby('CUSTOMERS_LEVEL_BASED')['PRICE'].mean().reset_index()
agg_df.head()

#Segment the new customers (Example: USA_ANDROID_MALE_0_18) into 4 segments based on PRICE
#Add the segments to the agg_df with the name 'SEGMENT'
[23, 27, 34, 34, 35, 39, 41, 48]

agg_df['SEGMENT'] = pd.qcut(agg_df.PRICE, q=4, labels=['D', 'C', 'B','A'])
agg_df.groupby('SEGMENT').agg({'PRICE': 'mean'}).reset_index()

#Classify the new incoming customers and predict how much revenue they can generate
# What segment does a 33-year-old Turkish woman, who uses ANDROID, belong to, and what is the expected average revenue she is likely to generate?
new_user = 'TUR_ANDROID_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]

# What segment does a 35-year-old French woman, who uses IOS, belong to, and what is the expected average revenue she is likely to generate?
new_user = 'FRA_IOS_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == 'BRA_ANDROID_FEMALE_0_18']

df[['PRICE', 'AGE']].corr()
