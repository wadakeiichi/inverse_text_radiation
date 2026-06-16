# -*- coding: utf-8 -*-
"""Generate curve-based SVG figures in the house style (planck-map.svg 準拠)."""
import numpy as np, os

OUT = "/sessions/happy-nifty-brahmagupta/mnt/宇宙物理教科書/spectra-of-the-universe/images"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', 'Noto Sans JP', sans-serif"
SERIF = "Georgia, 'STIX Two Text', 'Times New Roman', serif"
INK="#0a1929"; BLUE="#1f4e79"; AMBER="#d4a017"; AMBERT="#9a7400"; ORANGE="#c25e00"
ROSE="#c43f6b"; ROSED="#8a1f3e"; TEAL="#2e7d8c"; GRAY="#5a6a7a"; LGRAY="#8a99a8"; GRID="#e3e9f0"

def head(w,h,title,subtitle,comment=""):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SANS}">\n'
      f'<!-- {comment} | Style matched to planck-map.svg | License: CC BY 4.0 -->\n'
      f'<rect width="{w}" height="{h}" fill="#fafbfc"/>\n'
      f'<text x="{w/2}" y="40" text-anchor="middle" font-size="23" font-weight="700" fill="{INK}" letter-spacing="0.06em">{title}</text>\n'
      f'<text x="{w/2}" y="66" text-anchor="middle" font-size="14" fill="{GRAY}">{subtitle}</text>\n')

def footer(w,h,lines):
    s=""; y=h-18*(len(lines))-6
    for i,t in enumerate(lines):
        sz = 12 if i < len(lines)-1 else 11
        col = GRAY if i < len(lines)-1 else LGRAY
        s+=f'<text x="{w/2}" y="{y+18*i+12}" text-anchor="middle" font-size="{sz}" fill="{col}">{t}</text>\n'
    return s

def path(xs,ys,color,width=2.5,dash=None,opacity=1):
    d="M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in zip(xs,ys))
    da=f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} opacity="{opacity}"/>\n'

def txt(x,y,s,size=12,color=GRAY,anchor="start",weight=None,style=None,family=None):
    w=f' font-weight="{weight}"' if weight else ""
    st=f' font-style="{style}"' if style else ""
    fm=f' font-family="{family}"' if family else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}"{w}{st}{fm}>{s}</text>\n'

def axes_box(x0,y0,x1,y1):
    # x0,y0 = bottom-left pixel; x1,y1 = top-right pixel
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{INK}" stroke-width="1.5"/>\n'
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{INK}" stroke-width="1.5"/>\n')

# ================= 1. UV catastrophe =================
def fig_uv():
    w,hh=900,560; px0,px1,py0,py1=110,820,460,110
    h=6.626e-27;c=2.998e10;k=1.381e-16;T=5800.
    lx0,lx1=13.0,15.8
    def B(nu): x=h*nu/(k*T); return 2*h*nu**3/c**2/(np.expm1(np.clip(x,1e-9,300)))
    def RJ(nu): return 2*nu**2/c**2*k*T
    def WI(nu): return 2*h*nu**3/c**2*np.exp(-h*nu/(k*T))
    ly0,ly1=-9.0,-2.5
    X=lambda lx:(lx-lx0)/(lx1-lx0)*(px1-px0)+px0
    Y=lambda ly:py0-(ly-ly0)/(ly1-ly0)*(py0-py1)
    lnu=np.linspace(lx0,lx1,300); nu=10**lnu
    s=head(w,hh,"紫外線破綻 ― 古典論と観測の食い違い",
           "T = 5800 K のプランク分布と Rayleigh–Jeans 則（両対数）",
           "UV catastrophe (Ch.9 §9.3; also Ch.2 §2.5, Ch.10)")
    # grid + ticks
    for gx in range(13,16):
        s+=f'<line x1="{X(gx)}" y1="{py0}" x2="{X(gx)}" y2="{py1}" stroke="{GRID}" stroke-width="1"/>\n'
        s+=txt(X(gx),py0+20,f"10<tspan font-size=\"9\" dy=\"-5\">{gx}</tspan>",12,GRAY,"middle")
    for gy in range(-9,-2):
        s+=f'<line x1="{px0}" y1="{Y(gy)}" x2="{px1}" y2="{Y(gy)}" stroke="{GRID}" stroke-width="1"/>\n'
        s+=txt(px0-10,Y(gy)+4,f"10<tspan font-size=\"9\" dy=\"-5\">{gy}</tspan>",11,GRAY,"end")
    # divergence shading: where RJ exceeds Planck by >x2 (high-freq side)
    mask=RJ(nu)>2*B(nu); lo=lnu[mask][0]
    s+=f'<rect x="{X(lo)}" y="{py1}" width="{px1-X(lo)}" height="{py0-py1}" fill="{ROSE}" fill-opacity="0.07"/>\n'
    # curves (clip to box)
    def lg(vals): return np.log10(np.maximum(vals,1e-30))
    yB=lg(B(nu)); kb=(yB>ly0+0.02)
    s+=path(X(lnu[kb]),Y(yB[kb]),BLUE,3)
    yRJ=lg(RJ(nu)); keep=(yRJ<ly1-1e-9)&(yRJ>ly0+0.02)
    s+=path(X(lnu[keep]),Y(yRJ[keep]),ROSE,2.2,dash="7,4")
    yW=lg(WI(nu)); kw=(yW>ly0+0.02)
    s+=path(X(lnu[kw]),Y(yW[kw]),AMBER,2,dash="2,3")
    # hν=kT guide
    nuc=np.log10(k*T/h)
    s+=f'<line x1="{X(nuc)}" y1="{py0}" x2="{X(nuc)}" y2="{py1}" stroke="{GRAY}" stroke-width="1.2" stroke-dasharray="4,4"/>\n'
    s+=txt(X(nuc),py1-8,"hν = kT",12,GRAY,"middle",style="italic",family=SERIF)
    # labels
    s+=txt(X(13.9),Y(-3.95),"観測されるプランク分布",13,BLUE,weight="700")
    s+=txt(X(15.0),Y(-3.2),"Rayleigh–Jeans（古典）∝ ν²",13,ROSE,weight="700")
    s+=txt(X(15.02),Y(-3.2)+18,"→ 積分すると発散（紫外線破綻）",11,ROSED)
    s+=txt(X(15.25),Y(-6.2),"Wien 近似",12,AMBERT,weight="600")
    s+=txt(X(13.15),Y(-6.7),"低振動数では古典と一致",11,GRAY)
    s+=axes_box(px0,py0,px1,py1)
    s+=txt((px0+px1)/2,py0+44,"振動数 ν [Hz]",13,INK,"middle")
    s+=f'<text x="34" y="{(py0+py1)/2}" text-anchor="middle" font-size="13" fill="{INK}" transform="rotate(-90 34 {(py0+py1)/2})">B<tspan font-size="10">ν</tspan> [erg s⁻¹ cm⁻² Hz⁻¹ sr⁻¹]</text>\n'
    s+=footer(w,hh,["高振動数側の指数減衰には h が必要 ― 等分配（各モード kT）の破れが鍵（第9章 §9.3・第10章）"])
    return s+"</svg>\n"

# ================= 2. quantum freeze-out =================
def fig_freeze():
    w,hh=900,540; px0,px1,py0,py1=110,820,440,110
    X=lambda x:px0+x/8.0*(px1-px0); Y=lambda y:py0-y/1.15*(py0-py1)
    x=np.linspace(1e-6,8,400); yq=x/np.expm1(x)
    s=head(w,hh,"高振動数モードの「凍結」",
           "量子化振動子 1 個の平均エネルギー（第7章 §7.2・第10章 §10.2）",
           "Mode freeze-out")
    for gx in range(0,9):
        s+=f'<line x1="{X(gx)}" y1="{py0}" x2="{X(gx)}" y2="{py1}" stroke="{GRID}" stroke-width="1"/>\n'
        s+=txt(X(gx),py0+20,str(gx),12,GRAY,"middle")
    for gy in [0.5,1.0]:
        s+=f'<line x1="{px0}" y1="{Y(gy)}" x2="{px1}" y2="{Y(gy)}" stroke="{GRID}" stroke-width="1"/>\n'
        s+=txt(px0-10,Y(gy)+4,str(gy),11,GRAY,"end")
    # freeze-out region
    s+=f'<rect x="{X(3)}" y="{py1}" width="{px1-X(3)}" height="{py0-py1}" fill="{AMBER}" fill-opacity="0.10"/>\n'
    s+=txt(X(5.5),Y(0.78),"凍結領域：hν ≫ kT",14,AMBERT,"middle",weight="700")
    s+=txt(X(5.5),Y(0.78)+20,"エネルギー単位 hν が大きすぎて熱が届かず、",11.5,GRAY,"middle")
    s+=txt(X(5.5),Y(0.78)+36,"平均エネルギーは e^(−hν/kT) で消える",11.5,GRAY,"middle")
    # classical line
    s+=path([X(0),X(8)],[Y(1),Y(1)],ROSE,2.2,dash="7,4")
    s+=txt(X(6.9),Y(1.0)-10,"古典（等分配）：⟨E⟩ = kT",12.5,ROSE,weight="700",anchor="middle")
    # quantum curve
    s+=path(X(x),Y(yq),BLUE,3)
    s+=txt(X(1.52),Y(0.52),"量子化振動子",13,BLUE,weight="700")
    s+=txt(X(1.52),Y(0.52)+18,"⟨E⟩ = hν / (e^(hν/kT) − 1)",12,BLUE,family=SERIF,style="italic")
    s+=txt(X(0.25),Y(1.06),"x ≪ 1 では古典と一致（RJ 側）",11,GRAY)
    s+=axes_box(px0,py0,px1,py1)
    s+=txt((px0+px1)/2,py0+44,"x = hν / kT",13,INK,"middle",family=SERIF,style="italic")
    s+=f'<text x="34" y="{(py0+py1)/2}" text-anchor="middle" font-size="13" fill="{INK}" transform="rotate(-90 34 {(py0+py1)/2})">⟨E⟩ / kT</text>\n'
    s+=footer(w,hh,["この凍結が紫外線破綻（第9章）を救い、観測される黒体スペクトルの指数減衰を生む"])
    return s+"</svg>\n"

# ================= 3. equivalent width =================
def fig_ew():
    w,hh=900,540; px0,px1,py0,py1=100,560,440,110
    X=lambda x:(x+6)/12*(px1-px0)+px0; Y=lambda y:py0-y/1.15*(py0-py1)
    x=np.linspace(-6,6,400); prof=1-0.8*np.exp(-(x/1.5)**2)
    W=0.8*1.5*np.sqrt(np.pi)  # ≈2.13
    s=head(w,hh,"等価幅 W の定義",
           "吸収線が連続光から引き抜いた光を、同じ面積の長方形で測る（第20章 §20.1）",
           "Equivalent width")
    # shaded absorbed area
    d="M "+" L ".join(f"{X(a):.1f} {Y(b):.1f}" for a,b in zip(x,prof))
    d+=f" L {X(6):.1f} {Y(1):.1f} L {X(-6):.1f} {Y(1):.1f} Z"
    s+=f'<path d="{d}" fill="{BLUE}" fill-opacity="0.15" stroke="none"/>\n'
    # equal-area rectangle
    s+=f'<rect x="{X(-W/2):.1f}" y="{Y(1):.1f}" width="{X(W/2)-X(-W/2):.1f}" height="{Y(0)-Y(1):.1f}" fill="{ROSE}" fill-opacity="0.13" stroke="{ROSE}" stroke-width="1.5" stroke-dasharray="5,4"/>\n'
    # continuum
    s+=path([X(-6),X(6)],[Y(1),Y(1)],GRAY,1.5,dash="6,4")
    s+=txt(X(-5.7),Y(1)-8,"連続光（基準レベル）",12,GRAY)
    # profile
    s+=path(X(x),Y(prof),BLUE,3)
    s+=txt(X(2.6),Y(0.62),"吸収線の輪郭",13,BLUE,weight="700")
    s+=txt(X(-5.0),Y(0.42),"青い面積",12,BLUE,weight="600")
    s+=txt(X(-5.0),Y(0.42)+16,"= 吸われた光の総量",11,GRAY)
    s+=f'<line x1="{X(-3.4)}" y1="{Y(0.47)}" x2="{X(-1.3)}" y2="{Y(0.62)}" stroke="{BLUE}" stroke-width="1" stroke-dasharray="3,3"/>\n'
    # W double arrow
    yW=Y(0)-12
    s+=f'<line x1="{X(-W/2)}" y1="{yW}" x2="{X(W/2)}" y2="{yW}" stroke="{ROSE}" stroke-width="1.8"/>\n'
    for xx in (X(-W/2),X(W/2)):
        s+=f'<line x1="{xx}" y1="{yW-5}" x2="{xx}" y2="{yW+5}" stroke="{ROSE}" stroke-width="1.8"/>\n'
    s+=txt((X(-W/2)+X(W/2))/2,yW-9,"等価幅 W",13,ROSE,"middle",weight="700")
    s+=txt(X(0),Y(0)+34,"赤い長方形（深さ 1 × 幅 W）の面積 ＝ 青い面積",12,ROSED,"middle")
    s+=axes_box(px0,py0,px1,py1)
    s+=txt((px0+px1)/2,py0+52,"波長 λ",13,INK,"middle")
    s+=f'<text x="36" y="{(py0+py1)/2}" text-anchor="middle" font-size="13" fill="{INK}" transform="rotate(-90 36 {(py0+py1)/2})">規格化した強度（連続光 = 1）</text>\n'
    # right notes panel
    s+=f'<rect x="600" y="130" width="270" height="280" rx="10" fill="#ffffff" stroke="#d8e2ec" stroke-width="1.5"/>\n'
    s+=txt(735,160,"なぜ等価幅を使うか",14,INK,"middle",weight="700")
    # W = ∫ (Ic − Iλ)/Ic dλ  with true subscripts (absolutely positioned)
    s+=f'<g font-family="{SERIF}" font-style="italic" fill="{INK}">\n'
    for gx,gy,gs,gt in [(640,196,15,"W"),(658,195,13,"="),(674,198,19,"∫"),(686,196,15,"("),(694,196,15,"I"),(702,201,10,"c"),(714,196,15,"−"),(730,196,15,"I"),(738,201,10,"λ"),(746,196,15,")"),(756,196,15,"/"),(766,196,15,"I"),(774,201,10,"c"),(786,196,15,"dλ")]:
        s+=f'<text x="{gx}" y="{gy}" font-size="{gs}">{gt}</text>\n'
    s+="</g>\n"
    notes=[("・線形（profile）の詳細によらない積分量",224),
           ("・分光器の分解能が足りなくても測れる",250),
           ("・浅く広い線と深く狭い線が",276),
           ("　同じ W になりうる点には注意",294),
           ("・W → 柱密度 N の換算が成長曲線",322),
           ("　（curve of growth・§20.6）",340)]
    for t,yy in notes: s+=txt(614,yy,t,12,GRAY)
    s+=footer(w,hh,["観測される吸収線の最も基本的な観測量。第23章の組成決定はここから始まる"])
    return s+"</svg>\n"

# ================= 4. Voigt profile =================
def fig_voigt():
    w,hh=900,560
    # Voigt via convolution on fine grid
    xx=np.linspace(-40,40,16001); dx=xx[1]-xx[0]
    a=0.4
    G=np.exp(-xx**2)/np.sqrt(np.pi)
    L=(a/np.pi)/(xx**2+a**2)
    V=np.convolve(G,L,mode="same")*dx
    def interp(xq,f): return np.interp(xq,xx,f)
    s=head(w,hh,"Voigt 線形 ― コアは Gaussian、翼は Lorentzian",
           "Doppler（Gaussian）と減衰（Lorentzian）の畳み込み（第22章 §22.4、a = γ/2Δν_D = 0.4）",
           "Voigt profile, linear & log panels")
    # ---- left panel: linear ----
    px0,px1,py0,py1=90,430,440,120
    X=lambda v:(v+5)/10*(px1-px0)+px0; Y=lambda v:py0-v/0.88*(py0-py1)
    xq=np.linspace(-5,5,300)
    s+=txt((px0+px1)/2,108,"線形スケール",13,INK,"middle",weight="700")
    for gx in [-4,-2,0,2,4]:
        s+=txt(X(gx),py0+18,str(gx),11,GRAY,"middle")
    s+=path(X(xq),Y(interp(xq,G)),BLUE,2.2,dash="6,4")
    s+=path(X(xq),Y(interp(xq,L)),ROSE,2.2,dash="2,3")
    s+=path(X(xq),Y(interp(xq,V)),INK,3)
    s+=axes_box(px0,py0,px1,py1)
    s+=txt((px0+px1)/2,py0+42,"x = (ν − ν₀) / Δν_D",12.5,INK,"middle",family=SERIF,style="italic")
    s+=txt(X(-1.85),Y(0.40),"Gaussian",12,BLUE,"middle",weight="700")
    s+=txt(X(1.6),Y(0.27),"Voigt",13,INK,weight="700")
    s+=txt(X(-3.4),Y(0.13),"Lorentzian",12,ROSE,"middle",weight="700")
    s+=txt(X(0.45),Y(0.83),"← Lorentz の鋭いピーク",10.5,ROSE)
    # ---- right panel: log ----
    qx0,qx1,qy0,qy1=510,860,440,120
    lY=lambda v:qy0-(np.log10(np.maximum(v,1e-7))+6)/6.3*(qy0-qy1)
    qX=lambda v:v/10*(qx1-qx0)+qx0
    xq2=np.linspace(0,10,400)
    s+=txt((qx0+qx1)/2,108,"対数スケール（片側）",13,INK,"middle",weight="700")
    for gx in [0,2,4,6,8,10]:
        s+=txt(qX(gx),qy0+18,str(gx),11,GRAY,"middle")
    for gy in range(-6,1,2):
        s+=f'<line x1="{qx0}" y1="{lY(10.0**gy)}" x2="{qx1}" y2="{lY(10.0**gy)}" stroke="{GRID}" stroke-width="1"/>\n'
        s+=txt(qx0-8,lY(10.0**gy)+4,f"10<tspan font-size=\"8\" dy=\"-4\">{gy}</tspan>",10.5,GRAY,"end")
    # regions
    s+=f'<rect x="{qX(0)}" y="{qy1}" width="{qX(3)-qX(0)}" height="{qy0-qy1}" fill="{BLUE}" fill-opacity="0.07"/>\n'
    s+=f'<rect x="{qX(4)}" y="{qy1}" width="{qX(10)-qX(4)}" height="{qy0-qy1}" fill="{ROSE}" fill-opacity="0.07"/>\n'
    s+=txt(qX(1.5),qy1+22,"コア：Doppler 支配",11.5,BLUE,"middle",weight="700")
    s+=txt(qX(1.5),qy1+38,"→ 温度・乱流",10.5,GRAY,"middle")
    s+=txt(qX(7),qy1+22,"翼：Lorentz 支配 ∝ 1/x²",11.5,ROSED,"middle",weight="700")
    s+=txt(qX(7),qy1+38,"→ 密度・圧力（減衰幅）",10.5,GRAY,"middle")
    gv=interp(xq2,G); gm=gv>2e-6
    s+=path(qX(xq2[gm]),lY(gv[gm]),BLUE,2.2,dash="6,4")
    s+=path(qX(xq2),lY(interp(xq2,L)),ROSE,2.2,dash="2,3")
    s+=path(qX(xq2),lY(interp(xq2,V)),INK,3)
    s+=axes_box(qx0,qy0,qx1,qy1)
    s+=txt((qx0+qx1)/2,qy0+42,"x = (ν − ν₀) / Δν_D",12.5,INK,"middle",family=SERIF,style="italic")
    s+=footer(w,hh,["コアと翼を同時にフィットすると、温度（Doppler 幅）と密度（減衰幅）が独立に決まる ― §22.4 の「問い」"])
    return s+"</svg>\n"

for name,fn in [("uv-catastrophe.svg",fig_uv),("quantum-freeze-out.svg",fig_freeze),
                ("equivalent-width.svg",fig_ew),("voigt-profile.svg",fig_voigt)]:
    with open(os.path.join(OUT,name),"w") as f: f.write(fn())
    print("wrote",name)
