from Mamlambo.Request import Request
import Mamlambo

logo = "@LOGO"

version = Mamlambo.__version__

request = Request()

debug = request.path_info + "<br />" + request.method + "<br />" + request.query_string


