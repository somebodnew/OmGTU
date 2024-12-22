import pandas as pd

#pd.describe_option()
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.precision', 3)


testData = { 
    'Name': ['Strom, Mrs. Wilhelm (Elna Matilda Persson)', 'Navratil, Mr. Michel ("Louis M Hoffman")', 'Minahan, Miss. Daisy E'], 
    'Age':  [29, 36.5, 33], 
    'Sex':  ['female', 'male', 'female'] 
}
testdf = pd.DataFrame(testData)
print(testdf,'\n')


titanic1df = pd.read_csv('titanic_csv.csv', delimiter=';')
titanic1df.columns = titanic1df.columns.str.upper()
print(titanic1df,'\n')

titanic2df = pd.read_csv('https://gist.githubusercontent.com/zaryanezrya/8b4ef51c707cb16d5e88a44dc00a1bb2/raw/41230f49c6268e072dbf102672f670be256922ab/gistfile1.txt', delimiter=',')
titanic2df.columns = titanic2df.columns.str.upper()
print(titanic2df,'\n')

titanic_combined = pd.concat([titanic1df, titanic2df], ignore_index=True).drop_duplicates()
titanic_combined.set_index('PASSENGERID', inplace=True)
print(titanic_combined,'\n')

titanic_combined.sort_values(by='PASSENGERID', inplace=True)
print(titanic_combined,'\n')

print(titanic_combined.info(),titanic_combined.describe(),'\n',sep='\n')

titanic_combined.iloc[0], titanic_combined.iloc[2] = titanic_combined.iloc[2].copy(), titanic_combined.iloc[0].copy()
print(titanic_combined,'\n')

titanic_combined['SEX'] = titanic_combined['SEX'].map({'female': 'f', 'male': 'm'})
print(titanic_combined,'\n')

count = titanic_combined.groupby("TICKET").size()
mostbuyedtickets = count[count >= 6].index
print(mostbuyedtickets,'\n')

cabins_titanic1df = titanic_combined[titanic_combined['NAME'].isin(titanic1df['Name']) & titanic_combined['CABIN'].notna()]['CABIN'].unique()
people_in_same_cabins = titanic_combined[titanic_combined['CABIN'].isin(cabins_titanic1df)]
print(people_in_same_cabins,'\n')

titanic_combined['BIRTHYEAR'] = 1912 - titanic_combined['AGE']
print(titanic_combined,'\n')

cabin_counts = titanic_combined.groupby('CABIN').transform('size')
titanic_combined['COMPANION'] = cabin_counts - 1
print(titanic_combined,'\n')


titanic_combined.iloc[0], titanic_combined.iloc[1] = titanic_combined.iloc[1].copy(), titanic_combined.iloc[0].copy()
print(titanic_combined,'\n')


titanic_combined.to_csv('final_titanic.csv', sep=';')

paidthemost = titanic_combined.sort_values(by='FARE', ascending=False).head(10)
print(paidthemost,'\n')

print(titanic_combined.groupby(['SEX', 'SURVIVED']).size().unstack(),'\n')

print(titanic_combined.groupby(['PCLASS', 'SURVIVED']).size().unstack(),'\n')
