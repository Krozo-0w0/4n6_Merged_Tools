import subprocess, os, datetime, pytz
import pandas as pd
import numpy as np

location = None

MFTECMD = r"MFTECmd.exe"
EVTXECMD = r"EvtxeCmd.exe"
RECMD = r"RECmd.exe"
filefolder = "ExtractedFiles"

filetype = "csv"
dateTime = "%Y-%m-%d %H:%M:%S.%f UTC"
drive = "example_files\\C\\"
mftLocation = "example_files\\C\\$MFT"
batchPath = "BatchExamples\\DFIRBatch.reb"
mapPath = ""

def create_unique_directory(base_path="ExtractedFiles\\"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = os.path.join(base_path, timestamp)
    os.makedirs(dir_name, exist_ok=True)
    return dir_name + "\\"

def convert_to_utc(timestamp):
    try:
        local_dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=pytz.UTC)
        return local_dt.strftime(dateTime)
    except Exception as e:
        return "Invalid Timestamp"

def mark_csv(df, mark, filepath):
    df["Artifact Source"] = mark
    df = df.rename(columns={col: col + " " + mark for col in df.columns})
    df.to_csv(filepath, index=False)
    return df

def merge_csv(folderpath):
    print("Merging CSV Files...")
    try:
        df_mfte = pd.read_csv(folderpath + "Individual\\mftecmd.csv", low_memory=False)
        df_evtx = pd.read_csv(folderpath + "Individual\\evtxecmd.csv", low_memory=False)
        df_rec = pd.read_csv(folderpath + "Individual\\recmd.csv", low_memory=False)

        df_mfte["Normalized Timestamp"] = df_mfte["Created0x10"].apply(convert_to_utc)
        df_evtx["Normalized Timestamp"] = df_evtx["TimeCreated"].apply(convert_to_utc)
        df_rec["Normalized Timestamp"] = df_rec["LastWriteTimestamp"].apply(convert_to_utc)

        df_mfte = mark_csv(df_mfte, "(MFTECMD)", folderpath + "Individual\\mftecmd.csv")
        df_evtx = mark_csv(df_evtx, "(EVTXECMD)", folderpath + "Individual\\evtxecmd.csv")
        df_rec = mark_csv(df_rec, "(RECMD)", folderpath + "Individual\\recmd.csv")

        df_merged = pd.concat([df_mfte, df_evtx, df_rec], ignore_index=True)
        df_merged = df_merged[["Normalized Timestamp", "Artifact Source"] + [col for col in df_merged.columns if col not in ["Normalized Timestamp", "Artifact Source"]]]
        df_merged.to_csv(folderpath + "merged_file.csv", index=False)

        print("Merge complete. Saved as merged_file.csv")
    except FileNotFoundError:
        print("Error: One or more CSV files not found.")
    except Exception as e:
        print("Error during merge:", e)

def execute():
    folderpath = create_unique_directory()
    
    print("Executing RECmd...")
    subprocess.Popen(f"RECmd.exe -d {drive} --bn {batchPath} --{filetype} {folderpath}Individual\\ --dt \"{dateTime}\" --csvf recmd.csv", shell=True).wait()
    
    print("Executing MFTECmd...")
    subprocess.Popen(f"MFTECmd.exe -f {mftLocation} -m {mftLocation} --{filetype} {folderpath}Individual\\ --dt \"{dateTime}\" --csvf mftecmd.csv", shell=True).wait()
    
    print("Executing EvtxECmd...")
    subprocess.Popen(f"EvtxECmd.exe -d {drive} --{filetype} {folderpath}Individual\\ {mapPath} --dt \"{dateTime}\" --csvf evtxecmd.csv", shell=True).wait()
    
    print("All data is being extracted, please wait...")
    merge_csv(folderpath)
    print(f"Output folder: {folderpath}")

def main():
    print("DFIR Extraction Tool")
    execute()

if __name__ == "__main__":
    main()
