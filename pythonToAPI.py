import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv("userAPICode.env")
api_key = os.getenv("OPENAI_API_KEY")
client = Groq(api_key=api_key)

previous = ["m","m"]
lines = ["","","","",""]
lines2 = ["c0204e21-c8ac-402b-994e-d2800b558c8d","06da7e97-f082-4031-bbae-80b2d1b84124"]

file_path = "chatGPTcontext.txt"
with open(file_path, 'r', encoding="utf-8") as f:
    file_contents = f.read()

inputPath = "itemInput.txt"
outputPath = "itemOutput.txt"

def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": file_contents},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

while True:
    backlogCheck = False
    time.sleep(.05)
    with open(inputPath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(outputPath, "r", encoding="utf-8") as f2:
        lines2 = f2.readlines()
    with open("backlogDoc.txt", "r", encoding="utf-8") as f3:
        backlogList = f3.readlines()

    if len(lines) < 3:
        continue

    if lines[3].strip() not in previous and lines[4].strip() not in previous:
        previous[0] = lines[3].strip()
        previous[1] = lines[4].strip()

        item1 = lines[0].rstrip("\n")
        item2 = lines[1].rstrip("\n")

        if (item1 + " + " + item2 + "\n") in backlogList or (item2 + " + " + item1 + "\n") in backlogList:
            if (item1 + " + " + item2 + "\n") in backlogList:
                loc = backlogList.index(item1 + " + " + item2 + "\n")
            else:
                loc = backlogList.index(item2 + " + " + item1 + "\n")
            lines2[0] = backlogList[loc+1][2:len(backlogList[loc+1])]
            print("PREVIOUSLY CRAFTED")
            backlogCheck = True
        else:
            lines2[0] = get_gpt_response(f"{item1} + {item2}")
            print("RAW OUT =", lines2[0])

        one = "true"
        for x in range(0,len(lines2[0])):
            if lines2[0][x].isdigit():
                one = "false"
        if one == "true":
            lines2[0] = "1 "+lines2[0]
            print("SINGULAR")
        
        chars = len(lines2[0])-1
        if lines2[0][chars].isdigit():
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

        with open(outputPath, 'w', encoding="utf-8") as f:
            f.writelines(lines2)

        if backlogCheck != True:
            with open("backlogDoc.txt", "a", encoding="utf-8") as backlogWrite:
                backlogWrite.write("\n"+item1+" + "+item2+"\n= "+lines2[0])

        time.sleep(.5)
        with open(outputPath, 'w', encoding="utf-8") as f:
            f.writelines(["."])
        print("Success")
        print(lines2[0])
        print(lines)
        print("\n\n")
