import pandas as pd

df = pd.read_csv("graph.txt", header=None, delim_whitespace=True)

df['TrainingError'] = df.loc[:,1].str[11:]
df['CV'] = df.loc[:,2].str[10:]


df = df.ix[:,3:]

print df

df.to_csv('graph_data.csv', index = False)



