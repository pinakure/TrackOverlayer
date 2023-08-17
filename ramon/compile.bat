@pyinstaller --onefile -i icon.ico update_data.py
@move dist\update_data.exe RAMon.exe
@rmdir dist