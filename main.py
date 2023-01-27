import sys
import pymysql

PROGNAME = "ip"
VERSION = "1.00.01 (230126)"

# Connection (login) info for the database we want to consult. In any
# more advanced versions, this will be in a separate config file
IP_COUNTRY_DB_INFO = {
    'host': 'localhost',
    'user': 'webuser',
    'db': 'ipcountry',
    'password': 'webuser'
}
def main():
    parms = sys.argv

    # Check args. There should be just one, the ip address or "-v" for version.
    # Not just one arg? Put up usage message and bail.
    if len(sys.argv) != 2:
        usage()
        exit(-1)
    # Version request?
    elif (sys.argv[1] == "-v"):
        print_version()
        exit(0)
    # We'll assume, then, that the arg is an ip address and attempt to
    # convert it into a long integer that we can use to get the country
    # code from the database.
    # At this point, Lord help us if the arg isn't a well-formed IP
    # address because we will crash and burn in long skeins of
    # unhandled exceptions otherwise. Beware.
    # get_long_ip() returns -1 if anything goes wrong there.
    longIp = get_long_ip(sys.argv[1])
    if (longIp < 0):
        usage()
        exit(-1)
        
    print(longIp)
    # Last thing is to get the country code from the database and output it.
    print(get_country_code(longIp))

def get_long_ip(ip_addr):
    # Initialize integer IP address.
    ipnum = 0
    # split() the incoming ip address into four strings.
    ipAddrs = ip_addr.split('.')
    # Make sure we have four, bail if not.
    if (len(ipAddrs) != 4):
        return(-1)
    # Now accumulate an integer value of the ip address by incrementing
    # through each octet as a decrementing power of 256.
    ipnum += int(ipAddrs[0]) * (256 ** 3)
    ipnum += int(ipAddrs[1]) * (256 ** 2)
    ipnum += int(ipAddrs[2]) * (256 ** 1)
    ipnum += int(ipAddrs[3]) * (256 ** 0)

    return ipnum


def get_country_code(longIp):
    # Put the database access info in a local variable and use that to
    # initiate a connection.
    dbi = IP_COUNTRY_DB_INFO
    conn = pymysql.connect(
        host=dbi['host'],
        user=dbi['user'],
        password=dbi['password'],
        db=dbi['db']
    )
    # Make a cursor, in db lingo.
    cur = conn.cursor()
    # Make a query for the country code. It will be found
    # in a range between ipFROM and ipTO.
    query = 'SELECT countrySHORT FROM IPCountry WHERE ' \
            + f'ipFROM <= {longIp} AND {longIp} <= ipTO'
    # Execute the query through the cursor we created above.
    cur.execute(query)
    # Get the result. There should be only one, so we don't have
    # to loop through anything.
    result = cur.fetchone()
    # Ship the result back. Remember it's a single-value tuple, so we have
    # to extract the actual result.
    return result[0]

def usage():
    # Print usage() message and return.
    print(f'usage: {PROGNAME} ip_address')

def print_version():
    print(f'{PROGNAME} version {VERSION}')

######## main() called from here.

if __name__ == '__main__':
    main()
