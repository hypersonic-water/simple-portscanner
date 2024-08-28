import socket
import argparse
import os


def parse_input():  # parse commandline input
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="Hostname to scan")
    parser.add_argument("-p", "--port", type=int, help="Scan a specific port")
    parser.add_argument("-r", "--range", type=int, nargs=2, metavar=("START", "END"), help="Scan a range of ports")
    parser.add_argument("--all", "-a", action="store_true", help="Scan all ports")
    parser.add_argument("-s", "--status", action="store_true", help="Display scan progress")
    parser.add_argument("-t", "--timeout", type=float, default=1.5, help="Set timeout value")
    parser.add_argument("-l", "--log", type=str, help="Store results in a log file")

    args = parser.parse_args()

    if not args.port and not args.range and not args.all:
        parser.error("Invalid arguments! You must specify a port or a range of ports to scan!")

    return args


def get_addr(hostn: str):  # resolve hostname to ip_addr
    try:
        return socket.gethostbyname(hostn)
    except socket.gaierror:
        print(f"Cannot resolve hostname {hostn}!")
        exit(1)


def scan_port(hostn, portn):  # scan a single port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
        scanner.settimeout(args.timeout)
        print(f"Scanning host {get_addr(hostn)} [{hostn}]\n")
        if scanner.connect_ex((get_addr(hostn), portn)) == 0:
            print(f"Port {portn} is open")
        else:
            print(f"Port {portn} is closed")

    print(f"Scan complete!")


def write_logfile(hostn, file_loc, _values: list):  # write scan summary to logfile
    fpath = file_loc
    while True:
        if os.path.exists(fpath):
            if input(f"The file {fpath} exists on this system. Do you want to overwrite this file? [y]: ").strip().lower() != 'y':
                fpath = input("Enter new file path: ")
                continue
        break

    with open(fpath, "w") as f:
        f.write(f"Scan report for {get_addr(hostn)} [{hostn}]\n")
        for port in _values:
            f.write(f"{port} is open\n")


def scan_ports(hostn, port_list, status, file_loc):  # scan a range of ports
    open_ports = []
    host_addr = get_addr(hostn)

    try:  # try to scan given range of ports
        print(f"Scanning host {get_addr(hostn)} [{hostn}]\n")

        for portn in range(port_list[0], port_list[1] + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
                scanner.settimeout(args.timeout)

                if status:
                    print(f"\nScanning port {portn}")
                    print(f"Scan Progress: {(portn - port_list[0]) / (port_list[1] - port_list[0]) * 100:.2f}% complete")
                if scanner.connect_ex((host_addr, portn)) == 0:
                    print(f"Port {portn} is open")
                    open_ports.append(portn)
                else:
                    print(f"Port {portn} is closed")



        print(f"\nScan Complete!\nFound {len(open_ports)} port(s) open\n")

        print(f"Scan Summary")
        if open_ports:
            for port in open_ports:
                print(f"Port {port} is open")
        else:
            print("All ports were closed!")

    finally:  # write open ports to logfile regardless of exceptions
        if file_loc is not None:
            write_logfile(hostn, file_loc, open_ports)


# run the port scanner

args = parse_input()

host = args.hostname
status = args.status
file_loc = args.log

if args.port is not None: # scan a single port
    if args.port < 0 or args.port > 65535:
        print("Invalid port number!")
        exit(1)

    scan_port(host, args.port)

elif args.range is not None: # scan a range of ports
    if args.range[0] > args.range[1] or args.range[0] < 0 or args.range[0] > 65535 or args.range[1] < 0 or \
            args.range[1] > 65535: # ensure the range is valid
        print("Invalid port range!")
        exit(1)

    scan_ports(host, args.range, status, file_loc)

elif args.all: # scan all the ports
    scan_ports(host, [0, 65535], status, file_loc)
