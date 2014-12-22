import web
import os
import datetime
from random import Random


render = web.template.render('templates/')

urls = ('/', 'Index')

def random_str(randomlength=10):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

class Index:
    def GET(self):
        return render.index();

    def POST(self):
        # x = web.input(pic={})
        # filedir = 'upload' # change this to the directory you want to store the file in.
        # if 'pic' in x: # to check if the file-object is created
        #     filepath=x.pic.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
        #     filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
        #     fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
        #     fout.write(x.pic.file.read()) # writes the uploaded file to the newly created file.
        #     fout.close() # closes the file, upload complete.
        # raise web.seeother('/')

        dirpath = os.path.join(os.getcwd()+"/static/upload/", datetime.datetime.now().strftime("%Y-%m-%d"))
        if not os.path.exists(dirpath):
        	os.mkdir(dirpath)

        finalpath = os.path.join(dirpath, random_str())
        while os.path.exists(finalpath):
	        finalpath = os.path.join(dirpath, random_str())
        os.mkdir(finalpath)


        t = web.input(pageTitle={})
        tout = open(finalpath+"/title.txt", 'w')
        tout.write(t.pageTitle)
        tout.close()

        x = web.input(pic=[])
        y = web.input(des=[])
        i = 0
        for j in range(10):
            print j
        for p, d in zip(x['pic'], y['des']):
        	pout = open(finalpath+"/"+str(i)+'.jpg', 'w')
        	dout = open(finalpath+"/"+str(i)+'.txt', 'w')
        	pout.write(p)
        	dout.write(d)
        	pout.close()
        	dout.close()
        	i = i + 1

        folder = "/".join(finalpath.split('/')[-4:])
        return render.default(folder, i);


if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()
