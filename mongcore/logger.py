import datetime
import os
#import logging
from django.http import HttpResponse
import csv

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        print(bcolors.WARNING + msg + bcolors.ENDC)
        Logger.Log("WARNING", Logger.log_dir + Logger.log_wrn, msg)

    @staticmethod
    def Error(msg):
        print(bcolors.FAIL + msg + bcolors.ENDC)
        Logger.Log("ERROR", Logger.log_dir + Logger.log_err, msg)

    @staticmethod
    def Message(msg):
        print(bcolors.OKBLUE + msg + bcolors.ENDC)
        Logger.Log("MESSAGE", Logger.log_dir + Logger.log_msg, msg)


class HttpLogger:
    @staticmethod
    def send(typ, msg, content_type='text/csv'):
        Logger.Error(content_type)
        response = HttpResponse(content_type='text/csv')
        if(content_type=='text/csv'):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="error.csv"'
            writer = csv.writer(response)
            writer.writerow(['"' + typ  + '"'])
            writer.writerow(['"'+ msg + '"'])
        else:
            msg = "<table><tr><td>" + typ + ":" + msg + "</td></tr></table>"
            response = HttpResponse(msg)
        return response
   
    @staticmethod
    def Error(msg, content_type='text/csv'):
        return HttpLogger.send("Error", msg, content_type)

    @staticmethod
    def Message(msg, content_type='text/csv'):
        return HttpLogger.send("Message", msg, content_type)

    @staticmethod
    def Warning(msg, content_type='text/csv'):
        return HttpLogger.send("Warning", msg, content_type)


Logger.Init()

