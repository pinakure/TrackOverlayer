@pyinstaller --onefile -i icon.ico main.py
@move dist\main.exe RAMon_debug.exe
@rmdir dist
@pyinstaller --onefile --noconsole -i icon.ico main.py
@move dist\main.exe RAMon_debug.exe
@rmdir dist
