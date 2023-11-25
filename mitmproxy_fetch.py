from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import ctx

import re
import asyncio

class AddHeader:
    def __init__(self):
        self.summonURL = None
        self.debug     = open("debug.txt", "w")

    def request(self, flow):
        self.debug.write(flow.request.url)
        if (flow.request.method == "GET" and bool(re.search("query/summon", flow.request.url))):
            self.summonURL = flow.request.url
            with open('summonURL.txt',"w") as f:
                f.write(flow.request.url)

            self.debug.close()
            ctx.master.shutdown()


def start():
    myaddon = AddHeader()
    opts = options.Options(listen_host='127.0.0.1', listen_port=8080, confdir="./")
    pconf = proxy.config.ProxyConfig(opts)

    m = DumpMaster(opts, with_termlog=False, with_dumper=False)
    # m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)

    m.run()

    if myaddon.summonURL:
        return myaddon.summonURL
    

def threadstart():
    newloop = asyncio.new_event_loop()
    asyncio.set_event_loop(newloop)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start())
    except RuntimeError:
        pass
    loop.close()