import re
import inspect
import pickle


class Response():
    __code = None
    __headers = []
    __content_bytes = b""
    __mime = "text/html; encoding=utf-8"
    __encoding = None
    __complete = False  # if set True, the response is ready to be sent, use for immature end, error ...

    def __init__(self):
        frame = inspect.stack()[1][0]
        # read request data from hidden variable and deletes it
        if "__HIDDEN__RESPONSE__" in frame.f_locals:
            # self.url = frame.f_locals["__REQUEST"].url
            # self.method = frame.f_locals["__REQUEST"].method
            obj = pickle.loads(frame.f_locals["__HIDDEN__RESPONSE__"])
            if obj.headers:
                self.headers = []
                for h in obj.headers:
                    if h[0].lower() != 'content-length':
                        self.headers.append(h)
            else:
                self.reset()
            self.headers = list(dict.fromkeys(self.headers))
            if obj.mime:
                self.mime = obj.mime
            if obj.code:
                self.code = obj.code
            # remove _REQUEST and _RESPONSE so it's invisible for user
            del frame.f_locals["__HIDDEN__RESPONSE__"]
        else:
            self.reset()

    def detect_encoding(self):
        regex = r";[ ]*(?i)(charset)=(.*)"  # case insensitive "charset" followed by semicolon an x spaces
        matches = re.finditer(regex, self.__mime)
        ret = None
        for matches_count, match in enumerate(matches):
            ret = match.group(2).lower()
        if not ret:
            ret = "iso-8859-1"  # default encoding for HTTP
        elif ret.strip() == "":
            ret = "iso-8859-1"  # default encoding for HTTP
        return ret

    # Passed to WSGI
    # https://restfulapi.net/http-status-codes/
    @property
    def status(self):
        if self.__code == 100:
            return "100 Continue"
        if self.__code == 101:
            return "101 Switching Protocols"
        if self.__code == 102:
            return "102 Processing"
        if self.__code == 200:
            return "200 OK"
        if self.__code == 201:
            return "201 Created"
        if self.__code == 202:
            return "202 Accepted"
        if self.__code == 203:
            return "203 Non-Authoritative Information"
        if self.__code == 204:
            return "204 No Content"
        if self.__code == 301:
            return "301 Moved Permanently"
        if self.__code == 302:
            return "302 Found"
        if self.__code == 500:
            return "500 Internal Server Error"
        if self.__code == 400:
            return "400 Bad Request"
        if self.__code == 401:
            return "401 Unauthorized"
        if self.__code == 403:
            return "403 Forbidden"
        if self.__code == 404:
            return "404 Not Found"
        if self.__code == 405:
            return "404 Method Not Allowed"
        if self.__code == 500:
            return "500 Internal Server Error"

    @property
    def code(self):
        return self.__code

    @property
    def complete(self):
        return self.__complete

    @property
    def mime_encoding(self):
        return self.detect_encoding()

    @property
    def mime(self):
        return self.__mime

    @property
    def headers(self):
        return self.__headers

    @property
    def headers_render(self):
        content_length = [("Content-Length", str(len(self.__content_bytes)))]
        content_type = [("Content-Type", self.__mime)]
        return self.__headers + content_length + content_type

    def add_header_list(self, new_header):
        self.__headers = self.__headers + new_header

    def add_header_from_config(self, new_headers):
        to_add = []
        for item in new_headers:
            to_add.append((list(item)[0], item[list(item)[0]]))
        self.__headers = self.__headers + to_add

    def add_header(self, header, value):
        self.__headers = self.__headers + [(header, value)]

    def end(self):
        self.__complete = True

    # Passed to WSGI
    # @property
    # def content_bytes(self):
    #    return self.__content

    # @content_bytes.setter
    # def content_bytes(self, value):
    #    self.__content = value

    @code.setter
    def code(self, value):
        self.__code = value

    @complete.setter
    def complete(self, value):
        self.__complete = value

    @code.setter
    def code(self, value):
        self.__code = value

    @mime.setter
    def mime(self, value):
        self.__mime = value

    @headers.setter
    def headers(self, value):
        self.__headers = value

    @property
    def content_str(self):
        return self.__content_bytes.encode('UTF-8')

    @content_str.setter
    def content_str(self, value):
        # temp fix to accept both bytes and str
        if isinstance(value, str):
            self.__content_bytes = value.encode("utf-8")
        if isinstance(value, bytes):
            # self.__content_bytes = value
            raise ValueError('setter `content_str` has been called with `bytes`, expecting `str`')

    @property
    def content_bytes(self):
        return self.__content_bytes

    @content_bytes.setter
    def content_bytes(self, value):
        # temp fix to accept both bytes and str
        if isinstance(value, bytes):
            self.__content_bytes = value
        if isinstance(value, str):
            # self.__content_bytes = bytes(value, encoding='utf-8')
            raise ValueError('setter `content_bytes` has been called with `str`, expecting `bytes`')
        # print('call setter, in: ' + str(type(value)))
        # self.__content_bytes = bytes(value, encoding='utf-8')
        # print('call setter __content_bytes: ' + str(type(value)))

    def __call__(self):
        return self.code, self.headers, self.content_str

    def reset(self):
        self.__code = None
        self.__headers = []
        self.__content_bytes = b""
        self.__complete = False

# @r = Response()
# r.Code = 200
# r.Headers = [("a","x")]
# r.Content = "ahoj"
# print(r.Code)
# print(r())
