import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

TEMP_SAVE_FILENAME = 'a.jpg'

def get_df(filepath):
    df = pd.read_csv(filepath)\
        .drop_duplicates()\
        .dropna()

    # Assuming label is end of the columns
    label_column = df.columns[-1]

    label_encoder = LabelEncoder()

    for col in df.select_dtypes(include=['category', 'object']):
        if col != label_column:
            df[col] = label_encoder.fit_transform(df[col])

    return df, label_column


# To find out count of unique value of each column
def summary(df):
    summ = pd.DataFrame(df.dtypes, columns=['data type'])
    summ['#missing'] = df.isnull().sum().values
    summ['%missing'] = df.isnull().sum().values / len(df)* 100
    summ['#unique'] = df.nunique().values
    desc = pd.DataFrame(df.describe(include='all').transpose())
    summ['min'] = desc['min'].values
    summ['max'] = desc['max'].values
    return df.shape, summ

# Correlation
def correlation(df, label=''):
    plt.figure(figsize=(12, 12))
    colormap = plt.cm.gist_heat
    plt.title(f'Correlation Plot')
    sns.heatmap(df.select_dtypes('number').corr(), linewidths=0.1, vmax=0.5, cmap=colormap, linecolor='white',
                      annot=True)
    plt.savefig(TEMP_SAVE_FILENAME)
    return True

# CrossTab
def crosstab(df, label):
    less_unique_col = [column for column in df.columns if df[column].nunique() < 5 and column != label]
    total_plots = len(less_unique_col)
    if total_plots >= 1:
        c_cnt = 3
        r_cnt = math.ceil(total_plots / c_cnt)
        plt.figure(figsize=(12, 12))

        for idx, cur_col in enumerate(less_unique_col):
            plt.subplot(r_cnt, c_cnt, idx % total_plots + 1)
            sns.heatmap(data=pd.crosstab(df[cur_col], df[label], normalize='index'), annot=True, fmt='.2f',
                        cmap=sns.color_palette("Blues", as_cmap=True))
            plt.title(f"{cur_col} vs {label}")

        plt.tight_layout()
        plt.savefig(TEMP_SAVE_FILENAME)
        return True
    else:
        return False

# Boxplot between Target and Numeric Variables
def scatter_box_plot(df, label):
    more_unique_col = [column for column in df.columns if df[column].nunique() > 10 and column != label]
    total_plots = len(more_unique_col)
    if total_plots >= 1:
        c_cnt = 3
        r_cnt = math.ceil(total_plots / c_cnt)

        plt.figure(figsize=(12, 12))

        for idx, cur_col in enumerate(more_unique_col):
            plt.subplot(r_cnt, c_cnt, idx % total_plots + 1)
            sns.boxplot(x=label, y=cur_col, data=df, palette='dark:#82B0D2', hue=label)

            plt.title(f"{cur_col} : {label}")

        plt.tight_layout()
        plt.savefig(TEMP_SAVE_FILENAME)
        return True
    else:
        return False
        
# Distribution of Label
def distribution_label(df, label, title='Train'):
    label_series = df[label].value_counts()
    lbls = list(label_series.keys())

    f, ax = plt.subplots(1, 2, figsize=(12, 5))
    plt.subplots_adjust(wspace=0.3)
    #
    for col in lbls:
        ax[0].pie(label_series, labels=lbls,
                    startangle=90, frame=True, radius=1.2,
                    explode=([0.05]*(len(lbls)-1) + [.2]),
                    wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                    textprops={'fontsize': 10, 'weight': 'bold'},
                    autopct='%1.f%%',
                    shadow=True,
                    )

        sns.barplot(x=label_series, y=label_series.index, ax=ax[1], orient='horizontal', color='#82B0D2')

        ax[1].spines['top'].set_visible(False)
        ax[1].spines['right'].set_visible(False)
        ax[1].tick_params(axis='x', which='both', bottom=False, labelbottom=False)

        for i, v in enumerate(label_series):
            ax[1].text(v, i+0.1, str(v), color='black', fontweight='bold', fontsize=14)

        # Adding labels and title
        plt.setp(ax[1].get_yticklabels(), fontweight="bold")
        plt.setp(ax[1].get_xticklabels(), fontweight="bold")
        ax[1].set_xlabel(col, fontweight="bold", color='black', fontsize=14)

    f.suptitle(f'{title} Dataset Distribution of {col}', fontsize=20, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig(TEMP_SAVE_FILENAME)
    return True


CHART_TYPE_DICT = {
    'Correlation': correlation,
    'CrossTab': crosstab,
    'Distribution of Label': distribution_label,
    'Plot Count': scatter_box_plot,
}

df, last_column = get_df('sample_dataset/train.csv')
shape, summ = summary(df)
summ.style.background_gradient(cmap='Blues')