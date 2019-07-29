#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import Mamlambo
from . import Response
from . import Configuration


class MamlamboException:
    @staticmethod
    # > http_code: int (2xx-5xx), the full text ie. "200 OK" get's translated later
    # > error: main error
    def render(http_code=500,
               error="Error",
               description=None,  # basic description
               details=None,  # debug like details
               stack_trace=None):
        configuration = Configuration.Configuration()  # read singleton

        DEFAULT_ERROR_PAGE_CONTENT = u'<!DOCTYPE HTML><html><head><style> *{font-family:Arial,Helvetica,sans-serif}html,body,div,span,h1,h2,h3,h4,h5,h6,p,pre,a,code,b,u,i,center,dl,dt,dd,ol,ul,li,table,tbody,tr,th,td{margin:0;padding:0;border:0;font-size:100%;vertical-align:baseline}body,html{line-height:1;height:100%}ol,ul{list-style:none}table{border-collapse:collapse;border-spacing:0}body.black{background:rgb(0,0,0);background:url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDEgMSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJncmFkLXVjZ2ctZ2VuZXJhdGVkIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjAlIiB5MT0iMCUiIHgyPSIwJSIgeTI9IjEwMCUiPgogICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iIzAwMDAwMCIgc3RvcC1vcGFjaXR5PSIxIi8+CiAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiMyOTJjMmQiIHN0b3Atb3BhY2l0eT0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiAgPHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0idXJsKCNncmFkLXVjZ2ctZ2VuZXJhdGVkKSIgLz4KPC9zdmc+);background:-moz-linear-gradient(top,rgba(0,0,0,1) 0%,rgba(41,44,45,1) 100%);background:-webkit-gradient(linear,left top,left bottom,color-stop(0%,rgba(0,0,0,1)),color-stop(100%,rgba(41,44,45,1)));background:-webkit-linear-gradient(top,rgba(0,0,0,1) 0%,rgba(41,44,45,1) 100%);background:-o-linear-gradient(top,rgba(0,0,0,1) 0%,rgba(41,44,45,1) 100%);background:-ms-linear-gradient(top,rgba(0,0,0,1) 0%,rgba(41,44,45,1) 100%);background:linear-gradient(to bottom,rgba(0,0,0,1) 0%,rgba(41,44,45,1) 100%);filter:progid:DXImageTransform.Microsoft.gradient( startColorstr="#000",endColorstr="#292c2d",GradientType=0 )}body.red{background:#210000;background:url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDEgMSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJncmFkLXVjZ2ctZ2VuZXJhdGVkIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjAlIiB5MT0iMCUiIHgyPSIwJSIgeTI9IjEwMCUiPgogICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iIzIxMDAwMCIgc3RvcC1vcGFjaXR5PSIxIi8+CiAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiM0MjAwMDAiIHN0b3Atb3BhY2l0eT0iMSIvPgogIDwvbGluZWFyR3JhZGllbnQ+CiAgPHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjEiIGhlaWdodD0iMSIgZmlsbD0idXJsKCNncmFkLXVjZ2ctZ2VuZXJhdGVkKSIgLz4KPC9zdmc+);background:-moz-linear-gradient(top,#210000 0%,#420000 100%);background:-webkit-gradient(linear,left top,left bottom,color-stop(0%,#210000),color-stop(100%,#420000));background:-webkit-linear-gradient(top,#210000 0%,#420000 100%);background:-o-linear-gradient(top,#210000 0%,#420000 100%);background:-ms-linear-gradient(top,#210000 0%,#420000 100%);background:linear-gradient(to bottom,#210000 0%,#420000 100%);filter:progid:DXImageTransform.Microsoft.gradient( startColorstr="#210000",endColorstr="#420000",GradientType=0 )}body #header{height:6em;color:white;width:100%}body.black #header{background:url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEwAAABMCAIAAABI9cZ8AAABZUlEQVR4nN3RS47DMBAD0fKsdP/TejkLA0GQjyPLUjebvEDhgRsZa61F5rbI2LFg4b7v0ch4IcFPpgiJRGYJCUMmColB5goJQKYLWY1UELIUKSJkHVJHyCKklJAVSDUh05GCQuYiNYVMRMoKmYVUFjIFKS7kPlJfyE1kCSF3kFWEDCMLCRlD1hIygCwn5CqyopBLyKJC+pF1hXQiSwvpQVYX8hNpIOQc6SHkBGkj5BvSSchHpJmQd6SfkBekpZBnpKuQB9JYyIH0FgKbvRD4i4ylCFtrccgsIWFPJgqJQeYKCUCmC1mNVBCyFCkiZB1SR8gipJSQFUg1IdORgkLmIjWFTETKCpmFVBYyBSku5D5SX8hNZAkhd5BVhAwjCwkZQ9YSMoAsJ+QqsqKQS8iiQvqRdYV0IksL6UFWF/ITaSDkHOkh5ARpI+Qb0knIR6SZkHekn5AXpKWQZ6SrkAfSWMiB9BYC/zX14YmoQOPbAAAAAElFTkSuQmCC");border-bottom:1px solid #111}body.red #header{background:url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEwAAABMCAIAAABI9cZ8AAABY0lEQVR4nN3ay20DMRAE0bLODsb5x6UAfBAgCPqsuORwpqc7gcK7988fBbvm5i65OUgX/uYj84UkI0uEZCKrhKQhC4XkIGuFJCDLhexGKgjZihQRsg+pI2QTUkrIDqSakHCkoJBYpKaQQKSskCikspAQpLiQdaS+kEVkCyEryC5CppGNhMwhewmZQLYTchbZUcgpZFMh48i+QgaRrYWMILsL+Yo0EHKM9BBygLQR8gnpJOQt0kzIK9JPyBPSUsgj0lXIHWks5Ib0FgIXeyHJx4gS4TUTWSUkDVkoJAdZKyQBWS5kN1JByFakiJB9SB0hm5BSQnYg1YSEIwWFxCI1hQQiZYVEIZWFhCDFhawj9YUsIlsIWUF2ETKNbCRkDtlLyASynZCzyI5CTiGbChlH9hUyiGwtZATZXchXpIGQY6SHkAOkjZBPSCchb5FmQl6RfkKekJZCHpGuQu5IYyE3pLcQ+AdPQky88OH02AAAAABJRU5ErkJggg==");border-bottom:1px solid #420000}h1{font-weight:bold;padding:0.3em;padding-left:0.5em;padding-bottom:1.9em;font-weight:normal;font-size:3.5em}h2{padding-left:1.2em;padding-right:1.2em;padding-top:0.5em;font-weight:normal;font-size:1.5em;color:white} .n{font-weight:bold;color:#bbb;}.nn{color:#aaa;}#container{padding:1em;position:relative;top:3em;color:white;font-size:15px;font-weight:normal;margin-left:2em;margin-right:2em;font-family:courier}body.black #container{border:1px solid #222;background-color:#111}body.red #container{border:1px solid #420000;background-color:#280000}.footer{color:white;letter-spacing:-0.04em;margin:0;padding-bottom:0.3em;padding-top:0.3em;position:absolute;bottom:0px;width:100%;font-size:1.1em;height:1.3em}body.black .footer{border-top:1px solid #222;background-color:#111}body.red .footer{border-top:1px solid #420000;background-color:#280000}</style></head><body class="<%=theme%>"><div id="header"><h1><span class="n"><%=error_code%></span>&nbsp;<%=error_message%></h1></div><h2 class="n"><%=error_description%></h2><h2><%=error_details%></h2><div id="container" style="font: \'Courier New\', Courier, monospace"><%=error_stack%></div><p class="footer">&nbsp;&nbsp;&nbsp;<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALMAAAAZCAQAAADQmtfwAAAACXBIWXMAAAsTAAALEwEAmpwYAAAGvGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDIgNzkuMTYwOTI0LCAyMDE3LzA3LzEzLTAxOjA2OjM5ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDE4LTA5LTAzVDIyOjQ3OjUyKzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAxOC0wOS0wM1QyMjo1NiswMjowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAxOC0wOS0wM1QyMjo1NiswMjowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjEiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6ODcxNDU4ZGUtYTcyYi05YzQ5LTkzYjAtYzg2MzBlMmY1MDU4IiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ZjU4MDRjNWMtMjllMS05OTQwLTk2MTUtZjdhODQzZTdiM2I1IiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6YmI1YTc5YTgtZmU3Zi1kZDRiLWIxZjQtYmM2YjRjMjM3YzE1Ij4gPHBob3Rvc2hvcDpUZXh0TGF5ZXJzPiA8cmRmOkJhZz4gPHJkZjpsaSBwaG90b3Nob3A6TGF5ZXJOYW1lPSJNQU1MQU1CTyIgcGhvdG9zaG9wOkxheWVyVGV4dD0iTUFNTEFNQk8iLz4gPC9yZGY6QmFnPiA8L3Bob3Rvc2hvcDpUZXh0TGF5ZXJzPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmJiNWE3OWE4LWZlN2YtZGQ0Yi1iMWY0LWJjNmI0YzIzN2MxNSIgc3RFdnQ6d2hlbj0iMjAxOC0wOS0wM1QyMjo0Nzo1MiswMjowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTggKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjb252ZXJ0ZWQiIHN0RXZ0OnBhcmFtZXRlcnM9ImZyb20gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCB0byBpbWFnZS9wbmciLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjg3MTQ1OGRlLWE3MmItOWM0OS05M2IwLWM4NjMwZTJmNTA1OCIgc3RFdnQ6d2hlbj0iMjAxOC0wOS0wM1QyMjo1NiswMjowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTggKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpIaXN0b3J5PiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PuHpq8wAAANuSURBVGje7ZltnYQgEMY3ghGMYAQiGMEIRpgIRjDCRjCCEYxgg+c+LDcOAwywL/fhfgtfbk/Ahz/zAnjD7Vs/X78Ivpj/F+YehOlmFgwgjMknHVyidvzcgeAKo48g9Gq87lZd0Kc0qPGHwhgzSKhOjggHlxsHI0hVyQs3HACA2ZzGCQD6FZiwI1127vkovTH6BAA4eFkexVUB7jB7/XFZGQAAnNbCgQLVDlbZ9GzgMhoOngVu/l+GDNx9GwrQ75YWJXgzQJ3JHhWYMWQRyxHJ/1wMM0r3gG1EvvVqtl1CzFkZYm0psu9azFls15RaMWOo1HBBGwpmVItZqMNcbDuHmDOuLSzmwrwLF5qD2LVmMB+2HbVivrwAwN3UcEHbCmake8SRmUISwtzuoWI4XrwTfYh5S6YGaMw+mgJnnBZ/hSSiXCL6Y3saM7GGoaBB2mYijcvgl+qfNAtSAYOSGheOEwHmSEZgM9fgex6FgTmK/mGqacR85j3QwHyYZlTGPPqGU0DiSOc1prdrzEdmPQRmXtG7ZWXJnL1mw1EjZm61VGigeA4ZMypghtOLW0zw3ls1Zr2bSDzjKc7NmIMkpJNHE2ayWmUwn7FPsRmdacwyqInCBmaFDDn+hXmJZfBL1iRm14B50esu7Gh9AXPfgJm0T7EZnYyjDvP2y6iImTRm0jJ4wjv/9Txmx4JHZUeU61GDueapgHaEPsWapmyPLXdEeRqzlsG/XAZzy77ZYZDRX9hR9wrmln2zSGBbaEbGwizYgnrtSiaBeakPGhTK4InchaAXMIebn8uO8vb/fszivaM0ozzm7NWAj8/tKZCUG4mc+ibMHUf/SR5a/xQz+5Q0oxbM1yZO8MpcVLDPbhrzYO4tSMXsLVGPPLQIjnsZ81ahIRxf30D0zZhFurwWKwaNjs+Bs8KsZPhVekcKTOyU72aPNbpY/K3TsynQOHDl9iap+pjD6Uc72D/CA/8snnQxZnkpNKmpv455jG9QCjvtZJZ/HnPgU+zs5oEG1t65Qq+TV0cUydijM9fLmEX0p8oDzdsxC5+aqs6N5Tu6/E3h6d+RwNz5IO8+gvlxfSkPQdqp949jHvWtsepRuubdw+sq9NljTM/X+skrj7H0Uef5gh6j9TXlLwoGTC2fwSo/lE1X/oAL5vj9HPr9sv1v6g8qVKDXjpag4wAAAABJRU5ErkJggg==" style="height:16px" align="absbottom" title="MAMLAMBO"/>&nbsp; framework <span class="nn"><%=mamlambo_version%></span> | <span class="nn"><%=server_software%></span> | WSGI <span class="nn"><%=mod_wsgi_version%></span> | Python <span class="nn"><%=python_version%></span></p></body></html>'

        # new empty response object
        response_exception = Response.Response()

        text = DEFAULT_ERROR_PAGE_CONTENT

        if not description:
            description = ""

        if not details:
            details = ""

        print("Error " + str(http_code) + " " + error + " | " + details + " | " + description)

        if int(http_code) >= 500:
            theme = u"black"
        else:
            theme = u"red"
        text = text \
            .replace('<%=theme%>', theme) \
            .replace('<%=error_code%>', str(http_code)) \
            .replace('<%=error_message%>', error) \
            .replace('<%=error_description%>', description) \
            .replace('<%=error_details%>', details) \
            .replace('<%=error_stack%>', str(stack_trace)) \
            .replace('<%=mamlambo_version%>', Mamlambo.__version__) \
            .replace('<%=server_software%>', configuration.server_software) \
            .replace('<%=python_version%>', '.'.join(map(str, sys.version_info[:3]))) \
            .replace('<%=mod_wsgi_version%>', '.'.join(map(str, configuration.env_rsw['wsgi.version'])))

        response_exception.content_str = text
        response_exception.code = http_code
        response_exception.mime = "text/html"
        response_exception.end()

        return response_exception
