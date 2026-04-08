import os
import re

def fix_latex_errors(filepath):
    print(f"Processing {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Safely replace the exact corrupted phrases.
    # We add the new ones we found.
    corrupted_phrases = [
        ("}非排他性\\textbf{", "\\textbf{非排他性}"),
        ("}非竞争性\\textbf{", "\\textbf{非竞争性}"),
        ("}价格机制完全失灵\\textbf{", "\\textbf{价格机制完全失灵}"),
        ("}打个比方\\textbf{", "\\textbf{打个比方}"),
        ("}非市场机制\\textbf{", "\\textbf{非市场机制}"),
        ("}占优策略\\textbf{", "\\textbf{占优策略}"),
        ("}个人理性导致集体非理性\\textbf{", "\\textbf{个人理性导致集体非理性}"),
        ("}使用收益归个人、过度使用的成本归集体\\textbf{", "\\textbf{使用收益归个人、过度使用的成本归集体}"),
        ("}你少捕别人多捕，你的损失就是别人的收益\\textbf{", "\\textbf{你少捕别人多捕，你的损失就是别人的收益}"),
        ("}共享资源需要外部权威来限制个体行为\\textbf{", "\\textbf{共享资源需要外部权威来限制个体行为}"),
        ("}用暂时的垄断权换取知识的创造\\textbf{", "\\textbf{用暂时的垄断权换取知识的创造}"),
        ("}社区治理\\textbf{", "\\textbf{社区治理}"),
        ("}供给者只有一个\\textbf{", "\\textbf{供给者只有一个}"),
        ("}通过控制供给来操纵价格\\textbf{", "\\textbf{通过控制供给来操纵价格}"),
        ("}市场不是万能的，它需要外部力量的制衡\\textbf{", "\\textbf{市场不是万能的，它需要外部力量的制衡}"),
        ("}传统方案是政府管制\\textbf{", "\\textbf{传统方案是政府管制}"),
        ("}第二家进入就是社会资源浪费\\textbf{", "\\textbf{第二家进入就是社会资源浪费}"),
        ("}网络效应\\textbf{", "\\textbf{网络效应}"),
        ("}没有数据就做不好，没有用户就没有数据\\textbf{", "\\textbf{没有数据就做不好，没有用户就没有数据}"),
        ("}社交网络锁定\\textbf{", "\\textbf{社交网络锁定}"),
        ("}信息权力\\textbf{", "\\textbf{信息权力}"),
        ("}什么算\"垄断\"？\\textbf{", "\\textbf{什么算\"垄断\"？}"),
        ("}效率vs公平\\textbf{", "\\textbf{效率vs公平}"),
        ("}部分消费者剩余变成了垄断利润，部分直接消失了\\textbf{", "\\textbf{部分消费者剩余变成了垄断利润，部分直接消失了}"),
        ("}政治权力\\textbf{", "\\textbf{政治权力}"),
        ("}价格不是可以随意拨动的旋钮——它是信息的载体，扭曲价格就是扭曲信息\\textbf{", "\\textbf{价格不是可以随意拨动的旋钮——它是信息的载体，扭曲价格就是扭曲信息}"),
        ("}长期它制造了它试图解决的问题\\textbf{", "\\textbf{长期它制造了它试图解决的问题}"),
        ("}一个讽刺的画面\\textbf{", "\\textbf{一个讽刺的画面}"),
        ("}没有下降\\textbf{", "\\textbf{没有下降}"),
        ("}\"通过什么机制保护副作用最小\"\\textbf{", "\\textbf{\"通过什么机制保护副作用最小\"}"),
        ("}信息不足\\textbf{", "\\textbf{信息不足}"),
        ("}寻租\\textbf{", "\\textbf{寻租}"),
        ("}官僚成本\\textbf{", "\\textbf{官僚成本}"),
        ("}政府干预的最佳角色不是取代市场，而是修复市场的缺陷，然后让市场自己跑\\textbf{", "\\textbf{政府干预的最佳角色不是取代市场，而是修复市场的缺陷，然后让市场自己跑}"),
        ("}一切可以用货币衡量\\textbf{", "\\textbf{一切可以用货币衡量}"),
        ("}非货币交换体系\\textbf{", "\\textbf{非货币交换体系}"),
        ("}社会规范、关系逻辑和互惠原则\\textbf{", "\\textbf{社会规范、关系逻辑和互惠原则}"),
        ("}这个债务没有明确的到期日和金额，但双方都记得\\textbf{", "\\textbf{这个债务没有明确的到期日和金额，但双方都记得}"),
        ("}未来的人情债务\\textbf{", "\\textbf{未来的人情债务}"),
        ("}信任是一种可量化的资源\\textbf{", "\\textbf{信任是一种可量化的资源}"),
        ("}交易成本\\textbf{", "\\textbf{交易成本}"),
        ("}封闭性\\textbf{", "\\textbf{封闭性}"),
        ("}经济润滑剂\\textbf{", "\\textbf{经济润滑剂}"),
        ("}社会排斥的工具\\textbf{", "\\textbf{社会排斥的工具}"),
        ("}经济是模因退化的产物", "\\textbf{经济是模因退化的产物}"),
        ("}政治**", "\\textbf{政治}")
    ]
    
    for bad_str, good_str in corrupted_phrases:
        if bad_str in content:
            content = content.replace(bad_str, good_str)
            print(f"Fixed string: {good_str}")
            
    # Also find any remaining cases dynamically, but strictly matching a format where it likely wouldn't be valid text.
    # Looking for a `}` that has NO corresponding `{` on the same line before it.
    lines = content.split('\n')
    for i in range(len(lines)):
        # Very simple fallback: if there is a "}text\textbf{", we check if '{' appeared before '}'.
        # If not, it's definitely an inverted tag.
        temp_line = lines[i]
        while True:
            match = re.search(r'\}\s*([^\{\}\\]{1,50}?)\\textbf\{', temp_line)
            if not match:
                break
            # Find the index of this '}':
            idx = temp_line.find(match.group(0))
            # Check if there is an unmatched '{' before it
            left_part = temp_line[:idx]
            if left_part.count('{') <= left_part.count('}'):
                # It's an inverted tag!
                bad_str = match.group(0)
                good_str = f"\\textbf{{{match.group(1).strip()}}}"
                temp_line = temp_line.replace(bad_str, good_str, 1)
                lines[i] = temp_line
                print(f"Dynamically fixed: {good_str}")
            else:
                # Break to avoid infinite loop if it's a valid pair (like }...{)
                break
    content = '\n'.join(lines)
            
    # 2. Fix markdown bold "**text**" -> "\textbf{text}"
    def md_bold_replacer(match):
        text = match.group(1).strip()
        return f"\\textbf{{{text}}}"
        
    content = re.sub(r'\*\*(.+?)\*\*', md_bold_replacer, content)

    # 3. Fix broken commands like "extbf{" -> "\textbf{" and "ightarrow" -> "\rightarrow"
    content = re.sub(r'(?<!\\)extbf\{', r'\\textbf{', content)
    content = re.sub(r'(?<!\\)ightarrow', r'\\rightarrow', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_chapter3(filepath):
    print(f"Cleaning duplicate logic blocks in {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # The absolute lines (1-indexed) of duplicate paragraphs to remove in chapter 3.
    lines_to_remove = {56, 57, 62, 63, 68, 69, 74, 75, 144, 145, 150, 151, 200, 201, 206, 207, 212, 213, 218, 219}
    
    new_lines = []
    for i, line in enumerate(lines):
        if (i + 1) not in lines_to_remove:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    base_dir_part3 = "/Users/chenglu/Desktop/写作/动机社会/part3_systematic_expansion"
    if os.path.exists(base_dir_part3):
        for f in os.listdir(base_dir_part3):
            if f.endswith(".tex"):
                filepath = os.path.join(base_dir_part3, f)
                fix_latex_errors(filepath)
                if 'chapter3_politics_power_structure.tex' in f:
                    clean_chapter3(filepath)

    base_dir_part2 = "/Users/chenglu/Desktop/写作/动机社会/part2_geological_determinism"
    if os.path.exists(base_dir_part2):
        for f in os.listdir(base_dir_part2):
            if f.endswith(".tex"):
                filepath = os.path.join(base_dir_part2, f)
                fix_latex_errors(filepath)

    print("Great! All fixes applied successfully.")
