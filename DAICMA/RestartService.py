import win32serviceutil

def service_running(service, machine):
    return win32serviceutil.QueryServiceStatus(service, machine)[1] == 4

def service_info(action, machine, service):
    running = service_running(service, machine)
    servnam = 'service (%s) on machine(%s)'%(service, machine)
    action = action.lower(  )
    if action == 'stop':
        if not running:
            print "Can't stop, %s not running"%servnam
            return 0
        win32serviceutil.StopService(service, machine)
        running = service_running(service, machine)
        if running:
            print "Can't stop %s (???)"%servnam
            return 0
        print '%s stopped successfully' % servnam
    elif action == 'start':
        if running:
            print "Can't start, %s already running"%servnam
            return 0
        win32serviceutil.StartService(service, machine)
        running = service_running(service, machine)
        if not running:
            print "Can't start %s (???)"%servnam
            return 0
        print '%s started successfully' % servnam
    elif action == 'restart':
        if not running:
            print "Can't restart, %s not running"%servnam
            return 0
        win32serviceutil.RestartService(service, machine)
        running = service_running(service, machine)
        if not running:
            print "Can't restart %s (???)"%servnam
            return 0
        print '%s restarted successfully' % servnam
    elif action == 'status':
        if running:
            print "%s is running" % servnam
        else:
            print "%s is not running" % servnam
    else:
        print "Unknown action (%s) requested on %s"%(action, servnam)

if __name__ == '__main__':
    # Just some test code; change at will!
    machine = 'cr582427-a'
    service = 'Zope23'
    action = 'start'
    service_info(action, machine, service)