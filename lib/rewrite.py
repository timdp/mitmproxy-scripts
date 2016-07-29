from mitmproxy.models import HTTPResponse
from netlib.http import Headers

class Action:
    def __init__(self, url):
        self.url = url
    def __str__(self):
        return self.__class__.__name__ + "[" + self.url + "]"

class RewriteAction(Action):
    def perform(self, flow):
        flow.request.url = self.url

class RedirectAction(Action):
    def perform(self, flow):
        resp = HTTPResponse("HTTP/1.1", 302, "Found",
            Headers(Location=self.url), "")
        flow.reply.send(resp)

def action_factory(type, dest):
    type = type.lower()
    if type == "rewrite":
        return RewriteAction(dest)
    if type == "redirect":
        return RedirectAction(dest)
    raise "Invalid action type: " + type

actions = {}
with open("config/rewrite.txt") as f:
    for line in f:
        (action_type, url, dest) = line.split()
        action = action_factory(action_type, dest)
        actions[url] = action
        print("Registered action: " + url + " -> " + str(action))

def rewrite(flow):
    url = flow.request.url
    if url in actions:
        print("Performing action for " + url + ": " + str(actions[url]))
        actions[url].perform(flow)
