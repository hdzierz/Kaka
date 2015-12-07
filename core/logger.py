import datetime
import os
#import logging


class Logger:
    log_dir = '/tmp/nunz/'
    log_err = 'log_err'
    log_msg = 'log_msg'
    log_wrn = 'log_wrn'
#    logger = None

    @staticmethod
    def Init():
        if not(os.path.exists(Logger.log_dir)):
            os.makedirs(Logger.log_dir)

    @staticmethod
    def Log(typ, fn, msg):
        dtt = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        with open(fn, "a") as logfile:
            logfile.write("############################################\n")
            logfile.write(typ + "(" + dtt + " ): \n")
            logfile.write(msg + "\n")
            logfile.write("############################################\n\n\n")

    @staticmethod
    def Warning(msg):
        Logger.Log("WARNING", Logger.log_dir + Logger.log_wrn, msg)

    @staticmethod
    def Error(msg):
        Logger.Log("ERROR", Logger.log_dir + Logger.log_err, msg)

    @staticmethod
    def Message(msg):
        Logger.Log("MESSAGE", Logger.log_dir + Logger.log_msg, msg)


Logger.Init()

