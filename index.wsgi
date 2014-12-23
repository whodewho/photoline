import web
import os
import datetime
from random import Random
import pickle, pprint
import sae

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
    def GET(self, dateStr, randomFolder):
        dReader = open("static/upload/"+dateStr+"/"+randomFolder+"/config.txt", 'rb')
        data = pickle.load(dReader)
        data['dateStr'] = dateStr
        data['randomFolder'] = randomFolder
        # data['des'] = [x.replace("\r\n", "<br>") for x in data['des']]
        return render.default(web.storage(data))

class Index:
    def GET(self):
        return render.index();

    def POST(self):
        dirpath = os.path.join(os.path.join(app_root, "static/upload/"), datetime.datetime.now().strftime("%Y-%m-%d"))
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        finalpath = os.path.join(dirpath, random_str())
        while os.path.exists(finalpath):
            finalpath = os.path.join(dirpath, random_str())
        os.mkdir(finalpath)

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
            pReder = open(finalpath+"/"+str(i)+'.jpg', 'w')
            data['des'].append(d)
            pReder.write(p)
            pReder.close()
            i = i + 1
        data['number']=i

        dReader = open(finalpath+"/config.txt", 'wb')
        pickle.dump(data, dReader)
        dReader.close()

        raise web.seeother('/default/'+"/".join(finalpath.split('/')[-2:]))


app = web.application(urls, globals()) 
if __name__ == "__main__":
   app.run()
else:
    application = sae.create_wsgi_app(app.wsgifunc())

