#!/usr/bin/python

import sys
import os

if len(sys.argv) == 3:
    link = sys.argv[2]
else:
    link = 'https://msveiven.github.io'

def linkAllDirectories():

    os.chdir(os.environ['WIKIPROTPATH'])

    import webpageCreator
    webpageCreator.webpage(os.getcwd(), link)

    owd = os.environ['WIKIPROTPATH']+'/Scanners/'
    os.chdir(owd)
    directoryList1 = next(os.walk('.'))[1]
    #print(directoryList1)

    import webpageCreator
    #print(sys.argv[1])

    #url = sys.argv[1]
    #print(sys.argv[1])
    #webpageCreator.webpage(os.getcwd(), url)
    webpageCreator.webpage(os.environ['WIKIPROTPATH']+'/Scanners', link)
    #print('Now adding the links to the index file')

    #import directoryURLlink

    #    directoryURLlink.runCreateLinks(url)
    #directoryURLlink.runCreateLinks(link)

    i = 0
    while (i < len(directoryList1)):
        if (directoryList1[i] != 'apps'):
            if (directoryList1[i] != 'files'):
                if (directoryList1[i] != 'uploads'):
                    if (directoryList1[i] != '.idea'):
                        if (directoryList1[i] != '.git'):
                            import space_to_underscore

                            space_to_underscore.spaceToUnderscore(directoryList1[i])
                            import webpageCreator

            #                webpageCreator.webpage(os.path.abspath(directoryList1[i]), url)
                            webpageCreator.webpage(os.path.abspath(directoryList1[i]), link)
                            #print('Now adding the links to the index file')

    #                        import directoryURLlink

                            #    directoryURLlink.runCreateLinks(url)
    #                        directoryURLlink.runCreateLinks(link)

                            directoryList2 = next(os.walk('.'))[1]
                            sowd = os.getcwd()


                            j = 0
                            while (j < len(directoryList2)):
                                if (directoryList2[j] != 'apps'):
                                    if (directoryList2[j] != 'files'):
                                            if (directoryList2[j] != 'uploads'):
                                                if (directoryList2[j] != '.idea'):
                                                    if(directoryList2[j] != '.git'):
                                                        space_to_underscore.spaceToUnderscore(directoryList2[j])

            #                                           webpageCreator.webpage(os.path.abspath(directoryList2[j]), url)
                                                        webpageCreator.webpage(os.path.abspath(directoryList2[j]), link)
                                                        #print('Now adding the links to the index file')

                                                        #import directoryURLlink

                                                        #    directoryURLlink.runCreateLinks(url)
                                                        #directoryURLlink.runCreateLinks(link)

            #                                            print(os.getcwd())
                                                        os.chdir(sowd)
             #                                           print(os.getcwd())

                                j = j + 1

          #                  print(os.getcwd())
                            os.chdir(owd)
           #                 print(os.getcwd())

        i = i + 1

    return
def linkSingleDirectory():
    import webpageCreator
    webpageCreator.webpage(os.getcwd(), link)
#    print(link + '  ' + os.getcwd())
    return


if len(sys.argv) != 3:
    print('If you want to link all directories together with index.htm files, then write this: "python $WIKIPROTPATH/websiteCreatory.py all your_url". \n')
    print('If you want to update a single directory with links, first go to that specific directory, delete the index.htm file that you want to update, and then write this: "python $WIKIPROTPATH/websiteCreatory.py update_directory your_url"')

elif sys.argv[1].endswith('all'):
    linkAllDirectories()

elif sys.argv[1].endswith('update_directory'):
    linkSingleDirectory()


else:
    print('If you want to link all directories together with index.htm files, then write this: "python $WIKIPROTPATH/websiteCreatory.py all your_url". \n')
    print('If you want to update a single directory with links, first go to that specific directory, delete the index.htm file that you want to update, and then write this: "python $WIKIPROTPATH/websiteCreatory.py update_directory your_url"')
