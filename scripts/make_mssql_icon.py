import urllib.request
import re
import os

os.makedirs('assets/icons', exist_ok=True)
url = 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/microsoftsqlserver/microsoftsqlserver-original.svg'
content = urllib.request.urlopen(url).read().decode('utf-8')

# extract defs if any
defs_match = re.search(r'(<defs>.*?</defs>)', content, re.DOTALL)
defs = defs_match.group(1) if defs_match else ''

# extract paths
paths = re.findall(r'<path[^>]*>', content)
paths_str = '\n    '.join(paths)

wrapped_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" fill="none">
  <rect width="256" height="256" rx="60" fill="#242938"/>
  {defs}
  <g transform="translate(48, 48) scale(1.25)">
    {paths_str}
  </g>
</svg>
"""
with open('assets/icons/mssql.svg', 'w', encoding='utf-8') as f:
    f.write(wrapped_svg)
print('Wrote assets/icons/mssql.svg, size:', len(wrapped_svg))
