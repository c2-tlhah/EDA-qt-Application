# pyqt-dataset-EDA-helper
Using PyQt GUI to show performing Exploratory Data Analysis (EDA) on the CSV dataset used for binary or softmax text classification

I created this based on [this Kaggle notebook](https://www.kaggle.com/code/yaaangzhou/pg-s3-e26-eda-modeling/notebook). Not all the graphs(or charts) were referenced.

# Requirements
* PyQt5>=5.14
* matplotlib
* seaborn
* pandas
* scikit-learn
* jinja2 - For the sole purpose of handling dependencies

## What is EDA?
EDA stands for **Exploratory Data Analysis**. It is an approach to analyzing and visualizing data sets to summarize their main characteristics, often with the help of statistical graphics and other data visualization methods. The goal of EDA is to gain insights into the underlying patterns, relationships, and distributions within the data before applying more formal statistical techniques.

In the context of data science and machine learning, EDA is often one of the initial steps in the data analysis process. It helps analysts and data scientists understand the structure of the data, identify outliers, recognize patterns, and make informed decisions about subsequent modeling or analysis steps. EDA involves techniques such as summary statistics, data visualization (including charts and graphs), and various exploratory statistical methods.

**TL;DR, This is necessary when you have to analyze the dataset to modify it to enhance overall performance of the model based on it.**

## How to Run
1. git clone ~
2. pip install -r requirements.txt
3. python main.py

## Preview
![image](https://github.com/yjg30737/pyqt-dataset-EDA-helper/assets/55078043/087b68e6-731f-4600-9090-8dd2aa53adcf)

There is the table which shows the DataFrame's structure on the left side.

On the right side, you can see the graph. You can switch the type of any graph with the combobox if you want.

## Note

**Depending on the form of the dataset, some graphs may not function properly.** You will see the "Sorry" dialog if that happens.


