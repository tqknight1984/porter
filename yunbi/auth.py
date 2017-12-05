import hmac
import hashlib
import time
import urllib

class Auth():
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def urlencode(self, params):
        keys = params.keys()
        keys.sort()
        query = ''
        for key in keys:
            value = params[key]
            if key != "orders":
                query = "%s&%s=%s" % (query, key, value) if len(query) else "%s=%s" % (key, value)
            else:
                #this ugly code is for multi orders API, there should be an elegant way to do this
                d = {key: params[key]}
                for v in value:
                    ks = v.keys()
                    ks.sort()
                    for k in ks:
                        item = "orders[][%s]=%s" % (k, v[k])
                        query = "%s&%s" % (query, item) if len(query) else "%s" % item
        return query

    def sign(self, verb, path, params=None):
        query = self.urlencode(params)
        msg = "|".join([verb, path, query])
        signature = hmac.new(self.secret_key, msg=msg, digestmod=hashlib.sha256).hexdigest()
        return signature

    def sign_params(self, verb, path, params=None):
        if not params:
            params = {}
        tonce = int(1000*time.time())
        # print 'tonce' , tonce
        params.update({'tonce': tonce, 'access_key': self.access_key})
        query = self.urlencode(params)
        signature = self.sign(verb, path, params)
        return signature, query
