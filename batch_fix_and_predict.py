#!/usr/bin/env python3
import re
from pathlib import Path

# Extend predictions for chapter1/2/4 topics (based on extracted math)
# Use same structure as before, add missing topic predictions

EXTENDED_PREDICTIONS = {
    # Chapter1 Economic Base
    "从观点到价格——退化如何发生": "你可能会想：价格不就是供需决定的吗？\\ 但关键洞见：价格是观点的退化——从'我觉得好'压缩成'我愿意付多少钱'，这个过程丢失了什么？",
    "共识如何从分散的主观判断中涌现": "你可能会问：价格共识怎么来的？\\ 像鸟群 flocking：没有中央指挥，每只鸟看周围几只，整体涌现有序——价格是经济的自组织涌现。",
    "信息不对称如何扭曲价格共识": "你可能会觉得：信息不对称可以靠检测解决。\\ 但检测有成本，且不是所有信息都能检测（如'调校手感'）——信息壁垒是市场固有的摩擦。",
    "价格作为近似解——够用但不完美": "你可能质疑：价格不完美为什么还要用？\\ 因为'够用'——在信息有限时提供最低成本决策，哈耶克称为'价格信号'，协调陌生人行动。",
    "价格的边界——当退化无法完成": "你可能会想：所有东西都能定价吗？\\ 不能。爱、尊严、信仰——这些不能被压缩成价格，否则人性就消失了。价格有边界。",
    "需求强度的时空依赖性": "你可能会问：需求为什么是函数？\\ 同一瓶水：超市2块，沙漠50块，演唱会门口100块——你的需求强度随情境剧烈变化。",
    "情绪如何放大需求波动": "你可能会觉得：恐慌性抢购是理性的？\\ 不是——情绪放大需求，让超市货架瞬间清空，和实际物资短缺无关，是模因在驱动。",
    "收入、偏好和技术如何重塑长期需求": "你可能没想到：需求长期变化有三驱动力：收入（变富买更好的）、偏好（价值观迁移）、技术（新品类诞生）。",
    "需求预测的不可能性——混沌与反身性": "你可能会问：为什么需求预测总错？\\ 因为预测本身改变行为（索罗斯反身性）——预测房价涨→大家冲去买→房价真的涨→预测实现，但泡沫终将破裂。",
    "从需求波动到供给策略——卖家如何利用波动": "你可能会想：卖家只能被动应对需求吗？\\ 不，动态定价就是主动利用波动：航空、酒店、网约车，根据需求实时调价。",
    "自然稀缺vs人为稀缺——谁在控制供给？": "你可能会质疑：稀缺都是天然的吗？\\ 不。De Beers 控制钻石供给制造稀缺——人为稀缺是权力在定价中的体现。",
    "供给冲击——口罩价格的48小时暴涨": "你可能会问：供给 shock 有多快？\\ 极快。2020年2月，口罩从0.5元涨到10元只用了48小时——供给中断时价格弹性消失。",
    "垄断定价——为什么垄断者能赚超额利润": "你可能会想：垄断不就是定价高吗？\\ 关键是：垄断者赚的不是'正常利润'，而是**超额利润**——利用控制权把价格设在竞争价格之上。",
    "从供给博弈到信息不对称——价格无法反映的盲区": "你可能会问：供给博弈和之前的信息不对称有什么关系？\\ 垄断控制供给时，价格反映的是权力而非价值——信息不对称在两方都存在。",
    "负外部性——价格之外的隐藏成本": "你可能会觉得：市场交易是你情我愿，有什么问题？\\ 问题在于成本转嫁：你买快时尚衣服，价格没包含 Bangladeshi 工人的血汗和环境破坏——负外部性。",
    "正外部性——价格低估的社会收益": "你可能会问：正外部性有什么例子？\\ 教育：你上大学私人收益是高薪，社会收益是低犯罪率、高 civic participation——价格低估后者。",
    "科斯定理——为什么谈判不能解决一切": "你可能会想：科斯定理说产权清晰就能解决外部性，不是吗？\\ 理论上是的，但交易成本太高——现实中谈判很难达成，尤其涉及大量受损者。",
    "碳排放交易——把外部性内部化的尝试": "你可能会质疑：碳市场真的有效吗？\\ 它是尝试：总量控制下交易排放权，让污染者付费。但初期配额太松，价格低，约束力有限。",
    "法律无法解决的问题": "你可能会想：法律不是万能的吗？\\ 不是。法律能禁止行为但不能创造价值；能保护权利但不能分配资源；能裁决冲突但不能消除冲突根源。",
    "法律与文化：规则的两种形态": "你可能会问：法律和文化都是规则，区别在哪？\\ 法律靠强制力（警察/法院），文化靠认同（社会压力）。最佳状态是两者互补，而非互斥。",
    "法律与经济：正义vs效率": "你可能会觉得：追求正义会影响效率？\\ 是的。严格环保法保护环境但可能降低 GDP。社会需要在正义和效率之间权衡。",
    "法律与技术：规则追赶创新": "你可能会担忧：技术太快法律跟不上？\\ 确实。AI、基因编辑、加密货币——法律永远在追赶，而且经常在问题爆发后才立法。",
    "章尾——社会秩序的四层架构": "你可能在问：文化、经济、政治、法律，哪个更重要？\\ 不是哪个，而是它们如何嵌套：文化最软但最普遍，法律最硬但最窄。四层协同才是稳定社会。"
}

def get_topic(line):
    m = re.search(r'\\subsubsection\*\{段落\d+：(.+)\}', line)
    if m: return m.group(1)
    m2 = re.search(r'\\textbf\{段落\d+（why\d+：([^）]+））\}', line)
    if m2: return m2.group(1)
    return None

def generate_prediction(topic):
    if topic in EXTENDED_PREDICTIONS:
        return EXTENDED_PREDICTIONS[topic]
    # fallback
    return f"你可能会想：'{topic}'这个观点是否太绝对？\\ 但理解背后的机制后，它会成为你分析问题的有力工具。"

def process_chapter(filepath):
    lines = open(filepath, 'r', encoding='utf-8').readlines()
    new_lines = []
    i = 0
    added = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect \textbf{段落N...}
        if r'\textbf{段落' in line:
            # Convert this line to \subsubsection*
            topic = get_topic(line)
            if not topic:
                # Could not parse, keep as is
                new_lines.append(line)
                i += 1
                continue
            new_header = f'\t\\subsubsection*{{段落{topic.split("：")[0]}：{topic.split("：",1)[1]}}}' if '：' in topic else line
            new_lines.append(new_header)
            i += 1
            
            # Collect paragraph content
            para_lines = []
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip().startswith(r'\textbf{段落') or nxt.strip().startswith(r'\subsubsection') or nxt.strip().startswith(r'\section') or nxt.strip().startswith(r'\subsection') or nxt.strip().startswith('% ---'):
                    break
                para_lines.append(nxt)
                i += 1
            
            if para_lines:
                first = para_lines[0]
                # Find first sentence boundary
                insert_idx = -1
                for pat in ['。\\', '）：\\', ')\\']:
                    pos = first.find(pat)
                    if pos != -1:
                        insert_idx = pos + len(pat.rstrip(' '))
                        break
                if insert_idx == -1:
                    pos = first.find('。')
                    if pos != -1:
                        insert_idx = pos + 1
                
                if insert_idx != -1:
                    before = first[:insert_idx]
                    after = first[insert_idx:]
                    new_lines.append(before)
                    new_lines.append('\n')
                    new_lines.append('\t\\begin{tcolorbox}[colback=yellow!5, title=\\textit{读者行为预测}]\n')
                    new_lines.append(f'\t\t{generate_prediction(topic)}\n')
                    new_lines.append('\t\\end{tcolorbox}\n')
                    new_lines.append('\n')
                    if after.strip():
                        new_lines.append(after)
                    new_lines.extend(para_lines[1:])
                    added += 1
                    continue
                else:
                    new_lines.append(first)
                    new_lines.append('\n')
                    new_lines.append('\t\\begin{tcolorbox}[colback=yellow!5, title=\\textit{读者行为预测}]\n')
                    new_lines.append(f'\t\t{generate_prediction(topic)}\n')
                    new_lines.append('\t\\end{tcolorbox}\n')
                    new_lines.append('\n')
                    new_lines.extend(para_lines[1:])
                    added += 1
                    continue
        else:
            new_lines.append(line)
            i += 1
    
    # Also fix malformed \begin{motivation>} and \extbf{ if any remain
    content = ''.join(new_lines)
    content = content.replace(r'\begin{motivation>', r'\begin{motivation}')
    content = content.replace(r'\end{motivation>', r'\end{motivation}')
    content = content.replace(r'\extbf{', r'\textbf{')
    
    Path(filepath).write_text(content, encoding='utf-8')
    return added

if __name__ == '__main__':
    base = Path('part3_systematic_expansion')
    chapters = ['chapter1_economic_base.tex', 'chapter2_culture_folk_institutions.tex', 'chapter4_law_institutional_form.tex']
    total = 0
    for ch in chapters:
        target = base / ch
        if target.exists():
            count = process_chapter(target)
            print(f"{ch}: added {count} prediction boxes")
            total += count
        else:
            print(f"{ch}: file not found")
    print(f"Total predictions added: {total}")
