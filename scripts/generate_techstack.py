import urllib.request
import re
import os

os.makedirs('assets/icons', exist_ok=True)

icons_list = [
    # Row 1 (8)
    "dotnet", "cs", "angular", "ts", "js", "azure", "docker", "jenkins",
    # Row 2 (8)
    "grafana", "prometheus", "mssql", "git", "github", "vscode", "visualstudio", "cpp"
]

icon_svgs = {}

for name in icons_list:
    if name == "mssql":
        with open('assets/icons/mssql.svg', 'r', encoding='utf-8') as f:
            content = f.read()
            # extract inner graphic
            inner = re.search(r'<svg[^>]*>(.*)</svg>', content, re.DOTALL).group(1)
            icon_svgs[name] = inner.strip()
    else:
        url = f"https://skillicons.dev/icons?i={name}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(req).read().decode('utf-8')
            # Extract the nested svg or content
            match = re.search(r'<g transform="translate\(0, 0\)">\s*(<svg.*?</svg>)\s*</g>', raw, re.DOTALL)
            if match:
                icon_svgs[name] = match.group(1).strip()
            else:
                icon_svgs[name] = raw.strip()
            print(f"Loaded {name}")
        except Exception as e:
            print(f"Error loading {name}: {e}")

# Now build 8x2 grid SVG
# Each icon is 48x48, spacing is 6px.
ICON_SIZE = 48
GAP = 6
COLS = 8
ROWS = 2

WIDTH = COLS * ICON_SIZE + (COLS - 1) * GAP  # 426
HEIGHT = ROWS * ICON_SIZE + (ROWS - 1) * GAP # 102

def make_stack_svg(theme="dark"):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none">'
    ]
    for idx, name in enumerate(icons_list):
        r = idx // COLS
        c = idx % COLS
        x = c * (ICON_SIZE + GAP)
        y = r * (ICON_SIZE + GAP)
        inner = icon_svgs.get(name, "")
        
        # If the inner contains a full <svg viewBox="0 0 256 256">, embed it at (x, y) with 48x48
        if "<svg" in inner:
            # replace width and height on inner svg with 48
            inner_mod = re.sub(r'<svg[^>]*width="[^"]*"[^>]*height="[^"]*"', f'<svg width="{ICON_SIZE}" height="{ICON_SIZE}" x="{x}" y="{y}"', inner)
            if 'x="' not in inner_mod:
                inner_mod = inner_mod.replace('<svg', f'<svg x="{x}" y="{y}" width="{ICON_SIZE}" height="{ICON_SIZE}"', 1)
            parts.append(inner_mod)
        else:
            # mssql case: it has viewBox 0 0 256 256
            parts.append(f'<svg x="{x}" y="{y}" width="{ICON_SIZE}" height="{ICON_SIZE}" viewBox="0 0 256 256">{inner}</svg>')
            
    parts.append('</svg>')
    return '\n'.join(parts)

svg_dark = make_stack_svg("dark")
with open('assets/techstack-dark.svg', 'w', encoding='utf-8') as f:
    f.write(svg_dark)

svg_light = make_stack_svg("light")
with open('assets/techstack-light.svg', 'w', encoding='utf-8') as f:
    f.write(svg_light)

print("Generated assets/techstack-dark.svg and assets/techstack-light.svg successfully!")
