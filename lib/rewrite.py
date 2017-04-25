from fnmatch import fnmatch
from mitmproxy.http import HTTPResponse

actions = []

class Action(object):
    def __init__(self, _source_pattern, _destination, _options):
        self.source_pattern = _source_pattern
        self.destination = _destination
        self.options = _options
    def __str__(self):
        return self.__class__.__name__ + "[" + self.source_pattern + " -> " + self.destination + "]"
    def matches(self, url):
        return fnmatch(url, self.source_pattern)
    def build_destination(self, qs):
        dest = self.destination
        if self.options == "QSA":
            if "?" in self.destination:
                dest += "&"
            else:
                dest += "?"
            dest += qs[1:]
        return dest

class RewriteAction(Action):
    def perform(self, flow, qs):
        flow.request.url = self.build_destination(qs)

class RedirectAction(Action):
    def perform(self, flow, qs):
        flow.response = HTTPResponse.make(
            302,
            b"",
            {"Location": self.build_destination(qs)}
        )

def action_factory(action_type, source_pattern, destination, options):
    action_type = action_type.lower()
    if action_type == "rewrite":
        return RewriteAction(source_pattern, destination, options)
    if action_type == "redirect":
        return RedirectAction(source_pattern, destination, options)
    raise "Invalid action type: " + action_type

def load_actions():
    with open("config/rewrite.txt") as f:
        for line in f:
            if line.startswith("#") or " " not in line:
                continue
            parts = line.split()
            if len(parts) >= 4:
                (action_type, source_pattern, destination, options) = parts
            else:
                (action_type, source_pattern, destination) = parts
                options = ""
            action = action_factory(action_type, source_pattern, destination, options)
            actions.append(action)
            print("Registered action: " + str(action))
    return actions

def rewrite(flow):
    full_request_url = flow.request.url
    try:
        pos = full_request_url.index("?")
        qs = full_request_url[pos:]
    except:
        qs = ""
    for action in actions:
        if action.matches(full_request_url):
            print("Performing action for " + full_request_url + ": " + str(action))
            action.perform(flow, qs)
            break

load_actions()
