# LANCopyPaste

### a simple tool for copy,paste text on local netwrok devices

** Use `8000` Port: **

```
python3 main.py
```
open browser on client device and go to ``` {server_ip}:8000 ```
example: ``` 192.168.1.5:8000 ```

** send text to client (string): **
```
python3 main.py -m "Hello World!"
```

** send a text file content to client: **
```
python3 main.py -m /tmp/textfile.txt
```

** run on custom port: **
```
python3 main.py -p 2020
```

** set output path to save text file **
```
python3 main.py -p 2020 -o /tmp/clipboard.txt
```

### [buy me a coffee ☕️](https://bmc.link/mohsenparandvar)
