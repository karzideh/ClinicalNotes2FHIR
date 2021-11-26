import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

merged_data = pd.read_excel(r'dataset\Patient_Records_Training_Mappe_Merged.xlsx')
df = pd.DataFrame(merged_data[merged_data["source"] == "intuitive"]).groupby("disease")

for disease in df:
    colors = {"Y": "blue", "Q": "cyan", "N": "magenta"}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
    fig = plt.figure(figsize=(8, 6))
    Y = mpatches.Patch(color='blue', label='Anwesend')
    Q = mpatches.Patch(color='green', label='Fragwürdig')
    N = mpatches.Patch(color='magenta', label='Abwesend')
    disease[1].groupby('judgment').text.count().plot.bar(ylim=0, color=[N.get_facecolor(), Y.get_facecolor()])
    plt.title(disease[0])
    plt.legend(handles=[Y, N], loc=2)
    plt.ylabel("Anzahl Patienten")
    plt.xlabel("Vorliegen der Erkrankung")
    plt.show()