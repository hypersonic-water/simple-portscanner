# Simple Port Scanner

This is a simple port scanner written in Python. It allows the user to scan a specific port, a range of ports or all ports on a given target.

## Features
- **Scan a specific port on the target:** Check if a single port is open on the target.
- **Scan a range of ports on the target:** Check if a range of ports are open on the target.
- **Scan all ports on the target:** Check if all ports from 0 to 65535 are open on the target.
- **Save scan results to a log file.**
- **View the progress of the scan for a range of ports.**

## Usage
portscanner.py [-h] [-p PORT] [-r Start End] [--all] [-s] [-t TIMEOUT] [-l LOG] hostname

## Command-line arguments
**hostname              Hostname to scan**

**-p PORT, --port PORT  Scan a specific port**

**-r Start End, --range Start End
                        Scan a range of ports**
                      
**--all, -a             Scan all ports**

**-s, --status          Display scan progress**

**-t TIMEOUT, --timeout TIMEOUT
                        Set timeout value**
                      
**-l LOG, --log LOG     Store results in a log file**                    

## Examples
**Scan a single port**
`python3 portscanner.py example.com -p 8080`

**Scan a range of ports**
`python3 portscanner.py example.com -r 20 60`

**Scan all ports**
`python3 portscanner.py example.com --all`

**Save scan results to a log file**
`python3 portscanner.py example.com -r 22 80 --log scan_log.txt`

**View scan progress**
`python3 portscanner.py example.com --range 100 200 --status -l scan_log.txt`
