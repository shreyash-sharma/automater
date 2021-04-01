import subprocess


def run_code(file_name):
    cmd = " python ../files/"+file_name+".py 1"
    subprocess.call(cmd, shell=True)
    
    
#if __name__ == "__main__":
#    run_code("Macro_1")