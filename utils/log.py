# coding: utf-8

import logging
from tornado.options import options

class Log(object):

    def __init__(self, name=None):
        self.log = None
        # log format
        log_format = "[%(levelname)1.1s %(asctime)s] %(message)s"
        formatter = logging.Formatter(log_format, '%y%m%d %H:%M:%S')
        # console log handler
        console = logging.StreamHandler()
        console.setLevel(logging.WARN)
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
        # file log handler
        if options.log_file_prefix and name is not None:
            log = logging.getLogger(name)
            channel = logging.handlers.TimedRotatingFileHandler(
                filename=options.log_file_prefix,
                when='midnight',
                backupCount=options.log_file_num_backups
            )
            channel.setFormatter(formatter)
            log.addHandler(channel)
            if options.debug:
                log.setLevel(logging.DEBUG)
            else:
                log.setLevel(logging.INFO)
            self.log = log

    def format(self, *args):
        _ = ' '.join('%s' for _ in xrange(len(args)))
        return _ % (args)

    def info(self, *args):
        if self.log:
            self.log.info(self.format(*args))
        else:
            print self.format(*args)

    def warn(self, *args):
        if self.log:
            self.log.warn(self.format(*args))
        else:
            print self.format(*args)

    def debug(self, *args):
        if self.log:
            self.log.debug(self.format(*args))
        else:
            print self.format(*args)

    def error(self, *args):
        if self.log:
            self.log.error(self.format(*args))
        else:
            print self.format(*args)

log = Log('maicheren-api')
