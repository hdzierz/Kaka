import csv
from django.http import StreamingHttpResponse
from platform import platform


class Echo(object):
    """Copied from docs.djangoproject.com/en/1.8/howto/outputting-csv/

    An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def write_stream_response(rows, experi_name):
    """
    Builds a csv file from the given list of string representations of csv rows and
    returns a StreamingHttpResponse with the csv file as an attachment
    :param rows: list of string representations of csv rows
    :param experi_name: Used to name the csv file
    :return: StreamingHttpResponse with csv file as attachment
    """
    if 'Windows' in platform():
        writer = csv.writer(Echo())
    else:
        unix_dialect = csv.excel()
        unix_dialect.lineterminator = '\n'
        writer = csv.writer(Echo(), dialect=unix_dialect)
    reader = csv.reader(rows)
    # Write query results to csv response
    response = StreamingHttpResponse((writer.writerow(r) for r in reader),
                                     content_type="text/csv")
    content = 'attachment; filename="' + experi_name + '.csv"'
    response['Content-Disposition'] = content
    return response
