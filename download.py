import subprocess
x = subprocess.check_output("curl -so /dev/null -w '%{time_total}\n'  http://10.8.3.145:5000/downloads/10",shell=True)
y = subprocess.check_output("curl -so /dev/null -w '%{time_total}\n'  http://10.8.3.145:5000/downloads/50",shell=True)
z = subprocess.check_output("curl -so /dev/null -w '%{time_total}\n'  http://10.8.3.145:5000/downloads/100",shell=True)
print (float(z)+float(y)*2+float(x)*10)/3