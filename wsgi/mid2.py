#!/usr/bin/env python
import os
import threading
import logging
import signal
 
logger = None
 
def ShudownGracefully(pSignal, pFrame):
    logger.info('Shutdown gracefully')
 
if logger is None:
    logger = logging.getLogger('WSGIMultiThreadServer')
    handler = logging.FileHandler('WSGIMultiThreadServer.log')
    formatter = logging.Formatter('%(asctime)-15s %(process)06d %(thread)06d %(filename)s %(lineno)d %(module)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  
    logger.info('Active log')
    signal.signal(signal.SIGTERM, ShudownGracefully)
    logger.info('Register ShudownGracefully')  
 
def app(environ, start_response):
    lCurrentThread = threading.currentThread()
    logger.info('Start request')
    response_body = 'PID: %d\n' % os.getpid()
    response_body += 'TID: %d\n' % lCurrentThread.ident
    response_body += 'Thread name: %s\n' % lCurrentThread.name
    response_body += '\n'.join(['%s: %s' % (key, value) for key, value in sorted(environ.items())])
 
    # Response_body has now more than one string
    response_body = ['The Beggining\n',
                   '*' * 30 + '\n',
                   response_body,
                   '\n' + '*' * 30 ,
                   '\nThe End']
 
    # So the content-lenght is the sum of all string's lengths
    content_length = 0
    for s in response_body:
        content_length += len(s)
 
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(content_length))]
    start_response(status, response_headers)
 
    logger.info('Finish request')  
    return response_body
 
logger.info('Loaded test.py')
 
if __name__ == "__main__":
    from WSGIMultiThreadServer import make_multithread_server 
    # specify your 
    lWSGIMultiThreadServer = make_multithread_server('', 8000, app)
    # Respond to requests until process is killed
    lWSGIMultiThreadServer.serve_forever()
