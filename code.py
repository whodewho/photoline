import web

render = web.template.render('templates/')

urls = ('/', 'Upload')

class Upload:
    def GET(self):
        return render.index();

    def POST(self):
        x = web.input(myfile={})
        filedir = '/path/where/you/want/to/save' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        raise web.seeother('/upload')
    	
if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()
