import web
import os
import datetime
from random import Random
import pickle, pprint
import sae
from sae.storage import Bucket
from sae.storage import Connection
from sae.storage import Error
from base64 import decodestring
from datetime import date

# render = web.template.render('templates/')

web.config.debug = True

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)


urls = ('/', 'Index',
        '/default/(.*)/(.*)', 'Default')

def random_str(randomlength=10):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

class Default():
    def GET(self, bucketId, tupleId):
        conn = sae.storage.Connection()
        bucket = conn.get_bucket(bucketId)
        data = pickle.loads(bucket.get_object_contents(tupleId+"/config.txt"))
        # data['des'] = [x.replace("\r\n", "<br>") for x in data['des']]
        urlPrefix = bucket.generate_url(tupleId+"/config.txt")[:-11];
        data['urlPrefix'] = urlPrefix
        return render.default(web.storage(data))

class Index:
    def GET(self):
        return render.index();

    def POST(self):
        # chars='aabcdefghijklmnopqrstuvwxyz0123456789'
        # bucketId = chars[date.today().day]
        bucketId = 't'
        bucket = Bucket(bucketId)

        tupleId = random_str()
        while True:
            try:
                if list(bucket.list(prefix=tupleId)):
                    tupleId = random_str()
                else:
                    break
            except sae.storage.Error:
                pass
        
        x = web.input(pic=[])
        y = web.input(des=[])
        t = web.input(pageTitle={})

        data = {}
        data['title']=t.pageTitle
        data['des']=[]

        i = 0
        for p, d in zip(x['pic'], y['des']):
            if len(p)==0:
                continue
            bucket.put_object(tupleId+"/"+str(i)+'.jpg', decodestring(p[23:]))
            data['des'].append(d)
            i = i + 1

        if i == 0:
            return render.index()

        data['number']=i

        bucket.put_object(tupleId+"/config.txt", pickle.dumps(data))

        raise web.seeother("/default/"+bucketId+"/"+tupleId)


app = web.application(urls, globals()) 
if __name__ == "__main__":
   app.run()
else:
    application = sae.create_wsgi_app(app.wsgifunc())

