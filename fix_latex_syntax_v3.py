import os
import re

def fix_latex_file(file_path):
    print(f"Fixing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix broken bold patterns like "}text\textbf{" which seems to be an "inside out" bolding
    # Pattern: words}bold_text\textbf{words
    # We want: words\textbf{bold_text}words
    # Example: "这些成本}真实存在\textbf{，但没有被价格捕获"
    # Becomes: "这些成本\textbf{真实存在}，但没有被价格捕获"
    content = re.sub(r'\}\s*([^\{\}]+?)\s*\\textbf\{', r'\\textbf{\1}', content)

    # 2. Fix mixed MD bold syntax: **text** -> \textbf{text}
    content = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', content)

    # 3. Fix broken \textbf{...} where it says extbf{...} 
    content = re.sub(r'(?<!\\)extbf\{', r'\\textbf{', content)

    # 4. Fix broken \rightarrow where it says ightarrow
    content = re.sub(r'(?<!\\)ightarrow', r'\\rightarrow', content)

    # 5. Break long paragraphs
    paragraphs = content.split('\n\n')
    new_paragraphs = []
    
    for p in paragraphs:
        # If the paragraph is very long (e.g. > 800 characters)
        # Avoid breaking latex environments or comments
        striped_p = p.strip()
        if len(p) > 800 and not striped_p.startswith('%') and not striped_p.startswith('\\begin') and not striped_p.startswith('\\item') and not striped_p.startswith('\\chapter') and not striped_p.startswith('\\section'):
            # Try to break at a sentence boundary near the middle
            # Look for Chinese punctuation followed by space or just end of phrase
            # Using lookbehind to keep the punctuation
            sentences = re.split(r'([。！？]”?)', p)
            # re.split with capturing group will include the separators in the list
            # We need to recombine them
            recombined = []
            for i in range(0, len(sentences)-1, 2):
                recombined.append(sentences[i] + sentences[i+1])
            if len(sentences) % 2 != 0:
                recombined.append(sentences[-1])
            
            if len(recombined) > 2:
                mid = len(recombined) // 2
                p1 = "".join(recombined[:mid]).strip()
                p2 = "".join(recombined[mid:]).strip()
                new_paragraphs.append(p1)
                new_paragraphs.append(p2)
            else:
                new_paragraphs.append(p)
        else:
            new_paragraphs.append(p)
            
    content = '\n\n'.join(new_paragraphs)

    # Final check for common mistakes like \textbf{text** -> \textbf{text}
    content = re.sub(r'\\textbf\{(.+?)\s*\*\*', r'\\textbf{\1}', content)

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

print("All fixes applied successfully.")
