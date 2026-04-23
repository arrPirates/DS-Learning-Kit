import pandas as pd

#import csv -- include relative file path
df = pd.read_csv('T1_P1/T1_P1_data.csv')

#part one
print(df.shape)
print(df.columns)
print(df.dtypes)
print(df.info())
print(df.describe(include='all'))
# notes:
## several of the columns appear as objects below is what I would expect each column dtype to be:
# user_id                   int64
# signup_date               datetime64
# plan_type                 object
# monthly_fee               float64
# credit_score              int64
# is_active                 bool
# transactions_last_30d     int64
# referral_source           object
# notes                     object

##//##//##//##//##//##//##//##//##

#part two
print(df.isnull().sum())

### personal note -- answers found using print(df['columnName'].value_counts())
# user_id                   two values include "USR" prefix
# signup_date               there appear to be alternative date formats (ex yyyy-mm-dd & mm/dd/yyyy)
# plan_type                 no changes needed
# monthly_fee               remove $ to remove obj
# credit_score              decimal point has no meaning, all xxx.0 (fix optional)
# is_active                 using different boolean types (ex. 0/1 or False/True)
# transactions_last_30d     decimal point has no meaning, all xxx.0 (fix optional)
# referral_source           no changed needed
# notes                     no changed needed

##//##//##//##//##//##//##//##//##

#part three
# user_id                   two values include "USR" prefix
user_id_error = pd.to_numeric(df['user_id'],errors='coerce').isna()
print(df[user_id_error])
df['user_id'] = df['user_id'].str.replace('USR','').astype(int)
# signup_date               there appear to be alternative date formats (ex yyyy-mm-dd & mm/dd/yyyy)
df['signup_date'] = pd.to_datetime(df['signup_date'], format='mixed')
# plan_type                 no changes needed
# monthly_fee               remove $ to remove obj
df['monthly_fee'] = df['monthly_fee'].str.replace('$','').astype(float)
# credit_score              decimal point has no meaning, all xxx.0 (fix optional)
df['credit_score'] = pd.to_numeric(df['credit_score'], errors='coerce')
# is_active                 using different boolean types (ex. 0/1 or False/True)
bool_map = {'Y':True, 'N':False, '1':True, '0':False, 'yes':True, 'no':False, 'True':True, 'False':False}
df['is_active'] = df['is_active'].astype(str).map(bool_map)
# transactions_last_30d     decimal point has no meaning, all xxx.0 (fix optional)
df['transactions_last_30d'] = df['transactions_last_30d'].astype('Int64')
# referral_source           no changed needed
# notes                     no changed needed

##//##//##//##//##//##//##//##//##

#part four
print(df.dtypes)
print(df.isnull().sum())

user_id_error_fixed = pd.to_numeric(df['user_id'],errors='coerce').isna()
print(df[user_id_error_fixed])