import socket
import os
import subprocess
import cookielib 
import urllib2 
import time
import mechanize 
import string
import Tkinter
import tkMessageBox

server_ip = "10.8.17.141:5000"

def checkHotspot():
	with open(os.devnull, 'w') as devnull:
		is_master = subprocess.check_output("iwconfig | grep Master | wc -c",shell = True, stderr=devnull)
	if int(is_master) != 0:
		return True
	else:
		return False

def findmacandssid():
	with open(os.devnull, 'w') as devnull:
		is_master = subprocess.check_output("iwconfig | grep Master ",shell = True, stderr=devnull)
	is_master = is_master.split()	
	with open(os.devnull, 'w') as devnull:
		check_my_mac = subprocess.check_output("ifconfig " + is_master[0] + " | grep HWaddr",shell = True, stderr=devnull)	
	check_my_mac = check_my_mac.split()
	check_my_ssid = subprocess.check_output("nmcli -f SSID dev wifi list",shell = True)
	check_my_ssid = check_my_ssid.split()
	return check_my_mac[4].upper(),check_my_ssid[1]			

def RemoveQuotes(x):
	if x[0] =='\'':
		x = x[1:]
	if x[-1] == '\'':
		x= x[:-1]
	return x
		
top = Tkinter.Tk()
def Mycallback(a,B):
	B.config(state="disabled")
	print "Before using the software: ",a
	available_ap = subprocess.check_output("nmcli -f BSSID,ACTIVE,SIGNAL,SSID dev wifi list | awk '$2 ~ /no/ {print $1,$3,$4}'",shell=True)
	x = subprocess.check_output( "nmcli -f BSSID,ACTIVE,SIGNAL,SSID dev wifi list | awk '$2 ~ /yes/ {print $1,$3,$4}'",shell=True)
	x = x.split()
	x[2] = RemoveQuotes(x[2])
	bssid = x[0]
	ssid = x[2]
	power = x[1]
	available_ap = available_ap.split()
	for i in range(2,len(available_ap),3):
		available_ap[i] = RemoveQuotes(available_ap[i])
	bssid_to_ssid = {}
	ssid_to_bssid = {}
	create_map = subprocess.check_output("nmcli -f BSSID,SSID dev wifi list",shell=True)
	create_map = create_map.split('\n')
	
	for item in create_map[1:-1]:
		item = item.split()
		name=item[1]
		for item2 in item[2:]:
			name = name+"\ "+item2
		name=RemoveQuotes(name)
		name=name.split('\'')
		name1=name[0] 
		for item2 in name[1:]:
			name1 = name1 +"\\'"+item2
		bssid_to_ssid[item[0]] = name1
		if name1 not in ssid_to_bssid.keys():
			ssid_to_bssid[name1]=[item[0]]
		else:	
			ssid_to_bssid[name1].append(item[0])
	
	known_bssid = []
	res12 = subprocess.check_output("ls /etc/NetworkManager/system-connections",shell=True)
	res12=res12.split('\n')

	for _ in res12[0:-1]:
		_=_.split()
		wi=_[0]
		for item2 in _[1:]:
			wi = wi+"\ "+item2
		wi=wi.split('\'')
		wi1=wi[0]
		for item2 in wi[1:]:
			wi1 = wi1+"\\'"+item2
		z=subprocess.check_output("sudo cat /etc/NetworkManager/system-connections/"+wi1+" | grep psk= | wc -c",shell=True)
		z=int(z)
		if(z != 0 and wi1 in ssid_to_bssid.keys()):
			for item1 in ssid_to_bssid[wi1]:
				known_bssid.append(item1)		
	
	my_mac=bssid
	my_ip = subprocess.check_output("ip route get 8.8.8.8 | awk '{print $NF; exit}'",shell=True)
	my_ip=my_ip.split()
	my_ip = my_ip[0]
	url = server_ip + '/' + 'cmac=' + bssid + '&cstr=' + power + '&cname=' + ssid + '&address=' + my_ip +'&opts=' 
	flag = False

	if(available_ap[0] in known_bssid):
		flag = True
		url = url + available_ap[0]  + ',' + available_ap[1] + ','+ available_ap[2]

	for i in range(3,len(available_ap),3):
		if(available_ap[i] in known_bssid and flag):
			url = url + ',' + available_ap[i] + ',' + available_ap[i+1] + ',' + available_ap[i+2] 
		elif(available_ap[i] in known_bssid):
			url = url + available_ap[i] + ',' + available_ap[i+1] + ',' + available_ap[i+2] 
			flag = True	
	print url
	br = mechanize.Browser()
	cookiejar = cookielib.LWPCookieJar() 
	br.set_cookiejar( cookiejar ) 
	br.set_handle_equiv( True ) 
	br.set_handle_redirect( True ) 
	br.set_handle_referer( True ) 
	br.set_handle_robots( False ) 
	br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
	br.open( "http://"+url )
	br.select_form( name="login_form" ) 
	res = br.submit()

	if res.geturl()==("http://"+server_ip+"/success"):
	 	result = res.read()
	 	result = result.split()
	 	if tkMessageBox.askokcancel("Connect to", result):
	 		connect_to = subprocess.check_output("nmcli con up id "+ bssid_to_ssid[result[1]] ,shell=True)
	 		target_ssid = bssid_to_ssid[result[1]]
	 		counter=0
	 		while(True):
	 			counter = counter +1
	 			z = subprocess.check_output( "nmcli -f BSSID,ACTIVE dev wifi list | awk '$2 ~ /yes/ {print $1}'",shell=True)
				z = z.split()
				if counter > 6:
					print "Password might be incorrect forget the network and try again"
					B.config(state="active")
					return
				if len(z)>0:
					z = bssid_to_ssid[z[0]]
					if z == bssid_to_ssid[result[1]]:
						break
				else :
					print "Connecting to "+bssid_to_ssid[result[1]]+"......"
					connect_to = subprocess.check_output("nmcli con up id "+bssid_to_ssid[result[1]],shell=True)
					time.sleep(2)
			br.open("http://"+server_ip+"/address="+my_ip+"&accepted=true")
			b = subprocess.check_output("python download.py",shell=True)
			b = float(b)
			print "After using the software: ",b
			if(a > b):
				br.open("http://"+server_ip+"/address="+my_ip+"&feedback=true")
			else:
				br.open("http://"+server_ip+"/address="+my_ip+"&feedback=false")			
		else:
			br.open("http://"+server_ip+"/address="+my_ip+"&accepted=false")
	else:
		print "Error!!! "
	top.quit()	
def main():
	ishotspot = checkHotspot()
	if(ishotspot):
		my_mac,my_ssid = findmacandssid()
		br = mechanize.Browser()
		cookiejar = cookielib.LWPCookieJar() 
		br.set_cookiejar( cookiejar ) 
		br.set_handle_equiv( True ) 
		br.set_handle_redirect( True ) 
		br.set_handle_referer( True ) 
		br.set_handle_robots( False ) 
		br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
		br.open( "http://"+server_ip + "/hotspot="+my_ssid)
		print "Hotspot!!!"
	else:	
		a = subprocess.check_output("python download.py",shell=True)
		a = float(a)
		B = Tkinter.Button(top,text="Connect",height=2,width=10,command = lambda: Mycallback(a,B))	
		B.pack(padx=100,pady=100)
		top.geometry("300x300")
		top.mainloop()
main()