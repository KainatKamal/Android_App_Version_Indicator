import os
import os.path
import subprocess
import shutil
import xlsxwriter
import re
from pathlib import Path
from os.path import join



def execute_cmd(cmd,text):
	text=text.upper()
	p1 = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p1.communicate()
	if "DUMMY" not in  text :
		text=executable_output+text
		f=open(text,'a+')
		f.write(out)
		f.close()
	return out


	
print("  ---------------------------------  ")
print("    Android App Version Indicator    ")
print("  ---------------------------------  ")


execute_cmd("rmdir output /S /Q","dummy")
execute_cmd("mkdir output","dummy")
execute_cmd("type nul > output.txt","dummy")
 
# Create the excel report
workbook = xlsxwriter.Workbook('Apps_Version_Indicator.xlsx')
worksheet = workbook.add_worksheet("Apps_Version_Indicator")
border = workbook.add_format({'border':1})
cell_format = workbook.add_format({'bold':True, 'border':2})
cell_format.set_bg_color('cyan')
worksheet.write('A1', 'Sl. No.', cell_format)
worksheet.write('B1', 'APK Name', cell_format)
worksheet.write('C1', 'Package Name', cell_format)
worksheet.write('D1', 'Version Code', cell_format)
worksheet.write('E1', 'Version Name', cell_format)
worksheet.write('F1', 'Min SDK Version', cell_format)


apk_path=input("\n Enter the path of the folder where APKs are present: ")


row = 1
column = 0
serial_number = 1
current_working_directory = os.getcwd()
aapt_path = current_working_directory + "\\tools\\aapt2.exe"
excel_creation_path = current_working_directory + "\\Apps_Version_Indicator.xlsx"
excel_output_path = current_working_directory + "\\output\\Apps_Version_Indicator.xlsx"
output_txt_path = current_working_directory + "\\output.txt"
total_apps = 'dir /a:-d /s /b '+apk_path+' | find /c ":"'
aapt = aapt_path + " d badging "
find_version = ' | findstr /i /c:"version" | findstr /i /r "[0-9]" > output.txt'
delete_output_txt = 'del '+output_txt_path
no_of_apps = int(execute_cmd(total_apps,"dummy"))
print("\n Total no. of apps: ",no_of_apps)
all_apps = os.listdir(apk_path)


for apk_name in all_apps:	
	apk_full_path = os.path.join(apk_path, apk_name)
	execute = aapt + apk_full_path + find_version
	execute_cmd(execute,"dummy")
	file = open(output_txt_path)
	file_content = file.read()
	package_name=re.search(r"name='(.*?)' versionCode",file_content).group(1)
	version_code=re.search(r"versionCode='([\d.]+)",file_content).group(1)
	found1 = bool(version_code)
	version_name=re.search(r"versionName='([\d.]+)",file_content).group(1)
	found2 = bool(version_name)
	try:
		min_sdk_version=re.search(r"sdkVersion:'([\d.]+)",file_content).group(1)
	except AttributeError:
		min_sdk_version=re.search(r"sdkVersion:'([\d.]+)",file_content)
	found3 = bool(min_sdk_version)
	worksheet.write(row, column, serial_number, border)
	worksheet.write(row, column + 1, apk_name, border)
	worksheet.write(row, column + 2, package_name, border)
	if(found1 == True):
		worksheet.write(row, column + 3, version_code, border)
	else:
		worksheet.write(row, column + 3, 'NOT FOUND', border)
	if(found2 == True):
		worksheet.write(row, column + 4, version_name, border)
	else:
		worksheet.write(row, column + 4, 'NOT FOUND', border)
	if(found3 == True):
		worksheet.write(row, column + 5, min_sdk_version, border)
	else:
		worksheet.write(row, column + 5, 'NOT FOUND', border)
	serial_number +=1
	row +=1

file.close()


worksheet.set_column('B:C',50)
worksheet.set_column('D:F',25)
workbook.close()


shutil.move(excel_creation_path, excel_output_path)
execute_cmd(delete_output_txt,"dummy")
print("\n The report has been generated: \output\Apps_Version_Indicator.xlsx")
