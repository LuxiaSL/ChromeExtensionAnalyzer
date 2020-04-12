import os, json, pprint, re, clipboard
from hurry.filesize import size, si

pp = pprint.PrettyPrinter(indent=4)

extPath = "C:\\Users\\Steven\\Downloads\\ExtensionZip\\"

jsFiles = []
manifestJson = {}
jsonInfo = []
etcInfo = []
fileList = []
keywords = ['setIcon', 'setBadge', '\.post', '"POST"', '\.get', '"GET"']
caseInsensitve = ['icon', 'badge']

mainPrompt = '''Interface
1: View .js files and counts
2: manifest.json options
3: View .json files and contents
4: View etc file list
5: Copy the entire file list w/ sizes
0: Exit'''

manifestPrompt = '''Manifest Interface
1: See quick statuses
2: View entire contents

3: Return
0: Exit'''

def run_fast_scandir(dir):
    subfolders = []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            fileList.append({'path': f.path, 'partial-path': f.path.replace(extPath, ''), 'size': size(f.stat().st_size, system=si)})

    for dir in list(subfolders):
        run_fast_scandir(dir)

def ShowJSFiles():
    os.system('cls')
    colList = [*keywords, *caseInsensitve]
    printList = [['Files', *colList]]

    for jsFile in jsFiles:
        countStrs = []

        for col in colList:
            for word in jsFile['wordlist']['sensitive']:
                if col in word.keys():
                    countStrs.append(str(word[col]))
            for word in jsFile['wordlist']['insensitive']:
                if col in word.keys():
                    countStrs.append(str(word[col]))

        printList.append([jsFile['partial-path'], *countStrs])

    colSize = [max(map(len, col)) for col in zip(*printList)]
    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])

    printList.insert(1, ['-' * i for i in colSize])

    for row in printList: print(formatStr.format(*row))

    print('\n\n1: Return, literally anything else: Exit')

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum != 1:
            exit()
    else:
        exit()

def ShowManifestInt(err=False):
    if err:
        print("Err: Invalid number.\n\n")

    print(manifestPrompt)

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum < 1 :
            exit()
        elif currNum > 3:
            ShowManifestInt(True)
        elif currNum == 1:
            ShowManifestSpecific()
        elif currNum == 2:
            ShowEntireManifest()
        elif currNum != 3:
            ShowManifestInt(True)
    else:
        ShowManifestInt(True)

def ShowManifestSpecific():
    print('WIP')

def ShowEntireManifest():
    os.system('cls')

    pp.pprint(manifestJson)

    print('\n\n1: Return to Manifest, 2: Return to Main, literally anything else: Exit')

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum == 1:
            ShowManifestInt()
        elif currNum != 2:
            exit()
    else:
        exit()

def ShowJSONFiles():
    os.system('cls')

    for jsonFile in jsonInfo:
        print('Path: ' + jsonFile['partial-path'])
        pp.pprint(jsonFile['contents'])

    print('\n\nJSON ugly, you must be desperate')

    print('\n\n1: Return, literally anything else: Exit')

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum != 1:
            exit()
    else:
        exit()

def ShowEtcFiles():
    os.system('cls')

    colList = ['Path', 'Size']
    printList = [colList]

    for eachFile in etcInfo:
        printList.append([eachFile['partial-path'], eachFile['size']])

    colSize = [max(map(len, col)) for col in zip(*printList)]
    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])

    printList.insert(1, ['-' * i for i in colSize])

    for row in printList: print(formatStr.format(*row))

    print('\n\nUsually .html, or images')

    print('\n\n1: Return, literally anything else: Exit')

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum != 1:
            exit()
    else:
        exit()

def ShowFileList():
    os.system('cls')
    colList = ['Path', 'Size']
    printList = [colList]

    for eachFile in fileList:
        printList.append([eachFile['partial-path'], eachFile['size']])


    printStr = ""
    for row in printList:
        printStr += row[0] + '    ' + row[1] + '\n'

    clipboard.copy(printStr)

    colSize = [max(map(len, col)) for col in zip(*printList)]

    formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])

    printList.insert(1, ['-' * i for i in colSize])

    for row in printList: print(formatStr.format(*row))

    print('\n\nList copied to the clipboard automatically.')
    print('\n\n1: Return, literally anything else: Exit')

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum != 1:
            exit()
    else:
        exit()

def RetrieveSwitchNum(err=False):
    os.system('cls')
    if err:
        print("Err: Invalid number.\n\n")
    print(mainPrompt)

    inputNum = input("\n\n::")
    if inputNum.isnumeric():
        currNum = int(inputNum)
        if currNum < 1:
            exit()
        elif currNum > 5:
            RetrieveSwitchNum(True)
        else:
            return currNum
    else:
        RetrieveSwitchNum(True)

def ProcessJSFile( jsFile ):
    foundWords = {'sensitive': [], 'insensitive': []}
    with open(jsFile['path']) as File:
        fileData = File.read()
        for word in keywords:
            wordCount = len(re.findall(word, fileData))
            foundWords['sensitive'].append({word: wordCount})

        for word in caseInsensitve:
            wordCount = len(re.findall(word, fileData, re.IGNORECASE))
            foundWords['insensitive'].append({word: wordCount})

    return {'path': jsFile['path'], 'partial-path': jsFile['path'].replace(extPath, ''), 'wordlist': foundWords}

def ProcessManifestFile( manifest ):
    with open(manifest['path']) as File:
        manifestJson = json.load(File)
        return manifestJson

def ProcessJSONFile( jsonFile ):
    with open(jsonFile['path']) as File:
        jsonData = json.load(File)
        return {'path': jsonFile['path'], 'partial-path': jsonFile['path'].replace(extPath, ''), 'contents': jsonData}

def ProcessEtcFile( etcFile ):
    return etcFile

try:
    run_fast_scandir(extPath)

    for file in fileList:
        if file['path'].endswith('.js'):
            jsFiles.append(ProcessJSFile(file))
        elif file['path'].endswith('.json'):
            if 'manifest.json' in file['path']:
                manifestJson = ProcessManifestFile(file)
            else:
                jsonInfo.append(ProcessJSONFile(file))
        else:
            etcInfo.append(ProcessEtcFile(file))

except OSError:
    print("Error trying to open the extension folder at " + extPath + ".")

switchNum = -1
while switchNum != 0:
    switchNum = RetrieveSwitchNum()
    if switchNum == 1:
        ShowJSFiles()
    elif switchNum == 2:
        ShowManifestInt()
    elif switchNum == 3:
        ShowJSONFiles()
    elif switchNum == 4:
        ShowEtcFiles()
    elif switchNum == 5:
        ShowFileList()

