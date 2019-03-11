from shutil import *
import os
import datetime
from subprocess import call
from tkinter import *
from tkinter import filedialog

notDuplicates = []
viableDates = []
rawFileExtension = ".CR2"
jpegFileExtension = ".JPG"
jpegFileExtension2 = ".jpg"
movieFileextension = ".MP4"
timelapseFileExtension = ".MOV"
checkList = []

root = Tk()

rawVar = IntVar()
jpegVar = IntVar()
soundVar = IntVar()

frame = Frame(root)
frame.pack()

progressBar = Frame(root)
progressBar.pack(side=BOTTOM)

fromlabel = Label(frame)
targetlabel = Label(frame)
rawCheck = Checkbutton(frame, text=".CR2", variable=rawVar)
jpegCheck = Checkbutton(frame, text=".JPG", variable=jpegVar)
soundCheck = Checkbutton(frame, text="Sound when done", variable=soundVar)

fromlabel.config(text="Copy from: ")
targetlabel.config(text="Copy to: ")

fromlabel.pack(side=TOP)
targetlabel.pack(side=TOP)
soundCheck.pack(side=BOTTOM)
jpegCheck.pack(side=BOTTOM)
rawCheck.pack(side=BOTTOM)

progress = Label(progressBar)
progress.pack(side=BOTTOM)

subDir = ""


def creationDate(filepath):
    return os.stat(filepath).st_birthtime


def checkNotDuplicate(checked):
    for name in notDuplicates:
        if name == checked:
            return True
    return False


def duplicate(filepath, filename):
    if not checkNotDuplicate(filename):
        try:
            for file in os.listdir(filepath):
                if filename == str(file):
                    return True
            return False
        except:
            return False


def getFromDir():
    global fromDir
    filepath = filedialog.askdirectory()
    fromlabel.config(text="Copy from: "+filepath)
    fromDir = filepath


def getTargetDir():
    global targetDir
    filepath = filedialog.askdirectory()
    targetlabel.config(text="Copy to: "+filepath)
    targetDir = filepath


def findTotalElements():
    global totalNumberElements
    totalNumberElements = 0
    for file in os.listdir(fromDir):
        if checkFileExtension(str(file)[-4:]):
            createTime = datetime.date.fromtimestamp(
                creationDate(fromDir + "/" + file))
            if not duplicate(targetDir + "/" + str(createTime)[5:], str(file)):
                totalNumberElements += 1
                notDuplicates.append(str(file))
                viableDates.append(createTime)


def handleCheckBoxes():
    if rawVar.get() == 1:
        checkList.append(rawFileExtension)
    if jpegVar.get() == 1:
        checkList.append(jpegFileExtension)
        checkList.append(jpegFileExtension2)


def checkFileExtension(fileextension):
    if fileextension == movieFileextension or fileextension == timelapseFileExtension:
        return True

    for element in checkList:
        if fileextension == element:
            return True
    return False


def transfer():
    global numberCopied
    numberCopied = 0

    if targetDir == "" or fromDir == "":
        return

    filesCopied = 0
    handleCheckBoxes()
    findTotalElements()

    for file in os.listdir(fromDir):
        currentFileExtension = str(file)[-4:]
        if checkFileExtension(currentFileExtension):
            createTime = datetime.date.fromtimestamp(
                creationDate(fromDir + "/" + file))
            if createTime not in viableDates:
                pass

            if not os.path.exists(targetDir+"/"+str(createTime)[5:]):
                os.makedirs(targetDir+"/"+str(createTime)[5:])
                subDir = targetDir+"/"+str(createTime)[5:]

                os.makedirs(subDir+"/jpg")
                os.makedirs(subDir+"/raw")
                os.makedirs(subDir+"/video")

                if currentFileExtension == rawFileExtension:
                    copy2(fromDir+"/"+file, subDir+"/raw")
                elif currentFileExtension == jpegFileExtension or currentFileExtension == jpegFileExtension2:
                    copy2(fromDir+"/"+file, subDir+"/jpg")
                else:
                    copy2(fromDir+"/"+file, subDir+"/video")

                filesCopied += 1
                numberCopied += 1
            else:
                if checkNotDuplicate(str(file)):
                    subDir = targetDir+"/"+str(createTime)[5:]

                    if not os.path.exists(subDir + "/jpg"):
                        os.makedirs(subDir+"/jpg")
                    if not os.path.exists(subDir + "/raw"):
                        os.makedirs(subDir+"/raw")
                    if not os.path.exists(subDir + "/video"):
                        os.makedirs(subDir+"/video")

                    if currentFileExtension == rawFileExtension:
                        copy2(fromDir+"/"+file, subDir+"/raw")
                    elif currentFileExtension == jpegFileExtension or currentFileExtension == jpegFileExtension2:
                        copy2(fromDir+"/"+file, subDir+"/jpg")
                    else:
                        copy2(fromDir+"/"+file, subDir+"/video")

                    filesCopied += 1
                    numberCopied += 1

            updatep_rogress()
            root.update()

    if soundVar.get() == 1:
        if filesCopied == 1:
            call(['say', 'Done copying one file.'])
        else:
            call(['say', 'Done copying ' + str(filesCopied) + ' files.'])


def updatep_rogress():
    progress.config(text="Files copied: "+str(numberCopied) +
                    " / "+str(totalNumberElements))


browsebutton = Button(root, text="Choose from directory", command=getFromDir)
browsebutton2 = Button(
    root, text="Choose target directory", command=getTargetDir)
startbutton = Button(root, text="Copy files", command=transfer)

browsebutton.pack(side=TOP)
browsebutton2.pack(side=TOP)
startbutton.pack(side=BOTTOM)

root.mainloop()
