import pql


class Query:
    @staticmethod
    def result(request, infmt, qry):
        try:
            qry = pql.find(qry)
        except Exception as inst:
            Logger.Error(str(type(inst)))    # the exception instance
            Logger.Error(str(inst.args))     # arguments stored in .args
            Logger.Error(str(inst))
            return HttpLogger.Error("Syntax Error in " + str(qry)), False

        return qry, True

