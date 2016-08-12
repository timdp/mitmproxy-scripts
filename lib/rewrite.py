from mitmproxy.models import HTTPResponse
from netlib.http import Headers

class Action(object):
    def __init__(self, _url):
        self.url = _url
    def __str__(self):
        return self.__class__.__name__ + "[" + self.url + "]"

class RewriteAction(Action):
    def perform(self, flow, qs):
        flow.request.url = self.url + qs

class RedirectAction(Action):
    def perform(self, flow, qs):
        resp = HTTPResponse("HTTP/1.1", 302, "Found",
                            Headers(Location = self.url + qs), "")
        flow.reply.send(resp)

def action_factory(actionType, destination):
    actionType = actionType.lower()
    if actionType == "rewrite":
        return RewriteAction(destination)
    if actionType == "redirect":
        return RedirectAction(destination)
    raise "Invalid action type: " + actionType

actions = {}
with open("config/rewrite.txt") as f:
    for line in f:
        if line.startswith("#") or " " not in line:
            continue
        (action_type, url, dest) = line.split()
        action = action_factory(action_type, dest)
        actions[url] = action
        print "Registered action: " + url + " -> " + str(action)

def rewrite(flow):
    try:
        pos = flow.request.url.index("?")
        request_url = flow.request.url[:pos]
        qs = flow.request.url[pos:]
    except:
        request_url = flow.request.url
        qs = ""
    if request_url in actions:
        print "Performing action for " + request_url + ": " + str(actions[request_url])
        actions[request_url].perform(flow, qs)
