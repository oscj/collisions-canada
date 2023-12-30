import pandas as pd
collision_df = pd.read_excel('./data/y_2019_en.xlsx', sheet_name="in")
collision_df.to_pickle("./data/2019_collisions.pkl")