#!/usr/bin/env python
# coding: utf-8

# # import necessary libraries
# 

# In[5]:


import pandas as pd
import os


# # merging 12 month sale data into single file

# In[6]:


df= pd.read_csv("./Sales_Data/Sales_April_2019.csv")
files=[file for file in os.listdir('./Sales_Data')]
all_month_data=pd.DataFrame()
for file in files:
    df= pd.read_csv("./Sales_Data/"+file)
    all_month_data=pd.concat([all_month_data, df])
    
all_month_data.to_csv("all_data.csv", index=False)


# In[ ]:





# In[ ]:





# # Task1:read in update dataframe

# In[7]:


all_data=pd.read_csv("all_data.csv")
all_data.head()


# # clean up the data!

# while performing the operation we find the error .Based on that error , we can clean up the data (from my point of view)

# drop rows of NAN

# In[9]:


nan_df=all_data[all_data.isna().any(axis=1)]
nan_df.head()
all_data=all_data.dropna(how='all')
all_data.head()


# # find 'or 'and delete  it

# In[15]:


all_data=all_data[all_data['Order Date'].str[0:2] !='Or']


# #convert column to the correct type
# 

# In[19]:


all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered']) #make int
all_data['Price Each']=pd.to_numeric(all_data['Price Each']) #make float
 
    

Augment data with additional column

# # Task2- add month column

# In[20]:


all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
all_data.head()


# In[ ]:





# In[ ]:





# # add sales column

# In[21]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data.head()


# # add a city column

# In[39]:


#let's use .apply()
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City']=all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
 
all_data.head()


# # Q-1. what was the best month for sale? How much was earned that month?

# In[23]:


results=all_data.groupby('Month').sum()


# In[26]:


import matplotlib.pyplot as plt
months= range(1, 13)
plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# # what city has the highest number of sale?

# In[41]:


results=all_data.groupby('City').sum()
results


# In[45]:


import matplotlib.pyplot as plt

cities=[city for city ,df in all_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical',size=8 )
plt.ylabel('Sales in USD ($)')
plt.xlabel('City name')
plt.show()


# # what time should we display advertisement to maximize likelihood of customer's buying product?

# In[47]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data['Hour']= all_data['Order Date'].dt.hour
all_data['Minute']=all_data['Order Date'].dt.minute
all_data.head()


# In[53]:


hours=[hour for hour ,df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hours')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()

#my recommendation to display advertizement around(11am) or 7pm(19) to maximize likelehood of buying product


# # what products are most often sold together?

# In[58]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID', 'Grouped']].drop_duplicates()     #to remove duplicate
df.head()


# In[60]:


from itertools import combinations
from collections import Counter
count=Counter()
for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list, 2)))     #here 2 is the item and it can vary , if you want to keep it 3 or 4 you can do that.
for key, value in count.most_common(10):
    print(key, value)


# # Q-5 what product sold the most ? why do you think it sold the most?

# In[61]:


all_data.head()


# In[65]:


product_group= all_data.groupby('Product')
quantity_ordered=product_group.sum()['Quantity Ordered']
products=[product for product, df in product_group]
plt.bar(products, quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Ordered')
plt.xticks(products, rotation='vertical', size=8)
plt.show()


# In[70]:


prices=all_data.groupby('Product').mean()['Price Each'] # just google how to plot second y axis

fig, ax1=plt.subplots()

ax2=ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices,'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.show()
 


# In[ ]:




