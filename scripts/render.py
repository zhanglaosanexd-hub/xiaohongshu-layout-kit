#!/usr/bin/env python3
"""Generate separate 1080x1440 PNGs from Skill JSON. Python 3.9+, Pillow."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
def font(size, bold=False):
    for path in ([
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ] if bold else [
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def line(draw, text, xy, size=38, fill="#171717", bold=False, spacing=14):
    f = font(size, bold)
    draw.multiline_text(xy, str(text), font=f, fill=fill, spacing=spacing)

def frame(img, draw, box, source, root):
    x0,y0,x1,y1 = box
    draw.rounded_rectangle(box, radius=25, fill="#E9E9ED")
    if source:
        f = (root / source).resolve()
        if f.is_file():
            im=Image.open(f).convert("RGB")
            target=(x1-x0,y1-y0)
            from PIL import ImageOps
            crop=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS)
            img.paste(crop,(x0,y0))

def render(page, root, target):
    kind=page.get("type",page.get("template","T03"))
    img=Image.new("RGB",(W,H),"white")
    d=ImageDraw.Draw(img)
    accent="#348BD4"
    tag=page.get("tag","小红书图文")
    title=page.get("title","")
    sub=page.get("subtitle","")
    items=page.get("items",[])
    if kind=="T02":
        frame(img,d,(0,0,W,830),page.get("image",""),root)
        line(d,tag,(90,900),25,accent)
        line(d,title,(90,967),67,bold=True)
        line(d,sub,(90,1230),29,fill="#777777")
    elif kind=="T08":
        line(d,tag,(80,505),27,accent)
        line(d,title,(80,580),78,bold=True,spacing=25)
        line(d,page.get("body",""),(80,1075),28,fill="#777777")
    elif kind=="T11":
        frame(img,d,(80,80,1000,1035),page.get("image",""),root)
        line(d,title,(80,1090),67,bold=True)
        line(d,sub,(80,1295),29,fill="#777777")
    else:
        line(d,tag,(80,72),26,accent)
        line(d,title,(80,126),64,bold=True,spacing=15)
        line(d,sub,(80,345),27,fill="#777777")
        if kind=="T01":
            frame(img,d,(80,485,1000,1290),page.get("image",""),root)
        elif kind=="T03":
            frame(img,d,(80,500,1000,1315),page.get("image",""),root)
        elif kind=="T10":
            d.rounded_rectangle((80,495,1000,1300),radius=26,fill="#F5F5F7")
            line(d,page.get("prompt",""),(110,548),31,spacing=19)
        elif kind=="T09":
            for i,it in enumerate(items[:3]):
                y=500+i*265
                d.rounded_rectangle((80,y,1000,y+230),radius=25,fill="#F5F5F7")
                line(d,str(it.get("value","00"))+str(it.get("unit","")),(110,y+64),58,bold=True)
                line(d,it.get("title",""),(485,y+40),34,bold=True)
                line(d,it.get("desc",""),(485,y+105),25,fill="#777777")
        elif kind=="T05":
            for i,it in enumerate(items[:3]):
                y=490+i*270
                d.rounded_rectangle((80,y,1000,y+245),radius=25,fill="#F5F5F7")
                frame(img,d,(108,y+22,424,y+222),it.get("image",""),root)
                line(d,it.get("title",""),(470,y+52),35,bold=True)
                line(d,it.get("desc",""),(470,y+125),26,fill="#777777")
        elif kind in ("T04","T06","T07"):
            if kind=="T04":
                positions=[(80,490,1000,830),(80,855,535,1260),(555,855,1000,1260)]
            elif kind=="T07":
                positions=[(80,490,530,1260),(550,490,1000,1260)]
            else:
                positions=[(80,490,530,860),(550,490,1000,860),(80,885,530,1260),(550,885,1000,1260)]
            for i,(x0,y0,x1,y1) in enumerate(positions):
                it=items[i] if i<len(items) else {}
                d.rounded_rectangle((x0,y0,x1,y1),radius=22,fill="#F5F5F7")
                frame(img,d,(x0+15,y0+15,x1-15,y1-102),it.get("image",""),root)
                line(d,it.get("title",""),(x0+22,y1-91),28,bold=True)
                line(d,it.get("desc",""),(x0+22,y1-54),19,fill="#777777")
    img.save(target)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out",default="output")
    parser.add_argument("--contact-sheet",action="store_true")
    args=parser.parse_args()
    source=Path(args.input).resolve()
    data=json.loads(source.read_text(encoding="utf-8"))
    output=Path(args.out); output.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for i,page in enumerate(data["pages"],1):
        kind=page.get("type",page.get("template","T03"))
        name=f"{i:02d}-{kind}.png"
        render(page,source.parent,output/name)
        manifest.append({"page":i,"template":kind,"file":name})
        print(output/name)
    (output/"pages-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    (output/"content.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    if args.contact_sheet:
        from PIL import ImageOps
        thumbs=[Image.open(output/m["file"]).resize((270,360)) for m in manifest]
        cols=4; rows=(len(thumbs)+cols-1)//cols
        sheet=Image.new("RGB",(cols*270,rows*360),"#DDDDDF")
        for i,thumb in enumerate(thumbs):
            sheet.paste(thumb,((i%cols)*270,(i//cols)*360))
        sheet.save(output/"contact-sheet.png")
if __name__=="__main__":
    main()
