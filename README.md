# python
 Example:
 
check the dataset for data quality by six dimentions (uniqueness, timeliness, completeness, validity, consistency and accuracy) <br />
We take dataset from kaggle which contains information about parking in NYC </br>
![table](https://github.com/ViktorKorolko/data-branch/tree/python/img/parking.jpg)

script tested on [kaggle](https://www.kaggle.com/code/viktorkorolko/task03)
```
import pandas as pd
import re

'TASK 3'
'Declaring variables for calculating total rows, correct rows and wrong rows in six dimensions'
'Values for Task 1'
total1 = 0
total2 = 0
total3 = wrong3 = correct3 = 0
total4 = wrong4 = correct4 =null4= 0
total5 = wrong5 = correct5 = 0
total6 = wrong6 = correct6=null6 = 0
wrongdata1 = pd.DataFrame()
wrongdata2 = pd.DataFrame()
wrongdata3 = pd.DataFrame()
wrongdata4 = pd.DataFrame()
wrongdata5 = pd.DataFrame()
wrongdata6 = pd.DataFrame()

def uniqueness():
    'Uniqueness: for one Plate ID mast be one Vehicle Make'
    global total1,wrongdata1
    total1+=data[['Plate ID']].count()
    doubletemp=data.groupby(['Plate ID', 'Vehicle Make']).size().reset_index().rename(columns={0:'Count'})
    doubletemp=doubletemp.loc[(doubletemp['Count']>1)]
    wrongdata1=pd.concat([wrongdata1,doubletemp[doubletemp.duplicated(['Plate ID'], keep=False)]])
                 
def timeliness():
    'Timeliness: "Date First Observed" must be not later than "Issue Date"'
    global total2,wrongdata2
    data['Issue Date'] = pd.to_datetime(data['Issue Date'])
    data.loc[(data['Date First Observed'] == 0), ['Date First Observed']] =None
    for line in data['Issue Date']:
        total2 += 1
    wrongdata2=pd.concat([wrongdata2,data.loc[(data['Date First Observed']>20171231)]])
    
def completeness():
    'Completeness: The "Plate ID" exist for every row.'
    global total3,wrong3,correct3,wrongdata3
    for line in data['Plate ID']:
        total3 += 1
        if pd.isnull(line):
            wrong3 += 1
        else:
            correct3 += 1
    wrongdata3=pd.concat([wrongdata3,data.loc[(data['Plate ID'].isnull())]])
    
def validity():
    'Validity: Column "Violation In Front Of Or Opposite" mast have values O or P'
    global total4,correct4,wrong4, null4,wrongdata4
    dataclear = pd.DataFrame() 
    dataclear=data[(data['Violation In Front Of Or Opposite']!='O')&
                   (data['Violation In Front Of Or Opposite']!='P')]
    for line in dataclear['Violation In Front Of Or Opposite']:
        total4 += 1
        if line=='0' or line=='P':
            correct4 += 1
        elif pd.isnull(line):
            null4+=1
        else:
            wrong4 += 1
    wrongdata4=pd.concat([wrongdata4,dataclear.loc[(dataclear['Violation In Front Of Or Opposite'].notnull())]])          
    
def consistency():
    'Consistency: The value "Issue Date" must be specified'
    global total5,wrong5,correct5,wrongdata5
    for line in data['Issue Date']:
        total5 += 1
        if pd.isnull(line):
            wrong5 += 1
        else:
            correct5 += 1
    wrongdata5=pd.concat([wrongdata5,data.loc[(data['Issue Date'].isnull())]])
    
def accuracy():
    'Accuracy: In a record of "Date First Observed" month not vore then 12, days no more than 31'
    global total6,wrong6,correct6,null6,wrongdata6
    wronglist=[]
    corlist=[]
    data['Date First Observed']=data['Date First Observed'].astype(str)
    expr = re.compile(r'^....(?:0[1-9]|[12][0-9]|3[01])(?:0[1-9]|[12][0-9]|3[01])')
    date='^....(?:0[1-9]|[12][0-9]|3[01])(?:0[1-9]|[12][0-9]|3[01])'
    
    for line in data['Date First Observed']:
        total6 += 1
        if re.findall(expr, line):
            correct6 += 1
        elif line=='0':
            null6+=1
        else:
            wrong6 += 1 
    wrongdata6=pd.concat([wrongdata6,data[data['Date First Observed'].str.count(date)==0]]) 
    
'Main part: reading csv file with chunk'
url='/kaggle/input/nyc-parking-tickets/Parking_Violations_Issued_-_Fiscal_Year_2017.csv'            
for data in pd.read_csv(url, chunksize=500000):
    'Functions executing Task 1'
    uniqueness()
    timeliness()
    completeness()
    validity()
    consistency()
    accuracy()
    
'OUTPUTS'
print('TASK 3')

'Output Uniqueness'
print('\n\nUniqueness: No double rows, no duplicates')
print('Table with a wrong "Plate ID" and "Vehicle Make"')
print(wrongdata1[['Plate ID', 'Vehicle Make']])
print(wrongdata1['Plate ID'].count())

'Output Timeliness'
print('\n\nTimeliness: "Date First Observed" must be not later than "Issue Date"')
print('total rows:', total2, 'wrong rows:', wrongdata2['Issue Date'].count())
print(wrongdata2[['Summons Number','Plate ID','Issue Date','Date First Observed']])

'Output Completeness'
print('\n\nCompleteness: The "Plate ID" exist for every row.')
print('total rows:', total3, 'correct rows:', correct3, 'wrong rows:', wrong3)
print(wrongdata3[['Summons Number','Plate ID']])

'Output Validity'
print('\n\nValidity: Column "Violation In Front Of Or Opposite" mast have values O or P')
print('total rows:', total4, 'correct rows:', correct4,'empty rows',null4, 'wrong rows:', wrong4)
print('Table with wrong values')
print(wrongdata4[['Summons Number','Violation In Front Of Or Opposite']])

'Consistency'
print('\n\nConsistency: The value "Issue Date" must be specified')
print('total rows:', total5, 'correct rows:', correct5, 'empty rows:', wrong5)
print('Table with an empty cells "Issue value"')
print(wrongdata5[['Summons Number','Plate ID','Issue Date']])

'Output Dimension6: Accuracy'
print('\n\nAccuracy: In a record of "Date First Observed" month not vore then 12, days no more than 31')
print('total rows:', total6, 'correct rows:', correct6, 'wrong rows:', wrong6,'empty rows:', null6)
print(wrongdata6[['Summons Number','Plate ID','Date First Observed'
                 ]].loc[(wrongdata6['Date First Observed']!='0')])
```
Result:
```
/opt/conda/lib/python3.7/site-packages/IPython/core/interactiveshell.py:3361: DtypeWarning: Columns (18,38) have mixed types.Specify dtype option on import or set low_memory=False.
  if (await self.run_code(code, result,  async_=asy)):
TASK 3


Uniqueness: No double rows, no duplicates
Table with a wrong "Plate ID" and "Vehicle Make"
       Plate ID Vehicle Make
1835    12003MJ        DODGE
1836    12003MJ        NS/OT
1839    12005MJ        DODGE
1840    12005MJ        NS/OT
1841    12006MJ        DODGE
...         ...          ...
244663   XX478C        FRUEH
245816    YH101        LEXUS
245817    YH101        TOYOT
247444  ZHF9386        INTER
247445  ZHF9386        MERCU

[33723 rows x 2 columns]
33723


Timeliness: "Date First Observed" must be not later than "Issue Date"
total rows: 10803028 wrong rows: 20
          Summons Number  Plate ID Issue Date  Date First Observed
168949        1416979281   HKD1260 2017-02-04           20190204.0
1127979       1423984183   17463MD 2017-04-19           20200419.0
2041531       1408927408   55026MB 2017-03-29           20180309.0
2618178       1414159213   61096MC 2016-07-20           20200720.0
3269727       1409785828  F68942ST 2017-01-09           20200109.0
3637125       1407091761   GEZ8940 2016-07-14           20210914.0
3888675       1398922407   32729JZ 2016-10-03           20181003.0
4164159       1419968180    XCVF82 2017-05-17           20200517.0
4751255       1383348390   HGF1842 2016-09-15           20200915.0
6433401       1383348091   DFJ7977 2016-12-10           20201210.0
8017417       1411933163   HFX3107 2016-07-06           20180706.0
8682917       1419968221   GGT5395 2017-05-26           20190526.0
9587897       1413212852   13082MJ 2016-08-09           20180809.0
10547260      1411540906   95085MC 2016-05-31           20220613.0
10801737      1258136168   GNW2311 2018-05-03           20180503.0
10801849      1402295868   PHIL419 2018-05-24           20180524.0
10801865      1405591638   31339LV 2018-05-28           20180528.0
10802271      1408822672   55025MB 2018-11-16           20181116.0
10802275      1416588802   HJV7882 2018-11-17           20181117.0
10802342      1402908544   FDF8144 2018-12-16           20181216.0


Completeness: The "Plate ID" exist for every row.
total rows: 10803028 correct rows: 10802300 wrong rows: 728
          Summons Number Plate ID
11889         8240027763      NaN
28537         8233020280      NaN
35569         8581550060      NaN
36497         7802856115      NaN
47093         7468294598      NaN
...                  ...      ...
10786640      8236026978      NaN
10786641      8236026966      NaN
10786642      8236026954      NaN
10786643      8236026942      NaN
10786644      8236026929      NaN

[728 rows x 2 columns]


Validity: Column "Violation In Front Of Or Opposite" mast have values O or P
total rows: 8691436 correct rows: 1 empty rows 2161235 wrong rows: 6530200
Table with wrong values
          Summons Number Violation In Front Of Or Opposite
4             7868300310                                 F
6             1413609545                                 F
13            1416492320                                 F
14            1413656420                                 F
15            7959486440                                 F
...                  ...                               ...
10803023      1415891400                                 F
10803024      1384716543                                 F
10803025      1413536554                                 F
10803026      1415514203                                 F
10803027      1415995370                                 F

[6530201 rows x 2 columns]


Consistency: The value "Issue Date" must be specified
total rows: 10803028 correct rows: 10803028 empty rows: 0
Table with an empty cells "Issue value"
Empty DataFrame
Columns: [Summons Number, Plate ID, Issue Date]
Index: []


Accuracy: In a record of "Date First Observed" month not vore then 12, days no more than 31
total rows: 10803028 correct rows: 241530 wrong rows: 10561498 empty rows: 0
          Summons Number Plate ID Date First Observed
0             5092469481  GZH7067                 nan
1             5092451658  GZH7067                 nan
2             4006265037  FZX9232                 nan
3             8478629828  66623ME                 nan
4             7868300310  37033JV                 nan
...                  ...      ...                 ...
10803023      1415891400  HGK6453                 nan
10803024      1384716543  GRA6240                 nan
10803025      1413536554   RC8S28                 nan
10803026      1415514203  HGU9544                 nan
10803027      1415995370  GPP1608                 nan

[10561498 rows x 3 columns]
```
