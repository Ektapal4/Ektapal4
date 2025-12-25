import pandas as pd
from flask import session
import os

def save_result():
    marks = session.get("total_marks", 0)
    mental_status = ""

    if 0 < marks <= 10:
        mental_status = "Mentally Fit"
    elif 11 <= marks <= 20:
        mental_status = "Moderate"
    elif 21 <= marks <= 30:
        mental_status = "Need More Attention"
    elif 31 <= marks <= 40:
        mental_status = "Mentally not fit"
    elif 41 <= marks <= 45:
        mental_status = "Critical Issue"
    else:
        mental_status = "More critical"
    
    fpath = "static/Knowledge"
    filepath = os.path.join(fpath, "MH_result.xlsx")

    if os.path.exists(filepath):
        result_df = pd.read_excel(filepath)
    else:
        result_df = pd.DataFrame(columns=["Name", "Email", "Gender", "Age", "Score", "Status"])

    new_row = {
        "Name": session.get("name"),
        "Email": session.get("email"),
        "Gender": session.get("gender"),
        "Age": session.get("age"),"Score": marks,"Status": mental_status
    }

    new_row_df = pd.DataFrame([new_row])
    new_result_df = pd.concat([result_df, new_row_df], ignore_index=True)
    new_result_df.to_excel(filepath, index=False)
   

    # Clear session
    session.pop("name", None)
    session.pop("email", None)
    session.pop("gender", None)
    session.pop("age", None)
    #session.pop("total_marks", None)
