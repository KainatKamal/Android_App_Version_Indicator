# Android_App_Version_Indicator
This script extracts the below details of multiple APKs at once and stores them information in an excel.
- package name
- version code
- version name
- minSDK version

## Requirements:
- Windows 10
- Python3 installed and added to environment variable
- pip3 installed and added to environment variable
- Python Modules -> xlsxwriter

Install the python modules using the below command:<br/>
**pip install xlsxwriter**

## Extractor script usage:
1. Run the script - **python Android_App_Version_Indicator.py**
2. When prompted enter the path of the folder where APKs are present.
3. The excel will be present in the output folder with package name & version details of the APKs
    ![image](https://user-images.githubusercontent.com/49153415/150587749-9195123d-9f94-4d1e-bdab-8c3379da6632.png)


## Tool Used:
It utilises aapt2 standalone tool to extract the details. <br/>
**aapt2 version:** aapt2-7.2.0-alpha07-7984345-windows
