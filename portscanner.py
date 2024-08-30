import socket
import argparse
import os
from datetime import datetime


def parse_input():  # parse command line arguments

    """

    This function ensures that the required argument `target` is provided, which specifies
    the hostname or IP address of the target to scan. It also handles optional arguments
    that allow the user to specify a port or range of ports to scan, display scan progress,
    set the connection timeout value, and define the path for logging scan results.

    :return:  object containing the parsed arguments.


    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target to scan")
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
    """
    This function converts the target hostname to its corresponding IP address
    and exits the program if the hostname cannot be resolved

    :param hostn: target hostname

    """
    try:
        return socket.gethostbyname(hostn)
    except socket.gaierror:
        print(f"Error: Cannot resolve hostname {hostn}!")
        exit(1)


def write_logfile(_log_file_path: str, _values: list, start: int, end: int):  # write scan summary to logfile
    """
    This function is used to write the scan summary to the log file. It includes the range of ports scanned,
    the status of each open port, and the summary of the scan.

    :param _log_file_path: File path to write and save log file
    :param _values: list which contains the values of open ports
    :param start: Start of the port range scanned.
    :param end: End of the port range scanned.

    """
    fpath = _log_file_path
    try:
        while True:
            if os.path.exists(fpath):
                if input(
                        f"The file {fpath} exists on this system. Do you want to overwrite this file? [y]: ").strip().lower() != 'y':
                    fpath = input("Enter new file path: ")
                    continue
            break

        with open(fpath, "w") as f:
            f.write(f"Scan report for {host} [{hostn}]\n")
            f.write(f"Scanned ports {start} to {end}\n")
            f.write(f"Report generated on {datetime.now().strftime('%B %d, %Y %H:%M:%S')}\n\n")
            f.write("Scan Summary\n")
            f.write("================================================\n\n")

            for port in _values:
                f.write(f"PORT {port}: OPEN\n")

            if not _values:
                f.write("All Ports were CLOSED!\n")

            f.write("\n================================================\n")

        print(f"Successfully created logfile: {fpath}\n")

    except IOError as e:
        print(f"I/O Error {e}\n")

    except Exception as e:
        print(f"Unexpected Error while writing to file {fpath}: {e}\n")


def scan_ports(host, hostn, port_list, timeout, status, _log_file_path):  # scan a range of ports
    """
    This functions scans a given range of ports and displays the status, progress and summary of the scan. If a file path is given to save
    the scan results, it will call the write_logfile() function to write the scan summary to the logfile.

    :param host: target address
    :param hostn: target hostname
    :param port_list: this list contains the START and END value for range
    :param timeout: connection timeout value
    :param status: Boolean used to check whether to display the scan progress
    :param _log_file_path: location to save log file. If no location is given, the parameter is set as false


    """
    open_ports = []

    try:  # try to scan given range of ports
        print(f"Scanning host {host} [{hostn}]\n")

        for portn in range(port_list[0], port_list[1] + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
                scanner.settimeout(timeout)

                if status:
                    print(f"\nScanning port {portn}")
                    print(
                        f"Scan Progress: {(portn - port_list[0]) / (port_list[1] - port_list[0]) * 100:.2f}% complete")
                if scanner.connect_ex((host, portn)) == 0:
                    print(f"Port {portn} is open")
                    open_ports.append(portn)
                else:
                    print(f"Port {portn} is closed")

        print(f"\nScan Complete!\nFound {len(open_ports)} port(s) open\n")

        print(f"Scan Summary")
        if open_ports:
            for port in open_ports:
                print(f"Port {port} is open")
            print()

        else:
            print("All ports were closed!\n")

    except socket.error as e:
        print(f"Socket Error while scanning port: {e}")

    except Exception as e:
        print(f"Unexpected Error while scanning port: {e}")

    finally:  # write open ports to logfile regardless of exceptions
        if _log_file_path is not None:
            write_logfile(_log_file_path, open_ports, port_list[0], port_list[1])


# run the port scanner

args = parse_input()

hostn = args.target
host = get_addr(hostn)
status = args.status
_log_file_path = args.log
_timeout = args.timeout


# check if range and port numbers is valid
if args.range:
    # check if port numbers are valid
    if args.range[0] < 1 or args.range[0] > 65535 or args.range[1] < 1 or args.range[1] > 65535:
        print("Error: Port range values must be between 1 and 65535.")
        exit(1)
    # check if range is valid
    if args.range[0] > args.range[1]:
        print("Error: Start port must be less than or equal to end port.")
        exit(1)

if args.port:
    if args.port < 1 or args.port > 65535:
        print("Error: Port range values must be between 1 and 65535.")
        exit(1)


if args.port is not None:  # scan a single port
    status = False
    scan_ports(host, hostn, [args.port, args.port], _timeout, status, _log_file_path)

elif args.range is not None:  # scan a range of ports
    scan_ports(host, hostn, args.range, _timeout, status, _log_file_path)

elif args.all:  # scan all the ports
    scan_ports(host, hostn, [1, 65535], _timeout, status, _log_file_path)
