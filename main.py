import sys
import pymysql

PROGNAME = "ip"
VERSION = "1.00.00 (230116)"

DB_INFO = {
    'host' : 'localhost',
    'user' : 'webuser',
    'db' : 'ipcountry',
    'password' : 'webuser'
}

def main():

    parms = sys.argv

    # Check args. There should be just one, the ip address or "-v" for version.
    # Not just one arg? Put up usage message and bail.
    if len(sys.argv) != 2:
        usage()
        exit(-1)
    # Version request?
    elif(sys.argv[1] == "-v"):
        print_version()
        exit(0)
    # We'll assume, then, that the arg is an ip address and attempt to convert it into
    # a long integer that we can use to get the country code from the database.
    longIp = get_long_ip(sys.argv[1])
    print(longIp)
    # Last thing is to get the country code from the database and output it.
    print(get_country_code(longIp))

def usage():
# Print usage() message and return.
    print("usage: ip ip_address")

def print_version():
    print("%s version %s", PROGNAME, VERSION)

def get_long_ip(ip_addr):
    # Initialize integer IP address.
    ipnum = 0
    # split() the incoming ip address into four strings.
    ipAddrs = ip_addr.split('.')
    # Now accumulate an integer value of the ip address by treating each octet
    # as a power of 256.
    ipnum += int(ipAddrs[0]) * (256 ** 3)
    ipnum += int(ipAddrs[1]) * (256 ** 2)
    ipnum += int(ipAddrs[2]) * (256 ** 1)
    ipnum += int(ipAddrs[3]) * (256 ** 0)

    return ipnum

def get_country_code(longIp):
    # Put the database access info in a local variable and use that to
    # initiate a connection.
    dbi = DB_INFO
    conn = pymysql.connect (
        host=dbi['host'],
        user=dbi['user'],
        password=dbi['password'],
        db=dbi['db']
    )
    # Make a cursor, in db lingo.
    cur = conn.cursor()
    







######## main() called from here.

if __name__ == '__main__':
    main()
