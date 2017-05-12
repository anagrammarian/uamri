#!/usr/bin/python

import sys
import os
import glob

# def runCreateLinks(url):
def runCreateLinks(link):
#    def createLinks(directory, url):
    def createLinks(directory):
        #print('the link is '+link)
        #print(os.getcwd()+'/index.html')
        if os.path.exists(os.getcwd()+'/index.html') or os.path.exists(os.getcwd()+'/index.htm'):
            print('index will now be updated!')
        else:
            f = open('index.html', 'w+')
            f.write('<!DOCTYPE html>\n <html>\n <body> \n  </body> \n </html> ')
            f.close()
        f = open('index.html', 'r')

        f.seek(0)
        s = f.read()
        R = s.split('</body>')
#        Path = os.getcwd().split('GitHub')
 #       PathLink = Path[1]
        PathLink = os.environ['WIKIPROTPATH']
    #    print(str(PathLink))
        f.close()

#        from websiteCreator import link
        f = open('index.html', 'w')
        f.write(R[0])
        f.write('<p>\n')
        #        f.write('<font size="5"><A HREF = "'+ url + str(PathLink) + '/' + directory + '">' + directory.split('.htm')[0].replace("_"," ") + '</A></font>')
        wikiprotpath = str(os.environ['WIKIPROTPATH'])
        #print(os.path.abspath(directory))
        #print('\n')
        #print(os.environ['WIKIPROTPATH'].split('/'))
        #print('\n'+os.environ['WIKIPROTPATH'].split('/')[len(os.environ['WIKIPROTPATH'].split('/'))-1])
        #print(os.path.abspath(directory).split(os.environ['WIKIPROTPATH'].split('/')[len(os.environ['WIKIPROTPATH'].split('/'))-2]))

        f.write('<font size="5"><A HREF = "' + str(link)+'/'+os.environ['WIKIPROTPATH'].split('/')[len(os.environ['WIKIPROTPATH'].split('/'))-2] + os.path.abspath(directory).split(os.environ['WIKIPROTPATH'].split('/')[len(os.environ['WIKIPROTPATH'].split('/'))-2])[1] + '">' + directory.split('.htm')[0].replace("_", " ") + '</A></font>\n </p> \n')
        f.write('</body>\n')
        f.write('</html>\n')

        f.close()

        return


    directoryList = next(os.walk('.'))[1]

    i = 0
    while (i < len(directoryList)):
        if (directoryList[i] != 'apps'):
            if (directoryList[i] != 'files'):
                if (directoryList[i] != 'uploads'):
                    if (directoryList[i] != '.git'):
#                    createLinks(directoryList[i], url)
                        createLinks(directoryList[i])
    #                print(directoryList[i])
        i = i + 1

    currentPath = os.getcwd()
    path = currentPath+"/*.htm"
    #print(path)

    for fname in glob.glob(path):
        if (fname != 'index.htm'):
            fname = fname.split("/")
            #print(fname)
#            createLinks(fname[len(fname)-1], url)
            createLinks(fname[len(fname)-1])

    return