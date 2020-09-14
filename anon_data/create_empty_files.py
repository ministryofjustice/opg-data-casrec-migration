import pandas as pd
import os
import random

def tidy_column_name(col):
    formatted_col = col.replace(' ', '_').replace('.', '_').replace('\n', '')
    return formatted_col

with open("allcsvrows.txt", "r") as f:
    lines = f.readlines()
    for i in range(0, len(lines)):
        line = lines[i]
        if line[:3] == '==>':

            title = line[4:][:-4].split('.')[0]

            file_to_write = os.path.join('data', f'{title}.csv')
            cols = lines[i+1].split(',')
            formatted_cols = [f"{tidy_column_name(x)}" for x in cols]


            data = []
            for i in range(0, 1000):
                fake_data = [f"fake_{x}" for x in formatted_cols]
                fake_data = [x.replace('fake_Sex',random.choice(['M', 'F'])) for x in
                             fake_data]
                data.append(fake_data)

            df = pd.DataFrame(data, columns=formatted_cols)

            df.to_csv(file_to_write,  header=True, index=False)





