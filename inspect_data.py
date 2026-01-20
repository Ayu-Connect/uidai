
import pandas as pd
import os

files = [
    "api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment_1000000_1006029.csv"
]

with open("inspection_result.txt", "w") as f_out:
    for f in files:
        f_out.write(f"--- {f} ---\n")
        if os.path.exists(f):
            try:
                df = pd.read_csv(f)
                f_out.write(f"Columns: {list(df.columns)}\n")
                f_out.write(f"First Row: {df.iloc[0].tolist()}\n")
                f_out.write(f"Shape: {df.shape}\n")
                
                # check for state column anomalies
                if 'state' in df.columns:
                    states = df['state'].unique()
                    f_out.write(f"Unique States (first 10): {states[:10]}\n")
                    # Check if '100000' is in states
                    if 100000 in states or '100000' in states or 100000.0 in states:
                        f_out.write("FOUND 100000 IN STATES!\n")
                        # Show a row where state is 100000
                        bad_row = df[df['state'] == 100000]
                        if bad_row.empty:
                            bad_row = df[df['state'] == '100000']
                        f_out.write(f"Bad Row Sample: {bad_row.iloc[0].tolist() if not bad_row.empty else 'N/A'}\n")
                
            except Exception as e:
                f_out.write(f"Error reading: {e}\n")
        else:
            f_out.write("File not found.\n")
        f_out.write("\n")
