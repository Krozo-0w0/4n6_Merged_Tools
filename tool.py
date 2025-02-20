import subprocess, os, datetime
import pandas as pd

location = None

#filepaths of the tools
MFTECMD = r"MFTECmd.exe"
EVTXECMD = r"EvtxeCmd.exe"
RECMD = r"RECmd.exe"
filefolder = "ExtractedFiles"

#csv/csvf, json/jsonf
filetype = "csv"
dateTime = "yyyy-MM-dd HH:mm:ss.fffffff"
drive = "example_files\\C\\"
mftLocation = "example_files\\C\\$MFT"
batchPath = "BatchExamples\\DFIRBatch.reb"
mapPath = None

def create_unique_directory(base_path="ExtractedFiles\\"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = os.path.join(base_path, timestamp)
    os.makedirs(dir_name, exist_ok=True)
    return dir_name + "\\"

def showConfig():
    print("Current Configuration: ")
    print(f"[1] File type (csv or json): {filetype}")
    print(f"[2] Date/Time Format: {dateTime}")
    print(f"[3] Location: {drive}")
    
    if batchPath == None:
        print("[4] Batch (RECmd): Not set (REQUIRED)")
    else:
        print("[4] Batch (RECmd): " + batchPath)
        
    if mapPath == None:
        print("[5] Map (EVTXECMD): Not set")
    else:
        print("[5] Map (EVTXECMD): " + mapPath)
    
    print("[6] MFT Location: " + mftLocation)
    
    print("[7] Execute")
    
    print("[-1] Exit")
        
    print("Location to Save \"ExtractedFiles\"")
        
def execute():
    global batchPath
    global mapPath
    global mftLocation
    
    folderpath = create_unique_directory()
    
    # RECmd
    print("Executing RECmd")
    recmdCommand = f"RECmd.exe -d {drive} --bn {batchPath} --{filetype + ' ' + folderpath + "Individual\\"} --csvf recmd.csv"
    recmdProcess = subprocess.Popen(recmdCommand, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # MFTECmd
    print("Executing MFTECmd")
    mftecmdCommand = f"MFTECmd.exe -f {mftLocation} -m {mftLocation} --{filetype + ' ' + folderpath + "Individual\\"} --csvf mftecmd.csv"
    mftecmdProcess = subprocess.Popen(mftecmdCommand, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # EvtxECmd
    print("Executing EvtxECmd")
    evtxecmdCommand = f"EvtxECmd.exe -d {drive} --{filetype + ' ' + folderpath + "Individual\\"} --csvf evtxecmd.csv"
    evtxecmdProcess = subprocess.Popen(evtxecmdCommand, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("All Data are being Extracted in the background please wait for it to finish.")
    recmdProcess.wait()
    mftecmdProcess.wait()
    evtxecmdProcess.wait()
    
    
    merge_csv(folderpath)
    
    print(f"Output folder: {folderpath}")
    input("Entery anything to continue...")
    

def merged():
    global batchPath
    global mapPath
    global mftLocation
    global drive
    global filetype
    
    while(True):
        os.system('cls')
        showConfig()
        in1 = input("Option: ")
        if "1" == in1:
            in2 = input("[1] csv or [2] json")
            
            if "1" == in2:
                filetype = "csv"
            elif "2" == in2:
                filetype = "json"
            else:
                print("Invalid Input!!")
        elif "2" == in1:
            dateTime = input("DateTime Format: ")
        elif "3" == in1:
            drive = input("Drive: ")
        elif "4" == in1:
            batchPath = input("Find the Batch Files inside the Batch Example folder: ")
        elif "5" == in1:
            mapPath = input("Find in the Map folder")
        elif "6" == in1:
            mftLocation = input("Enter Location of MFT")
        elif "7" == in1:
            if batchPath == None:
                print("Fill up required Configuration")
            else:
                execute()
        elif "-1" == in1:
            break
        else:
            print("Invalid Input!!")
        

def merge_csv(folderpath):
    
    print("Current Working Directory: " + folderpath)

    try:
        
        df = pd.read_csv(folderpath + "Individual\\mftecmd.csv", low_memory=False)
        df2 = pd.read_csv(folderpath + "Individual\\evtxecmd.csv", low_memory=False)
        df3 = pd.read_csv(folderpath + "Individual\\recmd.csv", low_memory=False)  
        
        df4 = pd.merge(df, df2, left_on='Created0x10', right_on='TimeCreated')
        df5 = pd.merge(df3, df4, left_on='LastWriteTimestamp', right_on='LastRecordChange0x10')
        df5.to_csv(folderpath + "merged_file.csv")
      
        print("Done Merge to file \"merged_file.csv\"")
        
    except FileNotFoundError:
        print("Error file1 or file2 doesn't exist please double check")
    except Exception as e:
        print(e)
    return


def main():
    print("Mini Project 2")
    print("List of tools combined (3): ")
    print("1. MFTECmd")
    print("2. EvtxECmd")
    print("3. RECmd")

    merged()


if __name__ == "__main__":
    main()
