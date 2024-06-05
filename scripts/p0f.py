from p0f import P0f, P0fException

data = None
p0f = P0f("p0f.sock") # point this to socket defined with "-s" argument.
try:
    data = p0f.get_info("192.168.0.1")
except P0fException, e:
    # Invalid query was sent to p0f. Maybe the API has changed?
    print e
except KeyError, e:
    # No data is available for this IP address.
    print e
except ValueError, e:
    # p0f returned invalid constant values. Maybe the API has changed?
    print e

if data:
    print "First seen:", data["first_seen"]
    print "Last seen:", data["last_seen"]