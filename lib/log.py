from time import strftime, localtime

def log_combined(flow):
    client_ip = flow.client_conn.address.host
    date = strftime("%d/%b/%Y:%H:%M:%S", localtime(flow.request.timestamp_start))
    method = flow.request.method
    http_version = flow.request.http_version
    url = flow.request.url
    request = method + " " + url + " " + http_version
    try:
        referer = "\"" + flow.request.headers["referer"] + "\""
    except:
        referer = "-"
    try:
        user_agent = "\"" + flow.request.headers["user-agent"] + "\""
    except:
        user_agent = "-"
    print(client_ip + " - - [" + date + "] " +
        "\"" + request + "\" " +
        "- - " +
        "\"" + referer + "\" " +
        "\"" + user_agent + "\"")
