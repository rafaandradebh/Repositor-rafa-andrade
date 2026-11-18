import glob, os, subprocess, sys
S="/tmp/claude-0/-home-user-Repositor-rafa-andrade/ba5a56bd-caf9-52d9-82ca-c7bca9591c77/scratchpad"
B=S+"/build"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def src(key):
    if key=="7DD8": return glob.glob(S+"/raw2/*7DD8*")[0]
    m=sorted(glob.glob(S+f"/raw*/*IMG_{key}.*"))
    return m[-1] if key in("1334","1335","1336") else m[0]
# bloco: (tag, legenda, [(clip, inicio, duração)])
V=[
("", "3 DIAS COM 2 FILHOS", [("7DD8",12,2.8),("1304",1,2.8),("1311",2,2.8)]),
("", "A 52 km de BH  |  9 km do Inhotim", [("1325",5,2.5),("1325",1,2.5),("1326",3,2.5)]),
("MANHÃ", "Café da manhã incluso", [("1338",0.5,3.0),("1339",1,2.8),("1340",6,2.8)]),
("MANHÃ", "Ordenha e cavalgada incluídas", [("1266",2,2.7),("1268",3,2.6),("1269",0.5,2.7),("1270",1,2.6)]),
("ALMOÇO", "Almoço incluso", [("1316",1,2.0),("1318",1.5,2.2),("1320",1.5,2.2),("1314",0.5,2.1)]),
("TARDE", "3 piscinas  |  cascata natural", [("1304",8,2.6),("1311",7,2.6),("1282",8,2.6)]),
("TARDE", "Parquinho e cama elástica", [("1342",6,2.8),("1344",3,2.8)]),
("NOITE", "Jantar incluso", [("1334",0,2.2),("1335",0.3,2.2),("1336",0,1.2)]),
("QUARTOS", "Quase 40 quartos", [("1236",3,2.5),("1353",0.5,2.2),("P3174",0,1.8),("P3175",0,1.8),("P3176",0,1.8)]),
("", "Salva e manda pra quem viaja com você", [("1347",0,2.6),("1344",15,2.6),("1282",15,2.7)]),
]
TITLE=["Pousada com","pensão completa","em Brumadinho"]
def dt(text,y,size,box=True,col="white"):
    f=f"{B}/t_{abs(hash(text+str(y)))}.txt"; open(f,"w",encoding="utf-8").write(text)
    b=":box=1:boxcolor=black@0.45:boxborderw=18" if box else ":shadowx=3:shadowy=3"
    return f"drawtext=fontfile={FONT}:textfile={f}:fontsize={size}:fontcolor={col}:x=(w-text_w)/2:y={y}{b}"
segs=[]; n=0
for bi,(tag,cap,clips) in enumerate(V):
    for ci,(k,ss,d) in enumerate(clips):
        n+=1; out=f"{B}/s{n:02d}.mp4"
        txt=[]
        if tag: txt.append(dt(tag,120,52,True,"yellow"))
        if bi==0:
            for i,l in enumerate(TITLE): txt.append(dt(l,300+i*110,88,False))
            txt.append(dt(cap,1560,56))
        elif bi==9:
            txt.append(dt("Hotel Fazenda Horizonte Belo",1420,54,False))
            txt.append(dt("Brumadinho - MG",1500,46,False))
            txt.append(dt(cap,1620,46))
        else: txt.append(dt(cap,1560,56))
        tx=",".join(txt)
        if k.startswith("P"):
            p=glob.glob(S+f"/raw3/*IMG_{k[1:]}.JPG")[0]
            fc=f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,{tx}[v]"
            cmd=["ffmpeg","-nostdin","-v","error","-y","-loop","1","-t",str(d),"-i",p,"-filter_complex",fc,"-map","[v]"]
        else:
            vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"
            if k=="1343": vf="scale=1620:2880,crop=1080:1920:270:0,fps=30"
            cmd=["ffmpeg","-nostdin","-v","error","-y","-ss",str(ss),"-t",str(d),"-i",src(k),"-vf",vf+","+tx]
        cmd+=["-an","-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p",out]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: print("ERRO",k,r.stderr[-300:]); sys.exit(1)
        segs.append(out)
open(B+"/list.txt","w").write("".join(f"file '{s}'\n" for s in segs))
print(len(segs),"segmentos")
