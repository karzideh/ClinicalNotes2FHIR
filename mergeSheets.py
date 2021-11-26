import pandas as pd

diseases_data = pd.read_excel(r'dataset\Patient_Records_Test_Mappe.xlsx', sheet_name='diseases')
text_data = pd.read_excel(r'dataset\Patient_Records_Test_Mappe.xlsx', sheet_name='doc')
merged_data = text_data[["id", "text"]].merge(diseases_data[["source", "name", "id", "judgment"]], on="id", how="left")
merged_data.to_excel(r'dataset\Patient_Records_Test_Mappe_Merged.xlsx')