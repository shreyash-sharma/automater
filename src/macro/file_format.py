from datetime import date
today = date.today()
import datetime

def create_code(file_name):
    print("inside createCODE")
    code_file = "../files/"+file_name+".py"
    text_file = "../files/"+file_name+".txt"
    writ = open(code_file, "w")
    
    writ.write("import pyautogui"+"\n")
    writ.write("from time import sleep"+"\n")
    writ.write("def __write__(key):"+"\n")
    writ.write("    pyautogui.typewrite(key)"+"\n")
    writ.write("def __hotkey__(key1,key2):"+"\n")
    writ.write("    pyautogui.hotkey(key1,key2)"+"\n")
    writ.write("def __click__(x1,y1,click):"+"\n")
    writ.write("    pyautogui.click(x=x1,y=y1,button=click)"+"\n")
    
    
    f = open(text_file)
    Lines = f.readlines()
    count = 0
    # Strips the newline character 
    for idx,line in enumerate(Lines):
        #print(Lines[idx+0])
        line=Lines[idx]
        a=int(len(line))
        last = line.find("!")
        time_current = line[0:last].split(":")
        writ.write(line[last+1:a])
        if idx < len(Lines)-1:
            line_next=Lines[idx+1]
            last = line_next.find("!")
            time_next = line_next[0:last].split(":")
            
            #sleep logic
            if int(time_next[1]) > int(time_current[1]):
                diff = int(time_next[1]) - int(time_current[1])
                diff = 60 * diff
                time_next[2] = int(time_next[2]) + diff
            sleep = (int(time_next[2])-int(time_current[2]))
            if sleep == 0:
                sleep = 1
            writ.write("sleep("+str(sleep)+")"+"\n")
        #pp = pp.replace(pp[0:last], "") 
    
        
    writ.close()