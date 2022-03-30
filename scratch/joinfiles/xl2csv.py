# importing pandas as pd
import pandas as pd

# read an excel file and convert
# into a dataframe object
df = pd.DataFrame(pd.read_excel(r'C:\Users\2003640\Desktop\TextAnalysisNlp\static\csv_files\rawdata\train_data.xlsx'))

# show the dataframe
print(df.shape)
df.to_csv(r'C:\Users\2003640\Desktop\TextAnalysisNlp\static\csv_files\rawdata\train_data.csv')
print("over")