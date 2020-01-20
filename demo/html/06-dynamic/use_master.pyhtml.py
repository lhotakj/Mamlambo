from Mamlambo.Request import Request
from Mamlambo.Response import Response
import Mamlambo

logo = "@LOGO"

v = "test"

version = Mamlambo.__version__

request = Request()

debug = str(request.path_info) + "<br />" + str(request.method) + "<br />" + str(request.query_string) + "<br />" + request.unique_id

v ="here"
response = Response()
#response.add_header("X-X","aa")
#response.mime = "plain/text"
