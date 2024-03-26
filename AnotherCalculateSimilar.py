from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
import Levenshtein
import re
import pytesseract
from PIL import Image
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
saveString=""
def ocr_image(image_path):
    # Đọc văn bản từ ảnh sử dụng OCR
    text = pytesseract.image_to_string(Image.open(image_path),lang="vie",config="--psm 6",)
    return text

def remove_standalone_numbers(text):
    # Use regular expression to remove standalone numbers
    words=text.split(" ")
    res=""
    for word in words:
        word_without_numbers=word
        if not word.isdigit():
            # print("here")
            word_without_numbers =  re.sub(r'\d', '', word)
        res+=word_without_numbers+" "
    return res.rstrip()

def levenshtein_similarity(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    max_length = max(len(str1), len(str2))
    if(max_length==0):
        similarity=0
    else:similarity = 1 - (distance / max_length)
    return similarity
def ocrCanvas(folderPath):
    textOcr=[]
    files=os.listdir(folderPath)
    pngFile=[file for file in files if file.endswith(".png")]
    excludePngFile=f"canvas_screenshot_{len(files)}.png"

    for file in pngFile:
        if file !=excludePngFile:
            path=f"{folderPath}/{file}"
            text=ocr_image(path)
            textOcr.append(text)
        # else:
        #     path=f"{folderPath}/{file}"
        #     # print(f"last paragraph:{ocr_image(path)}")
    return textOcr
def mapStringCanvas(listString,stringReferences,listParagraph):
    global saveString
    mapString={}
    # print(stringAddion)
    for s in listString:
        # print(s)
        saveString=""
        for stringReference in stringReferences:
            # print("Phai giong tHANG NAY")
            # print(stringReference)
            mergeString(s,listString,stringReference,0)  
            if len(saveString)>0:
                mapString[s]=saveString
            else:
                listParagraph.append(s)
    # print(mapString)
    return mapString
def mergeString(currentString,listStringAddion,stringReference,max):
    global saveString
    similarity=levenshtein_similarity(currentString,stringReference)
    if levenshtein_similarity(currentString,stringReference[0:len(currentString)])<0.7:return

    if(len(currentString)>len(stringReference)+50):
        return
    if similarity>max:
        max=similarity
        if similarity>=0.8:
            # print(f"******************đạt:{currentString}")
            saveString=currentString
    for i in range(0,len(listStringAddion)):
        text=currentString+listStringAddion[i]
        # print(text)
        mergeString(text,listStringAddion,stringReference,max)
def getTextOcr(folderpath):
    path=f"{folderpath}/screenshotText.txt"
    stringOcr=[]
    with open(path,"r",encoding="utf-8") as file:
                for line in file:
                    line=remove_standalone_numbers(line)
                    if line not in stringOcr:
                            stringOcr.append(line)
    remove_similar_string(stringOcr)
    return stringOcr
def getTextCraw(folderpath):
    path=f"{folderpath}/textCrawl0.txt"
    stringOcr=[]
    with open(path,"r",encoding="utf-8") as file:
                for line in file:
                    line=remove_standalone_numbers(line)
                    if line not in stringOcr:
                            stringOcr.append(line)
    return stringOcr
def getStringAddion(folderpath,listString,listStringCanvas):
    files=os.listdir(folderpath)
    txtFile=[file for file in files if file.endswith(".txt")]
    stringOCRAddion=[]
    for text in txtFile:
        if text!="screenshotText.txt" and text!="result.txt" and text!="textCrawl0.txt":
            path=f"{folderpath}/{text}"
            with open(path,"r",encoding="utf-8") as file:
                for line in file:
                    line=remove_standalone_numbers(line)
                    check=True
                    for t in listString:
                        if levenshtein_similarity(line,t)>0.9:
                            check=False
                            break
                    if len(line)>0 and check and line not in stringOCRAddion:
                        stringOCRAddion.append(line)      
    # print(stringOCRAddion)
    return mapStringCanvas(stringOCRAddion,listStringCanvas,listString)
def remove_similar_string(strings, threshold=0.9):
    delString=[]
    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            if levenshtein_similarity(strings[i], strings[j]) > threshold:
                delString.append(strings[j])
    delString=set(delString)
    for s in delString:
        strings.remove(s)
    return strings

def sortText(folderpath):
    global saveString
    listStringOCR=getTextOcr(folderpath)
    listString=getTextCraw(folderpath)
    listStringCanvas=ocrCanvas(f"{folderpath}/canvas")
    listStringNeedVerified=[]
    # print(listStringCanvas)
    mapStringCanvas=getStringAddion(folderpath,listString,listStringCanvas)
    # print(mapStringCanvas)
    result={}
    for paragraph in listString:
        max=0
        firstLine=""
        for line in listStringOCR:
            if(len(paragraph)>len(line)):
                value=levenshtein_similarity(line,paragraph[0:len(line)])
            else:
                value=levenshtein_similarity(line[0:len(paragraph)],paragraph)
            if value>max:
                max=value
                if(max>0.8):
                    firstLine=line
        # print(firstLine)
        # index=listStringOCR.index(firstLine)
        # print("______________________paragraph")
        # print(f"{firstLine}:{max}")
        # print(f"{paragraph}:{index}")
        # if index in result:
        #     print("___________")
        #     print(f"index:{result[index]}")
        #     print(paragraph)
        # print(index)
        # print(firstLine)
        if(len(firstLine.rstrip())>0):
            index=listStringOCR.index(firstLine)
            result[index]=paragraph
        else:
            if(len(paragraph)>0):
                listStringNeedVerified.append(paragraph)
    # print(f"listStringNeedVerified:{listStringNeedVerified}")
    for paragraph in mapStringCanvas:
        max=0
        firstLine=""
        for line in listStringOCR:
            if(len(paragraph)>len(line)):
                    value=levenshtein_similarity(line,paragraph[0:len(line)])
            else:
                value=levenshtein_similarity(line[0:len(paragraph)],paragraph)
            if value>max:
                max=value
                if(max>0.8):
                    firstLine=line
        # print("______________________ mapstring")
        # print(f"{firstLine}:{max}")
        # print(f"{paragraph}:{index}")
        if(len(firstLine.rstrip())>0):
            index=listStringOCR.index(firstLine)
            result[index]=mapStringCanvas[paragraph]
        else:
            listStringNeedVerified.append(paragraph)
    sorted_dict = dict(sorted(result.items()))
    indexList=list(sorted_dict.keys())
    # print(indexList)
    for i in range(0,len(indexList)-1):
        s=sorted_dict[indexList[i]]
        begin=indexList[i]
        end=indexList[i+1]
        reference=""
        for j in range(begin,end):
            # print(f"begin:{begin}-end:{end}")
            reference=reference+" "+listStringOCR[j].rstrip()
        # print(f"string:{s}")
        # print(f"reference:{reference}")
        
        checkValue=levenshtein_similarity(s,reference)
        lenParagraph=len(s)
        lenReference=len(reference)+10
        if checkValue>=0.75 and lenParagraph<lenReference:
            # print("OK")
            # print(f"string:{s} {len(s)}")
            # print(f"reference:{reference} {checkValue} {len(reference)}")
            continue
        else:
            # print(f"something wrong:{checkValue>0.8}--{len(s)<len(reference)+10}")
            # print(f"{lenParagraph}-{lenReference}")
            # print(f"string:{s} {len(s)}")
            # print(f"reference:{reference} {checkValue} {len(reference)}")
            saveString=s
            mergeString(s,listStringNeedVerified,reference,checkValue)
            # print("++++++++++++++++")
            # print(saveString)
            sorted_dict[indexList[i]]=saveString
            
            # if(len(paragraph)<len(reference)+10 and checkValue<0.8):
                # print(f"string:{s}")
                # print(f"reference:{reference}")
                # print("something wrong")
            # else:
            #     temp=s
                # while(len(temp)<len(reference)):
                #     simliar=levenshtein_similarity(temp,reference)
                #     for string in listStringNeedVerified:
                #         newTemp=temp+" "+string.rstrip()
                #         newSimilar=levenshtein_similarity(newTemp,reference)
                #         if(simliar<newSimilar):
                #             temp=temp+" "+string.rstrip()
    # for key in sorted_dict:
    #     print(f"{key}: {sorted_dict[key]}")

    with open(f"{folderpath}/result.txt","w",encoding="utf-8") as file:
        for key, value in sorted_dict.items():
            # print(f"{key}: {value}")
            file.write(f"{value}\n")
        
    
        
# ocrCanvas("Cưng Chiều Cô Vợ Quân Nhân full\Chương 3090 Có lẽ tôi không trở về được nữa\canvas")
# sortText("Cưng Chiều Cô Vợ Quân Nhân full\Chương 3092 Có người thật!")