import os
import openai
import time
from dotenv import load_dotenv

load_dotenv("userAPICode.env")
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

previous = ["m","m"]
lines = ["","","","",""]
lines2 = ["c0204e21-c8ac-402b-994e-d2800b558c8d","06da7e97-f082-4031-bbae-80b2d1b84124"]

with open("ALLITEMS.txt","r") as file:
    items = file.readlines()
file.close()
for x in range(0,len(items)):
    items[x] = items[x].strip("\n")

for x in range(0,len(items),3):
    find = list(items[x])
    if "_" in find:
        while "_" in find:
            underscore = find.index("_")
            find[underscore] = " "
            finalString = "".join(find)
    else:
        finalString = str(find)
        finalString = "".join(find)
    items.append(finalString.title())

file_path = "chatGPTcontext.txt"
with open(file_path, 'r') as file:
        file_contents = file.read()

inputPath = "itemInput.txt"
outputPath = "itemOutput.txt"

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": str(file_contents)},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']


while True:
    backlogCheck = False
    time.sleep(.05)
    with open(inputPath, "r") as file:
        lines = file.readlines()
    file.close()
    with open(outputPath, "r") as file2:
        lines2 = file2.readlines()
    with open("backlogDoc.txt", "r") as file3:
        backlogList = file3.readlines()

    if len(lines) < 3:
        continue

    if lines[3] not in previous and lines[4] not in previous:

        previous[0]=(lines[3])
        previous[1]=(lines[4])

        item1 = lines[0][0:len(lines[0])-1]
        item2 = lines[1][0:len(lines[1])-1]

        
        if (item1 + " + " + item2 + "\n") in backlogList or (item2 + " + " + item1 + "\n") in backlogList:
            if (item1 + " + " + item2 + "\n") in backlogList:
                loc = backlogList.index(item1 + " + " + item2 + "\n")
            else:
                loc = backlogList.index(item2 + " + " + item1 + "\n")
            lines2[0] = backlogList[loc+1][2:len(backlogList[loc+1])]
            print("PREVIOUSLY CRAFTED")
            backlogCheck = True
        else:
            lines2[0] = get_gpt_response(str(item1+" + "+item2))
            print("RAW OUT =",lines2[0])


        one = "true"
        for x in range(0,len(lines2[0])):
            if lines2[0][x].isdigit():
                one = "false"
        if one == "true":
            lines2[0] = "1 "+lines2[0]
            print("SINGULAR")
        
        chars = len(lines2[0])-1
        if lines2[0][chars].isdigit() == True:
            print("rearranging")
            if lines2[0][chars-1] == " ":
                lines2[0] = (lines2[0][chars : chars+1] + " ") + lines2[0][0 : chars-1]
            else:
                lines2[0] = (lines2[0][chars-1 : chars+1] + " ") + lines2[0][0 : chars-2]
            print(lines2[0]+" rearranged")


        if "=" in lines2[0]:
            print("REARRANGING FOR EQUALS")
            eLoc = lines2[0].index("=")
            rearrange = lines2[0][eLoc+2 : len(lines2[0])]
            lines2[0] = rearrange



        if lines2[0][1] == " ":
            examine = lines2[0][2:len(lines2[0])]
        else:
            examine = lines2[0][3:len(lines2[0])]

        if examine == "sticks":
            examine = "stick"
            lines2[0] = "stick"

        print(examine)
        if examine not in items:
            while examine not in items:
                print("INVALID")
                lines2[0] = get_gpt_response(str(examine+" is not a valid item. Respond with only a valid, relevant option in the format of 'count itemID' and nothing else. Your next response must retain creativity whilst also staying relevant. Your two items to combine are " + item1 + " + " + item2))
                print(lines2[0])
                if lines2[0][1] == " ":
                    examine = lines2[0][2:len(lines2[0])]
                else:
                    examine = lines2[0][3:len(lines2[0])]
                print(examine)
                time.sleep(.5)

        with open(outputPath, 'w') as file:
            file.writelines(lines2)
        file.close()

        if backlogCheck != True:
            backlogWrite = open("backlogDoc.txt", "a")
            backlogWrite.write("\n"+item1+" + "+item2+"\n= "+lines2[0])
            backlogWrite.close()

        time.sleep(.5)
        replace = ["."]
        with open(outputPath, 'w') as file:
            file.writelines(replace)
        file.close()
        print("Success")
        print(lines2[0])
        print(lines)
        print("\n\n")