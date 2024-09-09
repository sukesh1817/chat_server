from mitmproxy import http

def response(flow: http.HTTPFlow):
    # redirect to different host
    if flow.request.pretty_host == "srechostel.in":
        flow.response.content = flow.response.content.replace("Login".encode(), "sujay".encode())

