# 自动化编辑：压缩 chapter1 段落5

import re, sys
from pathlib import Path

file = Path("part3_systematic_expansion/chapter1_economic_base.tex")
txt = file.read_text(encoding='utf-8')

# 目标段落标题
target_header = r'\textbf{段落5（why5：价格的边界——当退化无法完成）}：\\\\'
# 新内容（精简版，148 字）
new_body = '''不是所有模因选择都能退化为价格。你不会在婚礼上说"性价比最高"，也不会在投票站说"这票值500块"——某些选择拒绝金钱标尺。品牌（如苹果）展示模因→金钱→模因的闭环，但婚姻、信仰、政治等强模因领域无法压缩。更深问题：即使在价格有效的领域，信息分布也不均——下一节追踪信息差如何创造利润与市场失灵。'''

# 替换：找到标题后的内容直到下一个 \textbf{段落 或 \section
pattern = re.compile(
    re.escape(target_header) + r'(.*?)(?=\\textbf\{段落\d+|\\section\{|\\Z)',
    re.DOTALL
)
match = pattern.search(txt)
if not match:
    print("❌ 未找到段落5", file=sys.stderr)
    sys.exit(1)

old_body = match.group(1)
new_txt = txt[:match.start(1)] + new_body + txt[match.end(1):]

# 写回
file.write_text(new_txt, encoding='utf-8')
print("✅ 已压缩段落5: 原%d字 → 新%d字" % (len(old_body.strip()), len(new_body.strip())))