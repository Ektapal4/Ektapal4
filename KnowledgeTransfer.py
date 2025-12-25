import pandas as pd

def read_knowledge():
    fpath = "static/Knowledge"
    k_df = pd.read_excel(fpath + "/MH_Knowledgebase.xlsx")
    k_dict = k_df.to_dict(orient="records")
    return k_dict
