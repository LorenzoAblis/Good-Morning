My first webscraper using python that fetches the latest news, weather, and forecast and loads it on a simple tkinter app and loads every computer startup

To use, install the following libraries,

- threading
- requests
- BeautifulSoup
- webbrowser
- customtkinter (A tkinter theme that changes the UI to be more modern) https://customtkinter.tomschimansky.com

  To run on startup use the following instructions (FOR WINDOWS),

  - Navigate to your Startup folder
  - Create a new .txt file
  - Paste the following commands,
    Set objShell = CreateObject("WScript.Shell")
    objShell.Run "python C:\path\to\your\python\file.py", 0
    Set objShell = Nothing
  - Save the file and change the file extension to a .vbs file.
  - Restart your PC 

