from django.http import QueryDict, HttpResponse, HttpResponseRedirect
import gzip

class HttpDataDownloadResponse(HttpResponse):
    fmt = 'csv'
    gzipped = True
    data = None

    def __init__(self, data, report, fmt = 'csv', zipit = True):
        if data:
            c_type, download = self.get_mime_type(fmt)
            fn = report + '.' + fmt
            if zipit:
                with gzip.open('/tmp/' + fn + '.gz', 'wb') as f:
                    f.write(data)
                fn = fn + '.gz'
                c_type, download = self.get_mime_type('gzip')
                with gzip.open('/tmp/' + fn + '.gz', 'wb') as f:
                    data = f.read(fn)
            super(HttpDataDownloadResponse, self).__init__(data, content_type=c_type)
            if download:
                self['Content-Disposition'] = 'attachment; filename="' + fn + '"'
        else:
            super(HttpDataDownloadResponse, self).__init__('No Data')

    def get_mime_type(self, ext):
        if ext == 'json':
            return ('Content-type: application/json', False)
        if ext == 'xml':
            return ('Content-type: application/xml', False)
        if ext == 'yaml':
            return ('Content-type: text/x-yaml', False)
        if ext == 'csv':
            return ('Content-type: text/csv', False)
        if ext == 'gzip':
            return ('Content-type: application/x-gzip', True)
        return ('Content-type: application/octet-stream', True)
