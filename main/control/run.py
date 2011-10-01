import BaseHTTPServer
import sys
import datetime
from main.houses.foxtons import Foxtons
from main.houses.persistence import Librarian
from main.web.webserver import PropertiesHandler

def startDataAcquisition():
    print 'Start Data Acquisition @ ' + str(datetime.datetime.now())
    Librarian().archiveProperties(Foxtons().properties())
    print 'Data Acquisition Completed @ ' + str(datetime.datetime.now())

def startWeb():
    server_class = BaseHTTPServer.HTTPServer
    webserver = server_class(('192.168.1.2', 1234), PropertiesHandler)

    print "Web Server UP"
    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webserver.server_close()
    print "Web Server DOWN"

def stopWeb():
    raise Exception, 'Web stop supported yet through keyboard interrupt (for the time being)'


def fail():
    raise Exception, 'Expected run <start|stop> <data|web>, obtained ' + str(sys.argv[1:])

if __name__ == '__main__':
    if len(sys.argv) != 3: fail()

    command = sys.argv[1]
    what = sys.argv[2]

    if what == 'data':
        if command == 'start':
            startDataAcquisition()
        else:
            raise Exception, 'Data acquisition supports only start'

    elif what == 'web':
        if command == 'start':
            startWeb()
        elif command == 'stop':
            stopWeb()
        else:
            raise Exception, 'Web supports only start and stop commands'

    else: fail()
