import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import normaltest

def group_categories(series, top_n=10, other_label='Другое'):
    top_categories = series.value_counts().nlargest(top_n).index
    return series.apply(lambda x: x if x in top_categories else other_label)

dframe = pd.read_csv('RottenTomatoesMovies.csv') 

print("Первые 5 строк датафрейма:")
print(dframe.head())
print()

print("Последние 5 строк датафрейма:")
print(dframe.tail())
print()

print("Информация о типах данных:")
print(dframe.info())
print()

print("Основная статистическая информация:")
print(dframe.describe(include='all'))
print()

print(f"Количество строк до удаления дубликатов: {dframe.shape[0]}")
dframe = dframe.drop_duplicates()
print(f"Количество строк после удаления дубликатов: {dframe.shape[0]}")

dframe.rename(columns = {"movie_title" : "themovietitle"}, inplace=True)
print(dframe.info())
print()

dframe['genre_Grouped'] = group_categories(dframe['genre'], 10)
dframe['director_Grouped'] = group_categories(dframe['directors'], 10)

plt.figure(figsize=(8, 6))
sns.histplot(data=dframe, x='rating', bins=20, kde=True) 
plt.title("Гистограмма распределения рейтинга")
plt.xlabel("Rating")
plt.ylabel("Количество фильмов")
plt.tight_layout()
plt.savefig('hist_rating.png', dpi=300)  
plt.show()

plt.figure(figsize=(4, 6))
sns.boxplot(y=dframe['rating'])  
plt.title("Boxplot рейтинга")
plt.ylabel("Rating")
plt.tight_layout()
plt.savefig('boxplot_rating.png', dpi=300)
plt.show()

genre_counts = dframe['genre_Grouped'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Распределение фильмов по жанрам")
plt.axis('equal')
plt.tight_layout()
plt.savefig('pie_genre.png', dpi=300)
plt.show()

corr_matrix = dframe.corr(numeric_only=True)
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Тепловая карта корреляции")
plt.tight_layout()
plt.savefig('heatmap_correlation.png', dpi=300)
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=dframe, x='genre_Grouped', hue='director_Grouped')
plt.title("Количество фильмов по жанрам и режиссерам")
plt.xlabel("Жанр")
plt.ylabel("Количество")
plt.xticks(rotation=45)
plt.savefig('countplot_genre_director.png', dpi=300)
plt.show()

missing_values = dframe.isnull().sum()
print("Количество пропусков в каждом столбце:")
print(missing_values[missing_values > 0])

def fill_missing_values(dataframe):
    for column in dataframe.columns:
        if dataframe[column].isnull().sum() > 0:
            if pd.api.types.is_integer_dtype(dataframe[column]):
                median_value = dataframe[column].median()
                dataframe[column].fillna(median_value, inplace=True)
                print(f"Заполнен пропуск в столбце '{column}' медианой: {median_value}")
            elif pd.api.types.is_float_dtype(dataframe[column]):
                mean_value = dataframe[column].mean()
                dataframe[column].fillna(mean_value, inplace=True)
                print(f"Заполнен пропуск в столбце '{column}' средним значением: {mean_value}")
            else:
                mode_value = dataframe[column].mode()[0]
                dataframe[column].fillna(mode_value, inplace=True)
                print(f"Заполнен пропуск в столбце '{column}' модой: {mode_value}")

fill_missing_values(dframe)

missing_values_after = dframe.isnull().sum()
print("Проверка после заполнения пропусков:")
print(missing_values_after[missing_values_after > 0])
