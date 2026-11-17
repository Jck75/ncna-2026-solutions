import glob
import os
import re
from html import unescape

def html_to_markdown(html_str):
    start = html_str.find('<div class="problembody">')
    if start == -1:
        return ""
    end = html_str.find('</article>', start)
    if end == -1:
        end = len(html_str)
    body = html_str[start:end]

    # Convert table headers
    body = re.sub(r'<h2>(.*?)</h2>', r'\n\n## \1\n\n', body)
    body = re.sub(r'<h3>(.*?)</h3>', r'\n\n### \1\n\n', body)
    body = re.sub(r'<p>(.*?)</p>', r'\n\n\1\n\n', body, flags=re.DOTALL)
    
    # Samples table handling
    # Convert <table class="sample"...> into markdown code blocks
    def sample_replace(match):
        table_html = match.group(0)
        # find all pre blocks
        pres = re.findall(r'<pre>([\s\S]*?)</pre>', table_html)
        res = []
        for i in range(0, len(pres), 2):
            idx = i // 2 + 1
            inp = unescape(pres[i]).strip()
            out = unescape(pres[i+1]).strip() if i+1 < len(pres) else ""
            res.append(f"\n### Sample Input {idx}\n```\n{inp}\n```\n### Sample Output {idx}\n```\n{out}\n```\n")
        return '\n'.join(res)

    body = re.sub(r'<table class="sample"[\s\S]*?</table>', sample_replace, body)

    body = re.sub(r'<pre>([\s\S]*?)</pre>', r'\n```\n\1\n```\n', body)
    body = re.sub(r'<tt>([\s\S]*?)</tt>', r'`\1`', body)
    body = re.sub(r'<code>([\s\S]*?)</code>', r'`\1`', body)

    # Convert tex2jax
    body = re.sub(r'<span class="tex2jax_process">\$([\s\S]*?)\$</span>', r'$\1$', body)
    body = re.sub(r'<span class="tex2jax_process">\\\[([\s\S]*?)\\\]</span>', r'$$\1$$', body)

    # Strip remaining tags
    body = re.sub(r'<[^>]+>', ' ', body)
    body = unescape(body)
    body = re.sub(r'[ \t]+', ' ', body)
    body = re.sub(r'\n[ \t]+', '\n', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip()

for f in sorted(glob.glob('/home/pc1/icpc_2026_questions/raw_problems/*.html')):
    base = os.path.splitext(os.path.basename(f))[0]
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    cleaned = html_to_markdown(content)
    out_path = f'/home/pc1/icpc_2026_questions/raw_problems/{base}.md'
    with open(out_path, 'w', encoding='utf-8') as fp:
        fp.write(cleaned)
    print(f'Processed {base}: length {len(cleaned)}')
