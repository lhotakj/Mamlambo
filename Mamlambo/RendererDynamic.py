#!/usr/bin/python3
# -*- coding: utf-8 -*-

import kajiki
import re
import os
import io
import copy
import json
from contextlib import redirect_stdout
from .Configuration import Configuration
from .MamlamboException import MamlamboException


class RendererDynamic:
    __page_raw = None
    __page_result = None
    __page_template = None
    __page_master = None
    __page_code = None  # filename with code behind
    __page_code_source = None  # source code of code behind
    __page_mime = None
    __http_code = 200
    __page_filename = None
    __type = None  # master | page
    __master_placeholders = None
    __page_placeholders = None
    __directive_attributes = None

    __is_nested_call = None
    __verbose = True

    def verbose(self, text):
        if self.__verbose:
            print(text)

    def __init__(self, file_name, is_fragment=False, is_nested_call=0):
        self.__page_mime = "text/html"
        self.__http_code = 200
        self.__page_filename = file_name
        self.__is_nested_call = is_nested_call
        self.verbose("RendererDynamic.init('" + str(file_name) + "',is_nested_call=" + str(is_nested_call) + ")")
        self.read_file()

        # detect <@page ... > ------------------------------------------------------------------------------------------
        regex_page = r"^(\s+|)*<%(\s+|)*[pP][aA][gG][eE](.*|\n)%>"
        self.verbose("RendererDynamic.after")
        self.verbose("ANALYSIS: --")
        self.verbose(self.__page_raw)
        self.verbose("ANALYSIS: --")
        matches = re.findall(regex_page, self.__page_raw, flags=re.IGNORECASE | re.MULTILINE)
        self.verbose("RendererDynamic.matches pages = " + str(matches))
        if len(matches) > 1:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!|||||!!
            # ! experimental error handling !!!!!!!!!!
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!|||||!!
            # apply to addl
            response_exception = MamlamboException.render(500,
                                                          error="Page directive error",
                                                          description="Multiple %page directives")
            self.__page_result = response_exception.content_bytes.decode('UTF-8')
            self.__page_code = response_exception.status
            self.__page_mime = response_exception.mime
            return
        elif len(matches) == 1:
            attributes_string = " ".join(list(matches[0])).replace("\n", "").strip()
            if not self.process_directive_attributes(attributes_string):
                return
            self.verbose("PAGE ATTRIBUTES: " + str(self.__directive_attributes))
            ok = self.process_directive_page(matches)
            self.verbose("OK in __init__ :" + str(ok))
            if not ok:
                return
            try:
                x = kajiki.xml_template.XMLTemplate(
                    source=self.__page_raw,
                    is_fragment=is_fragment,
                    encoding=u'utf-8',
                    autoblocks=None,
                    cdata_scripts=True,
                    strip_text=True)
                self.__page_result = x().render()
            except Exception as ex:
                response_exception = MamlamboException.render(500,
                                                              error="Page rendering error",
                                                              description="Error in rendering",
                                                              stack_trace=str(ex).replace("\n", "<br />"))
                self.__page_result = response_exception.content_bytes.decode('UTF-8')
                self.__http_code = response_exception.code
                self.__page_mime = response_exception.mime
                return
            return

        # detect <@master ... > ----------------------------------------------------------------------------------------
        regex_master = r"^(\s+|)*<%(\s+|)*[mM][aA][sS][tT][eE][rR](.*|\n)%>"
        matches = re.findall(regex_master, self.__page_raw, flags=re.IGNORECASE | re.MULTILINE)
        self.verbose("RendererDynamic.matches master = " + str(matches))
        if len(matches) > 1:
            self.__page_result = MamlamboException.render(500,
                                                          error="Page directive error",
                                                          description="Multiple %master directives")
            return
        elif len(matches) == 1:
            attributes_string = " ".join(list(matches[0])).replace("\n", "").strip()
            if not self.process_directive_attributes(attributes_string):
                return

            if self.__is_nested_call == 0:
                response_exception = MamlamboException.render(500, error="Invalid call",
                                                              description="Master page cannot be called")
                self.__page_result = response_exception.content_bytes.decode('UTF-8')
                self.__http_code = response_exception.code
                self.__page_mime = response_exception.mime
                return

            self.verbose("MASTER ATTRIBUTES: " + str(self.__directive_attributes))
            ok = self.process_directive_master(matches)
            if not ok:
                return

    def read_file(self):
        try:
            with open(self.__page_filename) as f:
                self.__page_raw = f.read().strip()
                return True
        except Exception as ex:
            response_exception = MamlamboException.render(500,
                                                          error="Page processing error",
                                                          description="File {file_name} cannot be loaded".format(
                                                              file_name=self.__page_filename))
            self.__page_result = response_exception.content_bytes.decode('UTF-8')
            self.__page_code = response_exception.status
            self.__page_mime = response_exception.mime
            return False

    @staticmethod
    def insert_str(string, str_to_insert, index):
        return string[:index] + str_to_insert + string[index:]

    def load_code(self):
        filename = self.__page_code  # solve paths
        r = ""
        try:
            with open(filename) as f:
                r = f.read()
        except Exception as ex:
            response_exception = MamlamboException.render(500,
                                                          error="Page processing error",
                                                          description="Code behind File `{file_name}` cannot be loaded".
                                                          format(
                                                              file_name=self.__page_code))
            self.__page_result = response_exception.content_bytes.decode('UTF-8')
            self.__page_code = response_exception.status
            self.__page_mime = response_exception.mime
            return None
        return r

    def first_tag(self, html):
        self.verbose('===')
        self.verbose(html)
        self.verbose('===')
        regex_tag = r"(<\s*[^>]*.>)"
        matches = re.finditer(regex_tag, html, re.MULTILINE)
        for matches_count, match in enumerate(matches):
            return match.groups()[0].strip()

    # accepting str like 'master="xx" code="xxx"'
    def parse_attributes(self, attributes):
        ret = dict()
        if not attributes:
            return ret
        regex = r"(\w+)=(?:[\"']?([^\"'>=]*)[\"']?)"
        matches = re.finditer(regex, attributes, re.MULTILINE)
        for matches_count, match in enumerate(matches):
            atr = match.groups()[0].strip().lower()
            val = match.groups()[1].strip()
            ret[atr] = val
        return ret

    # accepting str like 'master="xx" code="xxx"'
    def process_directive_attributes(self, attributes):
        code = ""
        file_name_folder = os.path.dirname(os.path.abspath(self.__page_filename))
        self.__directive_attributes = self.parse_attributes(attributes)
        for atr, val in self.__directive_attributes.items():
            if atr == "code":
                self.__page_code = val
                self.__page_code = os.path.join(file_name_folder, val)
                self.verbose("SOURCE=" + self.__page_code)
                if self.__page_code:
                    self.__page_code_source = self.load_code()
                    self.verbose("SOURCE_CODE=" + self.__page_code_source)
                    if not isinstance(code, str):
                        return False
            elif atr == "mime":
                self.__page_mime = val
            elif atr == "masterpage":
                # absolute like -- /var/www/html/folder/x
                self.__page_master = os.path.normpath(os.path.join(file_name_folder, val))
                # make dynamic -- /folder/x - hack!
                self.__page_master = self.__page_master.replace(Configuration().map_path("/"), "")
            else:

                response_exception = MamlamboException.render(500,
                                                              error="Page processing error",
                                                              description="Unknown attribute `{atr}`!".
                                                              format(
                                                                  atr=atr))
                self.__page_result = response_exception.content_bytes.decode('UTF-8')
                self.__page_code = response_exception.status
                self.__page_mime = response_exception.mime
                return False
        return True

    # https://regex101.com/r/WN3CUI/11 OK!
    def parse_page_placholders(self):
        self.verbose('parse_page_placholders')
        ms = list()
        # <py:placeholder ...> ... </py:placeholder>
        regex = r"<py:placeholder(?:|.|\n)(?P<attributes>[^>]*)>(?P<content>(|.|\n*)*((?!<\/(py:placeholder)>))*(?:|.|\n))(?P<close>(<\/(py:placeholder)(?:|.|\n)>))"
        # what if something in placeholder!

        matches = re.finditer(regex, self.__page_raw, re.MULTILINE | re.IGNORECASE)
        for matches_count, match in enumerate(matches, start=1):

            attributes = match.group('attributes')
            content = match.group('content')

            if attributes:
                m_attributes = self.parse_attributes(attributes)
            else:
                m_attributes = {}

            m_start = match.start()
            m_end = match.end()
            m_tag = match.group()
            ms.append(
                {'start': m_start, 'end': m_end, 'tag': m_tag, 'attributes': m_attributes, 'content': content})

        # non-pair tag
        # <py:placeholder ... />
        # https://regex101.com/r/slr9YK/1
        regex = r"<(py:placeholder)(?P<attributes>[^\/>]*)\/>"
        matches = re.finditer(regex, self.__page_raw, re.MULTILINE | re.IGNORECASE)
        for matches_count, match in enumerate(matches, start=1):
            attributes = match.group('attributes')
            content = ''
            if attributes:
                m_attributes = self.parse_attributes(attributes)
            else:
                m_attributes = {}
            m_start = match.start()
            m_end = match.end()
            m_tag = match.group()
            ms.append(
                {'start': m_start, 'end': m_end, 'tag': m_tag, 'attributes': m_attributes, 'content': content})

        self.__page_placeholders = ms

    def process_directive_master(self, matches):
        self.__type = "master"

        # remove master directive
        self.__page_raw = re.sub(r"^(\s+|)*<%(\s+|)*[mM][aA][sS][tT][eE][rR](.*|\n)%>", "", self.__page_raw)
        self.verbose("in " + self.__type)
        ms = list()

        # https://regex101.com/r/Z4tKDg/3
        # <py:placeholder ...> ... </py:placeholder>
        regex = r"<py:placeholder(?:|.|\n)(?P<attributes>[^>]*)>(?P<content>(|.|\n*)*((?!<\/(py:placeholder)>))*(?:|.|\n))(?P<close>(<\/(py:placeholder)(?:|.|\n)>))"
        matches = re.finditer(regex, self.__page_raw, re.MULTILINE | re.IGNORECASE)
        for matches_count, match in enumerate(matches, start=1):
            attributes = match.group('attributes')
            content = match.group('content')
            if attributes:
                m_attributes = self.parse_attributes(attributes)
            else:
                m_attributes = {}
            m_start = match.start()
            m_end = match.end()
            m_tag = match.group()
            ms.append(
                {'start': m_start, 'end': m_end, 'tag': m_tag, 'attributes': m_attributes, 'content': content})

        # non-pair tag
        # <py:placeholder ... />
        # https://regex101.com/r/slr9YK/1
        regex = r"<(py:placeholder)(?P<attributes>[^\/>]*)\/>"
        matches = re.finditer(regex, self.__page_raw, re.MULTILINE | re.IGNORECASE)
        for matches_count, match in enumerate(matches, start=1):
            attributes = match.group('attributes')
            content = ''
            if attributes:
                m_attributes = self.parse_attributes(attributes)
            else:
                m_attributes = {}
            m_start = match.start()
            m_end = match.end()
            m_tag = match.group()
            ms.append(
                {'start': m_start, 'end': m_end, 'tag': m_tag, 'attributes': m_attributes, 'content': content})

        self.__master_placeholders = ms
        return ms

    def process_directive_page(self, matches):
        self.__type = "page"
        self.__page_raw = re.sub(r"^(\s+|)*<%(\s+|)*[pP][aA][gG][eE](.*|\n)%>", "", self.__page_raw)
        self.verbose("in " + self.__type)
        masterpage = None  # to hold source code

        if self.__page_master:
            # print('-- using master page')
            page_master_file_name = Configuration().map_path(path_info=self.__page_master)
            self.verbose("!RendererDynamic('" + page_master_file_name + "')")
            masterpage = RendererDynamic(page_master_file_name, is_nested_call=1)
            self.verbose("!After RendererDynamic of master:" + str(masterpage))
            # print('-- master info')
            # print("master_placeholderse: " + str(masterpage.master_placeholders))
            # print("master_code:\n---\n" + str(masterpage.__page_code_source) + "\n---")
            # print('-- original page')
            self.parse_page_placholders()
            # print("page_placeholderse: " + str(self.page_placeholders))
            # print(self.__page_raw)
            # TODO:
            self.verbose("page_placeholderse: " + json.dumps(self.page_placeholders, indent=2))
            self.verbose("master_placeholderse: " + json.dumps(masterpage.master_placeholders, indent=2))

            # validate
            count_page_placeholders = len(self.page_placeholders)
            count_master_placeholders = len(masterpage.master_placeholders)
            if count_page_placeholders > count_master_placeholders:
                response_exception = MamlamboException.render(
                    500, error="Page processing error",
                    description="Inconsistency between mastepage and page. "
                                "The master page contains {m} placeholders, but the page has "
                                "defined more placeholder ({p})".format(m=str(count_master_placeholders),
                                                                        p=str(count_page_placeholders)))
                self.__page_result = response_exception.content_bytes.decode('UTF-8')
                self.__page_code = response_exception.status
                self.__page_mime = response_exception.mime
                return False
            if count_page_placeholders < count_master_placeholders:
                response_exception = MamlamboException.render(
                    500, error="Page processing error",
                    description="Inconsistency between mastepage and page. "
                                "The master page contains {m} placeholders, but the page has "
                                "defined less placeholder ({p})".format(m=str(count_master_placeholders),
                                                                        p=str(count_page_placeholders)))
                self.__page_result = response_exception.content_bytes.decode('UTF-8')
                self.__page_code = response_exception.status
                self.__page_mime = response_exception.mime
                return False

            new_page_raw = copy.copy(masterpage.__page_raw)
            # master page - attribute id validation
            for master_placeholder in masterpage.master_placeholders:
                if 'id' not in master_placeholder["attributes"]:
                    response_exception = MamlamboException.render(
                        500, error="Page processing error",
                        description="Error in masterpage. Missing attribute 'id' in tag {tag}"
                            .format(tag=self.first_tag(master_placeholder["tag"])))
                    self.__page_result = response_exception.content_bytes.decode('UTF-8')
                    self.__page_code = response_exception.status
                    self.__page_mime = response_exception.mime

                    return False
                else:
                    master_id = master_placeholder["attributes"]["id"]
                    new_content = None
                    for page_placeholder in self.page_placeholders:
                        if 'id' not in page_placeholder["attributes"]:
                            response_exception = MamlamboException.render(
                                500, error="Page processing error",
                                description="Error in page. Missing attribute 'id' in tag {tag}"
                                    .format(tag=self.first_tag(page_placeholder["tag"])))
                            self.__page_result = response_exception.content_bytes.decode('UTF-8')
                            self.__page_code = response_exception.status
                            self.__page_mime = response_exception.mime
                            return False
                        else:
                            self.verbose("---")
                            self.verbose(page_placeholder['attributes']['id'])
                            if page_placeholder['attributes']['id'] == master_id:
                                new_content = page_placeholder['content']
                                break
                    if not new_content:
                        response_exception = MamlamboException.render(
                            500, error="Page processing error",
                            description="Error in page. Cannot find placeholder from master in page with id='{id}'"
                                .format(id=master_id))
                        self.__page_result = response_exception.content_bytes.decode('UTF-8')
                        self.__page_code = response_exception.status
                        self.__page_mime = response_exception.mime
                        return False

                    new_page_raw = new_page_raw.replace(
                        master_placeholder["tag"],
                        new_content)

            self.__page_raw = new_page_raw

        # if page_code include the code.py
        regex_doctype = r"<[^\!].*[\^>]*>"  # tags not starting with <! like DOCTYPE
        matches = re.finditer(regex_doctype, self.__page_raw, re.MULTILINE)
        self.verbose('~~~~~~~~')
        self.verbose('self.__page_code_source: ' + str(self.__page_code_source))
        self.verbose('~~~~~~~~')
        found = False
        for matches_count, match in enumerate(matches, start=0):
            found = True
            # if page has source code, inject it after <!DOCTYPE>

            if masterpage and masterpage.page_code_source:
                include_master_page_source_code = masterpage.page_code_source
            else:
                include_master_page_source_code = ""

            if self.__page_code_source:
                self.__page_raw = self.insert_str(
                    self.__page_raw,
                    "\n<?python:\n" + include_master_page_source_code + "\n" + self.__page_code_source + "\n?>",
                    match.end())
            break

        if not found:
            try:
                with io.StringIO() as buf, redirect_stdout(buf):
                    exec(self.__page_code_source)
                    self.__page_result = buf.getvalue()
            except Exception as ex:
                response_exception = MamlamboException.render(
                    500, error="Page processing error",
                    description="Error executing code", details=str(ex))
                self.__page_result = response_exception.content_bytes.decode('UTF-8')
                self.__page_code = response_exception.status
                self.__page_mime = response_exception.mime
                return None
            finally:
                return False
        return True

    @property
    def page_raw(self):
        return self.__page_raw

    @page_raw.setter
    def page_raw(self, page_raw):
        self.__page_raw = page_raw

    @property
    def page_result(self):
        return self.__page_result

    @page_result.setter
    def page_result(self, page_result):
        self.__page_result = page_result

    @property
    def page_template(self):
        return self.__page_template

    @page_template.setter
    def page_template(self, page_template):
        self.__page_template = page_template

    @property
    def page_code(self):
        return self.__page_code

    @page_code.setter
    def page_code(self, page_code):
        self.__page_code = page_code

    @property
    def page_mime(self):
        return self.__page_mime

    @page_mime.setter
    def page_mime(self, page_mime):
        self.__page_mime = page_mime

    @property
    def page_filename(self):
        return self.__page_filename

    @page_filename.setter
    def page_filename(self, page_filename):
        self.__page_filename = page_filename

    @property
    def http_code(self):
        return self.__http_code

    @http_code.setter
    def http_code(self, http_code):
        self.__http_code = http_code

    @property
    def master_placeholders(self):
        return self.__master_placeholders

    @master_placeholders.setter
    def master_placeholders(self, master_placeholders):
        self.__master_placeholders = master_placeholders

    @property
    def page_placeholders(self):
        return self.__page_placeholders

    @page_placeholders.setter
    def page_placeholders(self, page_placeholders):
        self.__page_placeholders = page_placeholders

    @property
    def page_code_source(self):
        return self.__page_code_source


# main entry
class RendererMain:
    __page_result = ""
    __page_mime = None
    __http_code = 200

    # def __init__(self, file_name, is_fragment=False):
    def __init__(self, request, response):
        file_name = Configuration().map_path(path_info=request.path_info)
        markdown = RendererDynamic(file_name, is_fragment=False, is_nested_call=0)
        response.mime = markdown.page_mime
        response.content_str = markdown.page_result
        response.code = markdown.http_code
        response.end()

    @property
    def page_result(self):
        return self.__page_result

    @page_result.setter
    def page_result(self, page_result):
        self.__page_result = page_result

    @property
    def page_mime(self):
        return self.__page_mime

    @page_mime.setter
    def page_mime(self, page_mime):
        self.__page_mime = page_mime

    @property
    def http_code(self):
        return self.__http_code

    @http_code.setter
    def http_code(self, http_code):
        self.__http_code = http_code
