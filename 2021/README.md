# Sitzplan Rat Oparl Parser

How does it work?

* The script `generateSitzplan.py` will read all board members of a committee via OParl API interface and then write the member list to the file `config-members.json`, if the file does not exist.
* If the file exists, then it will read the seating information from the field `seat` of every member and then render the committee seating plan to the file `sitzplan.html`

## Usage

```bash
    # Step 1: On the first run, the file config-members.json will be generated:
    python3 generateSitzplan.py

    # Step 2: Manually enter the seating information
    # Now you can open the file `config-members.json`
    # and fill out all the seating information in the fields `seat`.

    # Step 3: Run generateSitzplan.py again to generate the sitzplan.html
    python3 generateSitzplan.py

```

## Local development

It is easier to fill out the seating information if you get "live feedback". That is why you should do the following:

Open two shell windows:
1. Watch config files for changes and run our python-script to regenerate the Rats-Sitzplan
2. Serve the html

### Shellwindow 1
```bash
    # Watch for file changes and run generateSitzplan
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