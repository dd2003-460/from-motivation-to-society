import os
import re

def fix_latex_file(file_path):
    print(f"Fixing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix mixed MD bold syntax: **text** -> \textbf{text}
    # Handling cases like ** text ** and **text**
    # We use a non-greedy match to avoid matching across long spans
    content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', content)

    # 2. Fix broken \textbf{...} where it says extbf{...}
    # This often happens if the \ was missing
    content = re.sub(r'extbf\{', r'\\textbf{', content)

    # 3. Fix broken \rightarrow where it says ightarrow
    content = re.sub(r'ightarrow', r'\\rightarrow', content)

    # 4. Fix stray closing braces } that often appear before \textbf or other commands
    # These often look like: } \textbf{ or } 文本 \textbf{
    # We'll look for } followed by a space and a command, where the } isn't obviously closing anything
    # This is tricky, but the user's files seem to have a specific pattern of broken braces.
    # From what I saw:
    # "...这些成本}真实存在\textbf{..."
    # We can try to match '} ' if it's preceded by non-matching patterns or just common words
    # Let's target specific cases seen.
    content = re.sub(r'\}\s*真实存在', r' 真实存在', content)
    content = re.sub(r'\}\s*纯粹的', r' 纯粹的', content)
    content = re.sub(r'\}但现实中', r' 但现实中', content)
    content = re.sub(r'\}就像', r' 就像', content)
    content = re.sub(r'\}说明价格不是', r' 说明价格不是', content)
    
    # 5. Break long paragraphs
    # A paragraph is roughly defined by text between blank lines.
    # In Chinese text, sentences end with 。！？
    # We will try to find a natural break point in very long paragraphs.
    
    paragraphs = content.split('\n\n')
    new_paragraphs = []
    
    for p in paragraphs:
        # If the paragraph is very long (e.g. > 1000 characters)
        if len(p) > 800 and not p.strip().startswith('%') and not p.strip().startswith('\\begin') and not p.strip().startswith('\\item'):
            # Try to break at a sentence boundary near the middle
            sentences = re.split(r'(?<=[。！？])', p)
            mid = len(sentences) // 2
            if len(sentences) > 4:
                # Divide into two or three
                p1 = "".join(sentences[:mid])
                p2 = "".join(sentences[mid:])
                new_paragraphs.append(p1)
                new_paragraphs.append(p2)
            else:
                new_paragraphs.append(p)
        else:
            new_paragraphs.append(p)
            
    content = '\n\n'.join(new_paragraphs)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Target files
files = [
    '/Users/chenglu/Desktop/写作/动机社会/part2_geological_determinism/chapter1_materialist_historical_view.tex',
    '/Users/chenglu/Desktop/写作/动机社会/part2_geological_determinism/chapter2_survival_strategy_divergence.tex',
    '/Users/chenglu/Desktop/写作/动机社会/part3_systematic_expansion/chapter1_economic_base.tex',
    '/Users/chenglu/Desktop/写作/动机社会/part3_systematic_expansion/chapter2_culture_folk_institutions.tex',
    '/Users/chenglu/Desktop/写作/动机社会/part3_systematic_expansion/chapter3_politics_power_structure.tex',
    '/Users/chenglu/Desktop/写作/动机社会/part3_systematic_expansion/chapter4_law_institutional_form.tex'
]

for f in files:
    if os.path.exists(f):
        fix_latex_file(f)
    else:
        print(f"File {f} not found.")

print("All fixes applied.")
