from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
import Levenshtein
import re
import pytesseract
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ocrCanvasText={}
ocrCanvasCheck={}
saveString=""
textInImages=[]
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
def ocrCanvas(folderPath):
    global ocrCanvasText,ocrCanvasCheck,textInImages
    files=os.listdir(folderPath)
    pngFile=[file for file in files if file.endswith(".png")]
    excludePngFile=f"canvas_screenshot_{len(files)}.png"
    for file in pngFile:
        if file !=excludePngFile:
            path=f"{folderPath}/{file}"
            text=ocr_image(path)
            ocrCanvasText[file]=text
            ocrCanvasCheck[text]=False
            textInImages.append(text)
        else:
            path=f"{folderPath}/{file}"
            print(f"last paragraph:{ocr_image(path)}")
    # print(f"ocr Canvas:{textInImages}")
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
def checkRemoveTextInImage(string1,string2):
    string2=string2.rstrip()
    split_string = re.split(r'[.!?]', string2.rstrip())
    # print(split_string)
    if(len(string1)>len(string2)*1.5):
        return False
    if(levenshtein_similarity(string1,string2)>0.9):
        return True
    if(len(string1)<=len(string2)):
        for i in range(0,len(split_string)):
            if(levenshtein_similarity(string1[0:len(split_string[i])],split_string[i]))>0.9 and len(split_string[i])>0:
                count=len(split_string[i])
                s=string1[0:len(split_string[i])]
                # print(f"{s}:{count}")
                # print(f"{string1}:{len(string1)}")
                j=i+1
                similar=levenshtein_similarity(string1[0:len(split_string[i])],split_string[i])
                while count<len(string1)and j<len(split_string):
                    count+=len(split_string[j])
                    s+=split_string[j]
                    s=string1[0:count]
                    # print(f"reference:{string1[0:count]}")
                    # print(f"{s}:{count}:{levenshtein_similarity(string1[0:count],s)}")
                    similar=levenshtein_similarity(string1[0:count],s)
                    j+=1
                    if similar<0.85:
                        return False
                if similar>0.9:
                    return True
                
    return False
    
def sortText(folderPath):
    global ocrCanvasCheck,ocrCanvasText,saveString
    files=os.listdir(folderPath)
    listStringOCR=[]
    stringOCRAddion=[]
    mapIndex={}
    listString=[]
    result={}
    txtFile=[file for file in files if file.endswith(".txt")]
    for text in txtFile:
        if text=="screenshotText.txt":
            # print("đây này")
            path=f"{folderPath}/{text}"
            index=0
            with open(path,"r",encoding="utf-8") as file:
                for line in file:
                    line=remove_standalone_numbers(line)
                    if line not in mapIndex:
                            listStringOCR.append(line)
                            mapIndex[line]=index
                            index+=1
        elif text !="result.txt":
            path=f"{folderPath}/{text}"
            if text=="textCrawl0.txt":
                with open(path,"r",encoding="utf-8") as file:
                    for line in file:
                        line=remove_standalone_numbers(line)
                        if len(line)>1:
                            check=False
                            for ocrCanvas in ocrCanvasCheck:
                                # print("*************")
                                # print(line)
                                # print(ocrCanvas)
                                check=checkRemoveTextInImage(line,ocrCanvas)
                            # print(check)
                            if not check:
                                listString.append(line)
                                for key in ocrCanvasText:
                                    value=ocrCanvasText[key]
                                    if levenshtein_similarity(line,value)>0.8:
                                        ocrCanvasCheck[key]=True
                        
            # else:
            #     with open(path,"r",encoding="utf-8") as file:
            #         for line in file:
            #             line=remove_standalone_numbers(line)
            #             check=True
            #             for t in listString:
            #                 if levenshtein_similarity(line,t)>0.9:
            #                     check=False
            #                     break
            #             if len(line)>0 and check and line not in stringOCRAddion:
            #                 stringOCRAddion.append(line)      
    # print(stringOCRAddion)
    for line in stringOCRAddion:
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
                mergeString(line,stringOCRAddion,ocrCanvas,0)
                # if(len(saveString)>0):
                #     # print(saveString)
                #     listString.append(saveString)
            
    # print(f"len truoc set:{len(listString)}")
    listString=set(listString)
    # print(f"len sau set:{len(listString)}")
    for paragraph in listString:
        print(paragraph)
        max=0
        firstLine=""
        compareString=""
        if(len(paragraph)>120):
            compareString=paragraph[0:120]
        else:  compareString=paragraph
        # print(compareString)
        for line in listStringOCR:
            value=levenshtein_similarity(line,compareString)
            if value>max:
                max=value
                firstLine=line
        #     print(f"line:{line}:{value}")
        # print("**********")
        # print(f"final match:{firstLine}:{max}")
        index=mapIndex[firstLine]
        result[index]=paragraph
    sorted_dict = dict(sorted(result.items()))

    # Print the sorted dictionary
    with open(f"{folderPath}/result.txt","w",encoding="utf-8") as file:
        for key, value in sorted_dict.items():
            # print(f"{key}: {value}")
            file.write(f"{value}\n")
    # print(listStringOCR)
def levenshtein_similarity(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    max_length = max(len(str1), len(str2))
    if(max_length==0):
        similarity=0
    else:similarity = 1 - (distance / max_length)
    return similarity
str1="Ông biết rõ kết quả của việc đưa mình đi, không chỉ không ăn nói được với ba Lý Kiêu, mà cấp trên cũng sẽ nghi ngờ năng lực làm việc của ông.Dương Thụ gật đầu, gương mặt non nớt đã trở nên cứng cáp hơn: “Cô nói đúng! Sau đó tôi nghe thấy ông ta nói chuyện của cô liên quan đến hình ảnh của cả Quân khu 9 và vấn đề thu nhận binh lính sau này, nếu như rùm beng lên sẽ ảnh hưởng cực xấu, cho nên ông ta muốn nhân lúc đưa cô đi chuyển giao, để cô vô tình gặp phải Trí Tranh Bắc gì đó, xảy ra chuyện ngoài ý muốn, như vậy thì cũng coi như ăn nói được với ba Lý Kiều, đồng thời cũng không cần giao cho bộ Tư pháp giải quyết, quan trọng nhất chính là còn có thể có lý do tiến hành xử lý toàn bộ biên giới."
str2="Dương Thụ gật đầu, gương mặt non nớt đã trở nên cứng cáp hơn: “Cô nói đúng! Sau đó tôi nghe thấy ông ta nói chuyện của cô liên quan đến hình ảnh của cả Quân khu 9 và vấn đề thu nhận binh lính sau này, nếu như rùm beng lên sẽ ảnh hưởng cực xấu, cho nên ông ta muốn nhân lúc đưa cô đi chuyển giao, để cô vô tình gặp phải Trí Tranh Bắc gì đó, xảy ra chuyện ngoài ý muốn, như vậy thì cũng coi như ăn nói được với ba Lý Kiều, đồng thời cũng không cần giao cho bộ Tư pháp giải quyết, quan trọng nhất chính là còn có thể có lý do tiến hành xử lý toàn bộ biên giới.Ông biết rõ kết quả của việc đưa mình đi, không chỉ không ăn nói được với ba Lý Kiêu, mà cấp trên cũng sẽ nghi ngờ năng lực làm việc của ông."
# print(levenshtein_similarity(str1,str2))
ocrCanvas("Cưng Chiều Cô Vợ Quân Nhân full\Chương 3090 Có lẽ tôi không trở về được nữa\canvas")
sortText("Cưng Chiều Cô Vợ Quân Nhân full\Chương 3090 Có lẽ tôi không trở về được nữa")