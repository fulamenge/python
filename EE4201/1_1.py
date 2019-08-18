# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '../../../../Downloads'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# ### This tutorial is modified from: https://www.dataquest.io/blog/jupyter-notebook-tutorial/

#%%
print('Hello World!')


#%%
import time
time.sleep(5)


#%%
def say_hello(recipient):
    return 'Hello, {}!'.format(recipient)
say_hello('EE4211 Students')

#%% [markdown]
# # Intro to Markdown (This is a level 1 heading)
# ## This is a level 2 heading
# This is some plain text that forms a paragraph.
# Add emphasis via **bold** and __bold__, or *italic* and _italic_.
# Paragraphs must be separated by an empty line.
# 
# - Sometimes we want to include lists.
#     - Which can be indented.
# 
# 
# 1. Lists can also be numbered.
# 2. [It is possible to include hyperlinks](https://www.ece.nus.edu.sg/stfpage/motani/)
# 3. You can add images too: <img src="fullcolorlogo.jpg" alt="Drawing" style="width: 100px;"/>

#%%
import numpy as np
def square(x):
    return x * x


#%%
x = np.random.randint(1, 10)
y = square(x)
print('%d squared is %d' % (x, y))

#%% [markdown]
# Let get some data from [Fortune 500](http://archive.fortune.com/magazines/fortune/fortune500_archive/full/2005/) companies spanning over 50 years since the list’s first publication in 1955, put together from Fortune’s public archive. You can get a CSV of the data [at this link](https://s3.amazonaws.com/dq-blog-files/fortune500.csv).
# 
# 

#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


#%%
df = pd.read_csv('fortune500.csv')


#%%
df.head()


#%%
df.tail()


#%%
#Let’s rename those columns so we can refer to them later.
df.columns = ['year', 'rank', 'company', 'revenue', 'profit']


#%%
len(df)


#%%
df.dtypes


#%%
non_numberic_profits = df.profit.str.contains('[^0-9.-]')
df.loc[non_numberic_profits].head()


#%%
# How much bad data do we have?
round(100*len(df.profit[non_numberic_profits])/len(df),2)


#%%
bin_sizes, _, _ = plt.hist(df.year[non_numberic_profits], bins=range(1955, 2006))


#%%
#Let's remove the bad rows
df = df.loc[~non_numberic_profits]
df.profit = df.profit.apply(pd.to_numeric)


#%%
len(df)


#%%
df.dtypes


#%%
group_by_year = df.loc[:, ['year', 'revenue', 'profit']].groupby('year')
avgs = group_by_year.mean()
x = avgs.index
def plot(x, y, ax, title, y_label):
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.plot(x, y)
    ax.margins(x=0, y=0)


#%%
# Let's plot profits
y1 = avgs.profit
fig, ax = plt.subplots()
plot(x, y1, ax, 'Increase in mean Fortune 500 company profits from 1955 to 2005', 'Profit (millions)')


#%%
# Let's plot revenues
y2 = avgs.revenue
fig, ax = plt.subplots()
plot(x, y2, ax, 'Increase in mean Fortune 500 company revenues from 1955 to 2005', 'Revenue (millions)')


#%%
# A more complex plot, code taken from StackOverflow: https://stackoverflow.com/a/47582329/604687
def plot_with_std(x, y, stds, ax, title, y_label):
    ax.fill_between(x, y - stds, y + stds, alpha=0.2)
    plot(x, y, ax, title, y_label)

fig, (ax1, ax2) = plt.subplots(ncols=2)
title = 'Increase in mean and std Fortune 500 company %s from 1955 to 2005'
stds1 = group_by_year.std().profit.values
stds2 = group_by_year.std().revenue.values
plot_with_std(x, y1.values, stds1, ax1, title % 'profits', 'Profit (millions)')
plot_with_std(x, y2.values, stds2, ax2, title % 'revenues', 'Revenue (millions)')
fig.set_size_inches(14, 4)
fig.tight_layout()


