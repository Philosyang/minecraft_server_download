# minecraft_server_download
Download (and validate) the newest minecraft server jar.

Does not initiate download when website jar and local jar has the same sha-1 hash.

One possible usage is to integrate this into start_server.bat/.sh.

If ModuleNotFoundError try `pip install requests` and `pip install beautifulsoup4`.