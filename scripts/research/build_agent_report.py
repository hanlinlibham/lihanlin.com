"""Build the static, offline research journal. Requires Python Markdown.

The browser export is deliberately separate: the PDF is checked before publishing.
"""
from pathlib import Path
import html
import json
import re
import markdown

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research/agent-evolution-202611'
DEST = ROOT / 'public/research/agent-evolution/report'
sources = json.loads((SOURCE / 'sources.json').read_text())
source_map = {x['id']: x for x in sources}
E = html.escape

# Every diagram is an explanatory model, not a screenshot or a measured chart.
figures = {
 'centers': ('五种工作中心', ['Muse｜个人与目标','Grok Bot｜角色与流程','Claude Tag｜频道与线程','Super-agent｜授权任务','AbleWork｜研究与知识'], '五条路径并列存在；工作中心影响委托、状态和交付，不表示能力排名。', 'map'),
 'muse': ('个人目标如何继续推进', ['表达目标','保留约束','准备与执行','检查变化','回看与调整'], '用户的目标与约束贯穿过程；涉及重要外部后果时另行检查权限。依据 M1、M2 简化。', 'flow'),
 'grok': ('角色分开，账户内环境共享', ['研究 Bot','写作 Bot','流程 Bot','共享文件','浏览器与登录'], '上方是不同角色，下方是同一用户共享环境；角色记忆与环境访问是不同关系。依据 G1。', 'shared'),
 'tag': ('在原讨论中委托与交付', ['频道提出问题','线程保留上下文','获准工具执行','成果回到线程'], '团队在共同可见的位置接续工作；执行范围由配置与授权约束。依据 C1—C3 简化。', 'flow'),
 'superagent': ('事件进入持续任务', ['来源事件','准入与评估','授权任务','派工执行','回到原渠道'], '已有任务可接收相关上下文；新工作需要授权判断。依据 D2、D3 简化，不展示全部分支。', 'flow'),
 'proactivity': ('把主动性拆成具体动作', ['发现变化','判断关联','准备结果','选择通知','外部行动'], '每一步都有独立条件；准备可以积极，通知可以克制，外部行动仍需明确授权。作者分析。', 'stairs'),
 'memory': ('不同记忆需要不同更新方法', ['个人偏好｜用户纠正','流程方法｜版本修订','任务状态｜操作回执','领域知识｜证据更新'], '对象不同，正确性与失效方式不同；召回只是其中一步。作者分析。', 'map'),
 'authority': ('权限随工作路径反复检查', ['谁委托','读取什么','修改什么','分享给谁','以后还能否使用'], '相关性不授予权限；读取、执行、发布与后续消费分别检查。作者分析。', 'flow'),
 'quality': ('检查靠近它能控制的后果', ['材料输入','候选质量','正式写入','发布范围','后续有效性'], '格式、来源、语义、写入与可见性是不同检查，不由一个成功标记替代。作者建议。', 'flow'),
 'combination': ('一种可能的组合，而非已建成的互联', ['个人目标','可复用流程','团队讨论','持续任务','领域知识'], '跨形态交接携带成果、版本、来源、权限和责任。此图为作者提出的组合模型。', 'map'),
 'ableloop': ('AbleWork 当前日常路径', ['发布研究成果','核对身份与版本','生成或复用梗概','保存卡片与回执','后续检索与问答'], '消费前继续核对来源版本和读权；当前默认是梗概导航，非全量完整编译。依据 A1。', 'flow'),
 'reuse': ('跨作者复用的已观察路径', ['作者 A 发布 v2','生成对应梗概','作者 B 提出新问题','来源记录包含 v2'], '脱敏运行样本：证明新版成果进入另一人的任务输入，不证明答案已获用户接受。依据 A1。', 'flow'),
 'compile': ('历史完整编译的工作路径', ['材料与旧知识','比较形成候选','预检与重新比较','内核正式提交','宿主发布与再读取'], '候选、正式提交与发布分别有记录；历史验证不能代替当前默认运行状态。依据 A1。', 'flow'),
 'autowiki': ('编译语义与应用边界分工', ['模型｜提出候选','AutoWiki｜比较与校验','内核｜正式提交','AbleWork｜身份与材料','宿主｜权限与发布'], '上方为编译路径，下方为宿主责任；图为职责简化，具体接线以部署为准。依据 A1、A4。', 'shared'),
 'pulse': ('关注以后，后台准备结果', ['明确个人订阅','周期检查事实','比较当日水位','按需组织卡片','保存后回来阅读'], '同日水位未变可跳过模型和重写；产物保存与用户采用分开统计。依据 A2。', 'flow'),
 'commons': ('个人候选到公共知识的边界', ['个人知识与方法','候选池｜已观察','审核采纳｜待补实例','公共母本','用户只读消费'], '消费只读与候选上行已确认；候选到正式公共数据的采纳回执未观察到。依据 A3。', 'boundary'),
 'scenario': ('持续研究委托中的责任交接', ['关注目标','整理证据','团队判断','修订成果','后续问题'], '情境推演：口径分歧与重要结论变化需要明确裁定，不能只按时间覆盖。', 'flow'),
 'withdraw': ('来源变化应影响派生结果', ['来源更新或撤回','定位派生对象','重新检查读权','修订或标记结果','恢复任务再核对'], '情境推演与建议；不表示所有影响传播均已实现。历史合法交付按具体政策处理。', 'flow'),
 'portable': ('让成果离开一次对话仍可使用', ['稳定成果','作者与来源','明确版本','适用范围','其他人或 Agent'], '可携带对象不等于公开对象；迁移与复用仍受授权约束。作者推断。', 'flow'),
 'roadmap': ('按证据扩大责任', ['完成真实任务','能纠正和恢复','可重复的方法','持续职责','跨人知识复用'], '建议建设顺序，无日期承诺；每一步以真实结果和异常路径验证后再扩大范围。', 'stairs'),
}

def diagram(key, number):
    title, nodes, caption, kind = figures[key]
    ink, accent, purple = '#20352e', '#b95129', '#75609b'
    width, height = 720, (200 if kind in ('shared','map') else 168)
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="fig-title-{number} fig-desc-{number}">', f'<title id="fig-title-{number}">{E(title)}</title><desc id="fig-desc-{number}">{E(" → ".join(nodes)+"。"+caption)}</desc>', f'<defs><marker id="arrow-{number}" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="none" stroke="{accent}"/></marker></defs>']
    def line(x1,y1,x2,y2,dashed=False):
        dash_attr = 'stroke-dasharray="5 4"' if dashed else ''
        lines.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{accent}" stroke-width="1.5" {dash_attr} marker-end="url(#arrow-{number})"/>')
    def box(x,y,w,h,text,index,fill='#f2eee6',dash=False):
        dash_attr = 'stroke-dasharray="5 4"' if dash else ''
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{purple if dash else "#c8cbbf"}" {dash_attr}/>')
        label=text.split('｜')
        lines.append(f'<text x="{x+12}" y="{y+19}" font-size="10" fill="{accent}" font-family="sans-serif">{index:02d}</text>')
        if len(label)==2:
            lines.append(f'<text x="{x+w/2}" y="{y+h/2+1}" text-anchor="middle" font-size="15" font-weight="600" fill="{ink}">{E(label[0])}</text><text x="{x+w/2}" y="{y+h/2+24}" text-anchor="middle" font-size="13" fill="{purple}">{E(label[1])}</text>')
        else:
            # Deliberate two-line wrapping for long Chinese labels.
            cut=8 if len(text)>9 else 99
            a,b=text[:cut],text[cut:]
            lines.append(f'<text x="{x+w/2}" y="{y+h/2+(0 if b else 8)}" text-anchor="middle" font-size="14" font-weight="600" fill="{ink}">{E(a)}</text>')
            if b: lines.append(f'<text x="{x+w/2}" y="{y+h/2+22}" text-anchor="middle" font-size="14" fill="{ink}">{E(b)}</text>')
    if kind=='shared':
        lines.append('<rect x="5" y="105" width="710" height="88" rx="8" fill="#e7ece3"/>')
        for i,t in enumerate(nodes[:3]):
            x=17+i*240;box(x,8,205,75,t,i+1);line(x+102,84,x+102,112)
        for i,t in enumerate(nodes[3:]): box(80+i*310,117,250,62,t,i+4,fill='#f6f3ed')
    elif kind=='map':
        n=len(nodes);w=(700-(n-1)*10)/n
        lines.append(f'<path d="M20 155 H700" stroke="{accent}" stroke-width="1"/>')
        for i,t in enumerate(nodes):
            x=10+i*(w+10);box(x,15,w,105,t,i+1);line(x+w/2,121,x+w/2,155)
        lines.append(f'<text x="360" y="185" text-anchor="middle" font-size="14" fill="{ink}">共同问题：怎样让工作接续，结果可用，边界清楚</text>')
    else:
        n=len(nodes);w=(700-(n-1)*21)/n
        for i,t in enumerate(nodes):
            x=10+i*(w+21);y=18+i*9 if kind=='stairs' else 28
            box(x,y,w,80,t,i+1,fill='#eee9f2' if kind=='boundary' and i==2 else '#f2eee6',dash=kind=='boundary' and i in (2,3))
            if i<n-1: line(x+w,y+40,x+w+20,y+40+(9 if kind=='stairs' else 0),kind=='boundary' and i in (1,2))
        lines.append(f'<text x="12" y="151" font-size="11" fill="{purple}">{"虚线：正式采纳路径待补真实实例" if kind=="boundary" else "机制示意 · 箭头表示工作关系，不表示耗时或性能"}</text>')
    lines.append('</svg>')
    mobile=''.join(f'<li>{E(n.replace("｜"," · "))}</li>' for n in nodes)
    return f'<figure id="figure-{number}"><div class="figure-kicker">FIG. {number:02d} / 机制示意</div><h3>{E(title)}</h3>{"".join(lines)}<ol class="figure-mobile">{mobile}</ol><figcaption>{E(caption)}</figcaption></figure>'

def bibliography(group):
    rows=[]
    for item in sources:
        if item['group']!=group:continue
        title=f'<a href="{E(item["url"])}">{E(item["title"])}</a>' if item.get('url') else E(item['title'])
        if item.get('extra'):title+=f' · <a href="{E(item["extra"])}">Authorization</a>'
        rows.append(f'<li id="source-{item["id"]}"><span class="source-id">{item["id"]}</span><div>{title}<small>{E(item["note"])}</small></div></li>')
    return '<ol class="bibliography">'+''.join(rows)+'</ol>'

raw='\n'.join((SOURCE/p).read_text() for p in ('manuscript.md','part-2.md','part-3.md'))
chunks=[s for s in re.split(r'(?=^## \d+ \|)',raw,flags=re.M) if s.strip()]
chunks.sort(key=lambda x:int(re.match(r'## (\d+)',x).group(1)))
assert len(chunks)==60
folios=[];toc=[];part='';fig_count=0; stats=[]
for chunk in chunks:
    first,body=chunk.split('\n',1)
    num,title=first.removeprefix('## ').split(' | ',1)
    newpart=re.search(r'<!-- PART: (.*?) -->',body).group(1)
    if newpart!=part:
        toc.append(f'<li><a href="#p{num}"><span>{num}</span>{E(newpart)}</a></li>');part=newpart
    body=re.sub(r'<!-- PART: .*? -->','',body)
    for key in re.findall(r'\[FIG:(.*?)\]',body):
        fig_count+=1;body=body.replace(f'[FIG:{key}]',diagram(key,fig_count))
    body=re.sub(r'<!-- BIB:(.*?) -->',lambda m:bibliography(m[1]),body)
    def cite(m):
        item=source_map[m[1]]
        return f'<a class="cite" href="#source-{m[1]}" aria-label="来源 {m[1]}：{E(item["title"])}">[{m[1]}]</a>'
    body=re.sub(r'\[([MGCDA]\d+)\]',cite,body)
    rendered=markdown.markdown(body,extensions=['tables','sane_lists'])
    rendered=re.sub(r'(<table>.*?</table>)',r'<div class="table-scroll">\1</div>',rendered,flags=re.S)
    folios.append(f'<section class="folio {"references" if int(num)>58 else ""}" id="p{num}" aria-labelledby="title-{num}"><header class="folio-top"><span>{E(part)}</span><span>智能体的演进 / 2026.11</span></header><div class="folio-content"><div class="section-number">{num}</div><h2 id="title-{num}">{E(title)}</h2>{rendered}</div><footer class="folio-foot"><span>Hanlin Li · 研究专刊</span><a href="#contents">目录</a><span>{num} / 60</span></footer></section>')
    stats.append({'folio':int(num),'title':title,'han_chars':len(re.findall(r'[\u4e00-\u9fff]',chunk))})

css=(SOURCE/'report.css').read_text()
toc_rows=[]
for section in stats:
    n=section['folio']
    toc_rows.append(f'<li><a href="#p{n:02d}"><span class="toc-number">{n:02d}</span><span>{E(section["title"])}</span><span class="toc-page">{n+3}</span></a></li>')
print_toc=''.join(f'<section class="print-contents"><header>智能体的演进 / 2026.11</header><h2>目录 <small>{i+1} / 2</small></h2><p>左侧为正文节号，右侧为 PDF 页码；电子版可点击标题跳转。</p><ol>{"".join(toc_rows[i*30:(i+1)*30])}</ol><footer>Hanlin Li · 研究专刊 <span>{i+2}</span></footer></section>' for i in range(2))
screen_toc=f'<details class="full-contents"><summary>展开完整目录 · 60 节正文与来源</summary><ol>{"".join(toc_rows)}</ol></details>'
cover_svg='''<svg class="cover-art" viewBox="0 0 700 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="个人、角色、团队、任务和知识五条路径围绕持续责任相互连接，表示并存与结合，不表示排名"><g fill="none" stroke-width="1.3"><path d="M65 65 C180 65 210 180 350 115 S530 40 635 65" stroke="#f2b28f"/><path d="M65 180 C190 180 220 65 350 115 S520 220 635 180" stroke="#a5bca6"/><path d="M350 20 V215" stroke="#b1a6d1"/><ellipse cx="350" cy="115" rx="194" ry="82" stroke="#67786e" stroke-dasharray="5 7"/></g><g fill="#f4f0e7" font-family="sans-serif" font-size="16"><circle cx="65" cy="65" r="8" fill="#f2b28f"/><text x="86" y="57">个人 / Muse</text><circle cx="635" cy="65" r="8" fill="#b1a6d1"/><text x="610" y="48" text-anchor="end">角色 / Grok Bot</text><circle cx="65" cy="180" r="8" fill="#a5bca6"/><text x="86" y="207">团队 / Claude Tag</text><circle cx="635" cy="180" r="8" fill="#f2b28f"/><text x="610" y="208" text-anchor="end">任务 / Super-agent</text><circle cx="350" cy="20" r="6" fill="#b1a6d1"/><text x="366" y="30">知识 / AbleWork</text><rect x="281" y="89" width="138" height="52" rx="26" fill="#f4f0e7"/><text x="350" y="121" text-anchor="middle" fill="#20352e" font-size="19" font-weight="600">持续责任</text></g></svg>'''
cover=f'''<section class="cover" id="top"><div class="cover-top"><a href="https://lihanlin.com/">HANLIN LI / RESEARCH</a><span>2026 · NOVEMBER</span></div><div class="cover-main"><p class="eyebrow">AGENT EVOLUTION · 研究专刊</p><h1>智能体的<br><em>演进</em></h1><p class="cover-sub">从个人代理、数字角色与团队协作，<br>到持续任务和可复用的研究知识。</p>{cover_svg}<p class="cover-thesis">当智能体开始持续工作，差异不只在于能做多少事，<br>还在于责任怎样接续、边界怎样保持、成果怎样留下。</p><div class="cover-meta"><span>作者 / Hanlin Li</span><span>资料截至 / 2026.11.01</span><span>编成 / 2026.11.02</span></div></div><div class="cover-bottom"><span>面向 Agent 产品负责人、技术负责人和架构师</span><span>完整报告 · 含机制示意与来源</span></div></section>'''
nav=f'''<aside class="reader-nav" id="contents"><a class="brand" href="#top">智能体的演进<span>2026 / 11</span></a><nav aria-label="报告目录"><ol>{''.join(toc)}</ol></nav><div class="reader-actions"><a href="https://lihanlin.com/research/agent-evolution/">研究主页 ↗</a><a href="#top">回到封面 ↑</a></div><p class="nav-note">官方说明 · 作者运行核查<br>分析与情境推演分别标记</p></aside>'''
out=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="五种智能体形态的出发点、目标、机制比较与未来影响，以及 AbleWork 当前应用的完整长篇研究。"><title>智能体的演进｜2026 年 11 月研究专刊 · Hanlin Li</title><style>{css}</style></head><body><a class="skip-link" href="#p01">跳到正文</a>{nav}<main>{cover}{screen_toc}{print_toc}{''.join(folios)}<div class="screen-end"><p>本文资料截至 2026 年 11 月 1 日。未来判断与情境推演均已在正文标注。</p><a href="#top">回到封面 ↑</a> · <a href="https://lihanlin.com/research/agent-evolution/">返回研究主页</a></div></main></body></html>'''
DEST.mkdir(parents=True,exist_ok=True)
(DEST/'index.html').write_text(out)
cover_asset='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 830" role="img" aria-labelledby="title desc"><title id="title">智能体的演进</title><desc id="desc">2026 年 11 月研究专刊，从个人代理到持续任务与研究知识，Hanlin Li。</desc><rect width="620" height="830" fill="#20352e"/><path d="M45 66 H575 M45 758 H575" stroke="#6c7d6d"/><g fill="#f4f0e7" font-family="sans-serif"><text x="45" y="43" font-size="12" letter-spacing="2">HANLIN LI / RESEARCH</text><text x="575" y="43" text-anchor="end" font-size="12">2026.11</text><text x="45" y="124" fill="#efb18d" font-size="13" letter-spacing="2">AGENT EVOLUTION</text><text x="45" y="238" font-size="76" font-family="serif">智能体的</text><text x="45" y="332" font-size="80" fill="#efb18d" font-family="serif">演进</text><text x="45" y="395" font-size="21">从个人代理、数字角色与团队协作</text><text x="45" y="431" font-size="21">到持续任务和可复用的研究知识</text></g><g fill="none" stroke-width="1.6"><path d="M60 530 C200 530 225 650 310 592 S460 510 560 530" stroke="#efb18d"/><path d="M60 660 C190 660 220 535 310 592 S470 700 560 660" stroke="#a4bca5"/><path d="M310 485 V707" stroke="#b0a0d0"/><ellipse cx="310" cy="592" rx="175" ry="90" stroke="#697d6b" stroke-dasharray="5 8"/></g><g fill="#f4f0e7" font-family="sans-serif" font-size="13"><text x="60" y="515">个人</text><text x="535" y="515">角色</text><text x="60" y="688">团队</text><text x="535" y="688">任务</text><text x="325" y="493">知识</text><rect x="247" y="571" width="126" height="42" rx="21" fill="#f4f0e7"/><text x="310" y="599" text-anchor="middle" fill="#20352e" font-size="18">持续责任</text><text x="45" y="793" font-size="12">五种形态 · 机制对照 · AbleWork 应用</text><text x="575" y="793" font-size="12" text-anchor="end">研究专刊</text></g></svg>'''
(DEST.parent/'cover.svg').write_text(cover_asset)
(SOURCE/'content-stats.json').write_text(json.dumps({'folios':len(chunks),'mechanism_figures':fig_count,'han_chars':len(re.findall(r'[\u4e00-\u9fff]',raw)),'sections':stats},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'folios':len(chunks),'figures':fig_count,'html_bytes':len(out.encode()),'output':str(DEST/'index.html')}))
