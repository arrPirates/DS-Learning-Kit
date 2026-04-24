import pandas as pd

df = pd.read_csv('T1/T1_P2/T1_P2_data.csv')

#---------------------------------------------
print('Part 1 — Load and Setup')
#---------------------------------------------

df['txn_date'] = pd.to_datetime(df['txn_date'])
print(df.info())

#---------------------------------------------
print('Part 2 — Boolean Indexing')
#---------------------------------------------

completed_amt100Plus = df[(df['amount'] > 100) & (df['status'] == 'completed')]
print(completed_amt100Plus.head())
print(len(completed_amt100Plus))

eastWest_flagged = df[((df['region'] == 'East')|( df['region'] == 'West')) & (df['is_flagged'] == True)]
print(eastWest_flagged)

foodTransport_amt20under = df[((df['category'] == 'food')|( df['category'] == 'transport')) & (df['amount'] < 20)]
print(foodTransport_amt20under)
print(len(foodTransport_amt20under))

merchant_isNull = df[df['merchant'].isna()]
print(merchant_isNull)

#---------------------------------------------
print('Part 3 — .query() Equivalents')
#---------------------------------------------

completed_amt100Plus_query = df.query("amount > 100 and status == 'completed'")
print(len(completed_amt100Plus))
print(len(completed_amt100Plus_query))

south_nonFlag_nonPend_amt50plus = df.query("is_flagged == False and status != 'pending' and amount > 50 and region == 'South'")
print(south_nonFlag_nonPend_amt50plus)

#---------------------------------------------
print('Part 4 — Advanced Filtering')
#---------------------------------------------

userId_filter = df[df['user_id'].isin([1001, 1003, 1005])]
print(userId_filter)
print(len(userId_filter))

merchant_containPay = df[df['merchant'].str.contains('pay', case=False, na=False)]
print(merchant_containPay)

q1_2024 = df[(df['txn_date'] >= '2024-01-01') & (df['txn_date'] <= '2024-03-31')]
print(q1_2024)
print(len(q1_2024))

complexFilter = df[(df['txn_date'].isin(q1_2024['txn_date'])) & (df['status'] == 'completed') & (df['is_flagged'] == False) & (df['amount'] >= 50) & df['amount'] <= 500]
print(complexFilter.sort_values(by = 'amount',ascending = False))