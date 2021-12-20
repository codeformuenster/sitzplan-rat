# Sitzplan Rat Oparl Parser

## Local development

Open two shell windows:
1. Watch config files for changes and run our python-script to regenerate the Rats-Sitzplan
2. Serve the html
### Shellwindow 1
```bash
    # Watch a list of files
    #   "-f" => File to watch (can be repeated)
    #   "-c" => Command to execute on file change
    inotify-hookable -f config-members.json -f generateSitzplan.py -c 'python3 generateSitzplan.py'

    # Alternative version:
    #   "-w" => Directory to watch ("dot" = current dir)
    #   "-i" => File patterns to ignore (we ignore html files, because they will be generated, which triggers a recursive call)
    inotify-hookable -w . -i *.html config-members.json -f generateSitzplan.py -c 'python3 generateSitzplan.py'
```
### Shellwindow 2
```bash
    # Run http server
    python3 -m http.server 8000
```