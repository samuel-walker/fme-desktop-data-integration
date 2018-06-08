import re

line = "<br><br><img src=\"./Images/Img2.012.GrayedOutFeatureAttrs.png\">"

imgsplit = ""
tags = re.split(r'(?<=>)(.+?)(?=<)', line.strip())
print(tags)
for i in tags:
  if "img src=" in i:
      imgsplit = i

imgsplit = imgsplit.split("\"")[1].split("/")[2]
print(imgsplit)

line = "![](./Images/Img2.012.GrayedOutFeatureAttrs.png)"
imgsplit = line.strip()[6:-1].rsplit('/', 1)[-1]
print(imgsplit)
