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
ocrCanvasText={}
ocrCanvasCheck={}
saveString=""
textInImages=[]
ocrStringMap={}
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

def ocrCanvas(folderPath,stringAddion):
    global ocrCanvasText,ocrCanvasCheck,textInImages,ocrStringMap
    directory=folderPath+"/canvas"
    files=os.listdir(directory)
    pngFile=[file for file in files if file.endswith(".png")]
    excludePngFile=f"canvas_screenshot_{len(files)}.png"
    for file in pngFile:
        if file !=excludePngFile:
            path=f"{directory}/{file}"
            text=ocr_image(path)
            ocrCanvasText[file]=text
            ocrCanvasCheck[text]=False
            textInImages.append(text)
        else:
            path=f"{directory}/{file}"
            print(f"last paragraph:{ocr_image(path)}")

    for line in stringAddion:
        value=False
        for ocrCanvas in ocrCanvasCheck:
            if levenshtein_similarity(line,ocrCanvas)>0.95:
                value=ocrCanvasCheck[ocrCanvas]
                
        if not value:
            saveString=""
            for ocrCanvas in ocrCanvasCheck:
                # print("______________")
                # print(line)
                # print(ocrCanvas)
                if ocrCanvas not in ocrStringMap: 
                    mergeString(line,stringAddion,ocrCanvas,0)
                    if(len(saveString)>0):
                        ocrStringMap[ocrCanvas]=saveString
            
def mergeString(currentString,listStringAddion,stringReference,max):
    global saveString
    similarity=levenshtein_similarity(currentString,stringReference)
    # print("___________")
    # print(f"{currentString}:{similarity}")
    # print(stringReference)
    if(len(currentString)>len(stringReference)+5):
        return
    if similarity>max:
        max=similarity
        if similarity>=0.9:
            # print(currentString)
            saveString=currentString
    for i in range(0,len(listStringAddion)):
        text=currentString+listStringAddion[i]
        # print(text)
        mergeString(text,listStringAddion,stringReference,max)

def sortText(folderPath):
    
ocrCanvas("Cưng Chiều Cô Vợ Quân Nhân full\Chương 3090 Có lẽ tôi không trở về được nữa\canvas")
sortText("Cưng Chiều Cô Vợ Quân Nhân full\Chương 3090 Có lẽ tôi không trở về được nữa")