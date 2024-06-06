import subprocess


#excel打开PERSONAL.xlsb
excel_exe_path = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
workbook_path = r"C:\Users\25757\AppData\Roaming\Microsoft\Excel\XLSTART\PERSONAL.xlsb"

subprocess.Popen([excel_exe_path, workbook_path])
# 定义应用程序路径的变量

marktext_path = r'D:\App\marktext\MarkText.exe'
navicat_path = r'F:\Navicat+Premium+16\Navicat Premium 16\navicat.exe'
datagrip_path = r'F:\DataGrip 2023.3.1\bin\datagrip64.exe'
everything_path = r'D:\App\everything\Everything.exe'
qq_path = r'D:\App\qq\Bin\QQ.exe'
# 将所有路径存储在一个列表中
app_paths = [
    marktext_path,
    navicat_path,
    datagrip_path,
    everything_path,
    qq_path
]

# 循环遍历列表，使用subprocess.Popen打开每个应用程序
for path in app_paths:
    subprocess.Popen([path])
