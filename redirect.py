import requests

def requestRedirect(originalIp, redirectIp, originalPort, redirectPort):
    requests.post("mandarin-host:3000/v1/redirect",
    json={  'originalIp': originalIp ,
            'redirectIp' : redirectIp,
            'originalPort': originalPort,
            'redirectPort': redirectPort})
