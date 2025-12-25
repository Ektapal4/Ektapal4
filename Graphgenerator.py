import pandas as pd;
import matplotlib.pyplot as plt;
def create_graphs():
    fpath="static/Knowledge";
    result_df=pd.read_excel(fpath+"/MH_result.xlsx");
    #creating genderwise mental health chart
    gender_wise_df=(result_df.groupby(['Gender','Status']).size().sort_index(ascending=True));
    plt.legend(["Gender of participants","Mental Status of Participants"]);
    gender_wise_df.plot(kind='pie',legend="",title="Genderwise Mental Health Chart",ylabel="",figsize=(8,6),
                    colors=["red","blue","green","orange","lime","silver","maroon","orange","gray","navy"]);
    plt.title("Genderwise Mental Health Chart",color="blue",fontsize="10",
          fontweight="bold",fontstyle="oblique",fontfamily="Serif",);
    #save pie chart
    plt.savefig("static/graph/mental_pie.png");
    #Genrating agewise graph
    bins=[10,20,30,40,50,60,125];
    labels_range=["11-20","21-30","31-40","41-50","51-60","61-125"];
    result_df["Age_Range"]=pd.cut(result_df["Age"],bins,labels=labels_range);
    agewise_df=(result_df.groupby(['Age_Range','Status']).size().unstack(sort=True));
    print(agewise_df)
    agewise_df.plot(kind='bar', figsize=(8, 6), colormap="Set2")
    plt.title("Agewise Mental Health Chart",color="maroon",fontsize="20",fontweight="bold",fontstyle="oblique",
          fontfamily="Serif",);
    plt.xlabel("Age");
    plt.ylabel("Mental Status");
    plt.legend(["Critical Issue","Mentally Fit","Mentally Fit","Moderate","More Attention"]);
    plt.savefig("static/graph/mental_bar.png");
