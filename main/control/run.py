import sys
import datetime
from main.houses.loader import Loader
from main.web.web_server import Server

def startDataAcquisition():
    print 'Start Data Acquisition @ ' + str(datetime.datetime.now())
    Loader().loadAll()
    print 'Data Acquisition Completed @ ' + str(datetime.datetime.now())

def startWeb():
    Server().start()

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
