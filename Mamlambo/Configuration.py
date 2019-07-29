import os
import yaml
from .MamlamboException import MamlamboException
from . import Singleton
from .Response import Response
import re
from urllib.parse import urlparse


@Singleton.singleton_object
class Configuration(metaclass=Singleton.Singleton):
    __configuration = None
    __configuration_file = None
    __env_raw = None

    __document_root = None
    __extensions_static = []
    __extensions_dynamic = []
    __default_document = []
    __trailing_slash_redirect = False
    __redirections = None
    __routes = None

    __server_software = None  # read from env once

    __exception_response = None

    loaded = False

    def __init__(self):
        pass

    def map_path(self, path_info):
        return os.path.normpath(os.path.join(self.__document_root, path_info.lstrip('/')))

    def parse_config(self, env, path_to_configuration):

        self.__env_raw = env
        result_parse_env = self.parse_env()
        if isinstance(result_parse_env, Response):
            return result_parse_env

        if 'MAMLAMBO_CONFIGURATION' not in os.environ:
            if not path_to_configuration:
                return MamlamboException.render(
                    500,
                    "Missing configuration",
                    "Cannot locate configuration, "
                    "environment variable `MAMLAMBO_CONFIGURATION` neither `path_to_configuration` "
                    "was set.")
            else:
                if not os.path.isfile(path_to_configuration):
                    return MamlamboException.render(
                        500,
                        "Configuration file can't be found",
                        "Path `" + path_to_configuration + "` doesn't exist.")
                try:
                    self.__configuration = yaml.load(open(path_to_configuration))
                except Exception as e:
                    return MamlamboException.render(500,
                                                    "Invalid configuration",
                                                    "Configuration file can't be loaded. " + str(e))
                self.__configuration_file = path_to_configuration
        else:
            path_to_configuration = os.environ['MAMLAMBO_CONFIGURATION']
            if not os.path.isfile(path_to_configuration):
                return MamlamboException.render(
                    500,
                    "Configuration file can't be found",
                    "Path `" + path_to_configuration + "` doesn't exist.")
            try:
                self.__configuration = yaml.load(open(path_to_configuration))
            except Exception as e:
                return MamlamboException.render(500,
                                                "Invalid configuration",
                                                "Configuration file can't be loaded. " + str(e))
            self.__configuration_file = path_to_configuration

        result_parse_configuration = self.parse_configuration()
        if isinstance(result_parse_configuration, Response):
            return result_parse_configuration

        self.loaded = True
        return None

    def parse_env(self):
        if 'DOCUMENT_ROOT' in self.__env_raw:
            self.__document_root = self.__env_raw['DOCUMENT_ROOT']

        if 'SERVER_SOFTWARE' in self.__env_raw:
            self.__server_software = self.__env_raw['SERVER_SOFTWARE']
        else:
            self.__server_software = "Unidentified"

        if not self.__document_root and 'CONTEXT_DOCUMENT_ROOT' in self.__env_raw:
            self.__document_root = self.__env_raw['CONTEXT_DOCUMENT_ROOT']

        if not self.__document_root:
            return MamlamboException.render(
                500,
                "Invalid configuration",
                "Variable document_root missing. In case you host your application in Apache, check "
                "<a href='https://httpd.apache.org/docs/2.4/mod/core.html#documentroot'>Apache documentation</a>.")
        return None

    @staticmethod
    def parse_request(env, request):
        for env_key, env_value in env.items():
            # print(env_key + " = " + str(env_value))
            # add any items from dictionary starting with HTTP_ as request headers.
            # Example `HTTP_HOST` will become `host`
            if env_key.startswith("HTTP_"):
                request.add_header(env_key[5:].lower(), env_value)
            # add other `REQUEST_*` as they are
            if env_key.startswith("REQUEST_"):
                request.add_header(env_key, env_value)
            # add other `SERVER_*` as they are
            if env_key.startswith("SERVER_"):
                request.add_header(env_key, env_value)

        if 'REQUEST_METHOD' in env:
            request.method = env['REQUEST_METHOD']

        if 'REQUEST_SCHEME' in env:
            request.scheme = env['REQUEST_SCHEME']

        if 'QUERY_STRING' in env:
            request.query_string = env['QUERY_STRING']
            if request.query_string == "":
                request.query_string = None

        if 'REQUEST_URI' in env:
            request.uri = env['REQUEST_URI']  # with query params
            o = urlparse(request.uri)
            request.path_info = o.path  # without query
        else:
            return MamlamboException.render(
                500,
                "Invalid request",
                "The request doesn't contain `REQUEST_URI`. Check your server implementation.")
        return None

    def validate_rule(self, rules, mode):
        for old, new in rules.items():
            groups_old = re.compile(old).groups
            groups_new = 0
            if groups_old == 0:
                return True
            for x in range(groups_old):
                if "${" + str(x) + "}" in new:
                    groups_new += 1
            print("GROUPS ```````````````````")
            print("groups_old: " + str(groups_old))
            print("groups_new: " + str(groups_new))
            if groups_old != groups_new:
                return MamlamboException.render(
                    500,
                    "Invalid rule in {mode} configuration ",
                    "The rule `{old}:{new}` has mismatched number of regex groups and replacement "
                    "variables. Regex of for old has `{groups_old}` while the regex for new URL has "
                    "`{groups_new}`".format(
                        old=old, new=new, groups_old=str(groups_old), groups_new=str(groups_new),
                        mode=str(mode)))

            return True

    def parse_configuration(self):
        with open(self.__configuration_file, 'r') as stream:
            try:
                data = yaml.load(stream, Loader=yaml.SafeLoader)
                # extensions -------------------------------------------------------------------------------------------
                if 'extensions' not in data:
                    return MamlamboException.render(
                        500,
                        "Invalid configuration",
                        "Missing section `extensions`!")
                for item in data['extensions']:
                    extension = None
                    serve = None
                    mime = None
                    headers = None
                    methods = None
                    if 'extension' in item:
                        extension = item['extension']
                    else:
                        return MamlamboException.render(
                            500,
                            "Invalid configuration",
                            "`extension` not defined in `{item}`!".format(item=str(item)))
                    if 'serve' in item:
                        serve = item['serve'].lower()
                    else:
                        return MamlamboException.render(500,
                                                        "Invalid configuration",
                                                        "`serve` not defined in `{item}`!".format(item=str(item)))
                    if serve not in ["static", "dynamic"]:
                        return MamlamboException.redner(
                            500,
                            "Invalid configuration",
                            "`serve` must be set to `dynamic` or `static`. "
                            "Value `{serve}` not recognized`!".format(serve=str(serve)))
                    if 'mime' in item:
                        mime = item['mime'].lower()
                    else:
                        return MamlamboException.render(
                            500,
                            "Invalid configuration",
                            "`mime` not defined in `{item}`!".format(item=str(item)))
                    if 'headers' in item:
                        headers = item['headers']
                    if 'methods' in item:
                        methods = item['methods']

                    if serve == "static":
                        self.__extensions_static.append(
                            {extension: {"mime": mime, "headers": headers, "methods": methods}}
                        )
                    if serve == "dynamic":
                        self.__extensions_dynamic.append(
                            {extension: {"mime": mime, "headers": headers, "methods": methods}}
                        )

                # default_document -------------------------------------------------------------------------------------
                # TODO: type <>
                if 'default_document' in data:
                    if not isinstance(data['default_document'], list):
                        bad_type = str(type(data['default_document']))
                        return MamlamboException.render(
                            500,
                            "Invalid configuration",
                            "`default_document` must contain a list of file`! "
                            "Type `{bad_type}` is not allowed".format(bad_type=bad_type))
                    self.__default_document = list(data['default_document'])

                # trailing_slash_redirect ------------------------------------------------------------------------------
                # TODO: type <>
                if 'trailing_slash_redirect' in data:
                    if not isinstance(data['trailing_slash_redirect'], bool):
                        bad_type = str(type(data['trailing_slash_redirect']))
                        return MamlamboException.render(
                            500,
                            "Invalid configuration",
                            "`trailing_slash_redirect` must be a boolean value`! "
                            "Type `{bad_type}` is not allowed".format(bad_type=bad_type))

                    self.__trailing_slash_redirect = bool(data['trailing_slash_redirect'])

                # redirections -----------------------------------------------------------------------------------------
                # TODO: type <>
                if 'redirections' in data:
                    if not isinstance(data['redirections'], dict):
                        bad_type = str(type(data['redirections']))
                        return MamlamboException.render(
                            500,
                            "Invalid configuration",
                            "`redirections` must be a dictionary - "
                            "while the key is the old regex, and the value new regex! "
                            "Type `{bad_type}` is not allowed".format(bad_type=bad_type))

                    validation_result = self.validate_rule(data['redirections'], 'redirections')
                    if isinstance(validation_result, Response):
                        return validation_result

                    self.__redirections = data['redirections']

                # redirections -----------------------------------------------------------------------------------------
                # TODO: type <>
                if 'routes' in data:
                    if not isinstance(data['routes'], dict):
                        bad_type = str(type(data['routes']))
                        return MamlamboException.render(
                            500,
                            "Invalid configuration",
                            "`routes` must be a dictionary - "
                            "while the key is the old regex, and the value new regex! "
                            "Type `{bad_type}` is not allowed".format(bad_type=bad_type))

                    validation_result = self.validate_rule(data['redirections'], 'redirections')
                    if isinstance(validation_result, Response):
                        return validation_result

                    self.__routes = data['routes']

            except yaml.YAMLError as e:
                return MamlamboException.render(
                    500,
                    "Invalid configuration",
                    "Configuration file parse error. " + str(e))

    @property
    def extensions_dynamic(self):
        return self.__extensions_dynamic

    @property
    def extensions_static(self):
        return self.__extensions_static

    @property
    def document_root(self):
        return self.__document_root

    @property
    def server_software(self):
        return self.__server_software

    @property
    def default_document(self):
        return self.__default_document

    @property
    def trailing_slash_redirect(self):
        return self.__trailing_slash_redirect

    @property
    def redirections(self):
        return self.__redirections

    @property
    def routes(self):
        return self.__routes

    @property
    def env_rsw(self):
        return self.__env_raw
