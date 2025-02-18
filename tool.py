import subprocess, os, datetime

location = None

#filepaths of the tools
MFTECMD = r"MFTECmd.exe"
EVTXECMD = r"EvtxeCmd.exe"
RECMD = r"RECmd.exe"
filefolder = "ExtractedFiles"

#csv/csvf, json/jsonf
filetype = "csv"
dateTime = "yyyy-MM-dd HH:mm:ss.fffffff"
drive = "c:\\"
mftLocation = "c:\\$MFT"
batchPath = None
mapPath = None

def create_unique_directory(base_path="ExtractedFiles\\"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_name = os.path.join(base_path, timestamp)
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

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
        print("[5] Map (EVTXECMD): " + batchPath)
    
    print("[6] MFT Location: " + mftLocation)
    
    print("[7] Execute")
        
    print("Location to Save \"ExtractedFiles\"")
        
def recmd():
    os.system("RECmd.exe --help")
    # os.system(RECMD)
    # print("Enter \"help\" to show inputs")
    # print("Enter \"exit\" to return to main menu")
    # while(True):    
    #     prompt = input("Command: ")
        
    #     if prompt == "exit":
    #         return
    #     elif prompt == "help":
    #         os.system(RECMD)
    #     else:
    #         os.system(RECMD + " " + prompt)
    return

def evtxecmd():
    os.system("EvtxeCmd.exe --help")
    return

def mftecmd():
    os.system("MFTECmd.exe --help")
    return


def execute():
    global batchPath
    global mapPath
    global mftLocation
    
    folderpath = create_unique_directory()
    
    #Recmd
    print("Executing RECmd")
    os.mkdir(folderpath + "\\recmd")
    recmdCommand = f"RECmd.exe -d {drive} --bn {batchPath}  --{filetype + " " + folderpath + "\\recmd"}"
    subprocess.Popen(recmdCommand, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
    
    #MFTECmd
    print("Executing MFTECmd")
    os.mkdir(folderpath + "\\mftecmd")
    mftecmdCommand = f"MFTECmd.exe -f {mftLocation}  --{filetype + " " + folderpath + "\\mftecmd"}"
    subprocess.Popen(mftecmdCommand, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    #evtxecmd
    print("Executing EvtxECmd")
    os.mkdir(folderpath + "\\evtxecmd")
    evtxecmdCommand = f"EvtxECmd.exe -d {drive} --{filetype + " " + folderpath + "\\evtxecmd"}"
    subprocess.Popen(evtxecmdCommand, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("All Data are bing Extracted in the background please wait for it to finish.")
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
        in1 = input("Edit Default Config?")
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
            print(batchPath != None)
            if batchPath == None:
                print("Fill up required Configuration")
            else:
                execute()
        else:
            print("Invalid Input!!")
        



def main():
    while(True):
        temp = ""
        print("Mini Project 2")
        print("List of tools combined (3): ")
        print("[1] RECmd")
        print("[2] EVTXCmd")
        print("[3] MFTECmd")
        print("[4] Merged")
        print("[-1] Exit")
        in1 = input("Input: ")
        
        if in1 == "1":
            recmd()
        elif in1 == "2":
            evtxecmd()
        elif in1 == "3":
            mftecmd()
        elif in1 == "4":
            merged()
        elif in1 == "-1":
            break
        else:
            print("Invalid Input!!")
        
    return

if __name__ == "__main__":
    main()
