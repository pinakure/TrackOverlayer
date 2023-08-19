@pyinstaller --onefile --noconsole -i icon.ico main.py
@move dist\main.exe RAMon.exe
@rmdir dist