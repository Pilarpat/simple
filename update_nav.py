import glob
import re

new_nav = """            <ul class="nav-menu">
                <li class="nav-item"><a href="index.html" class="nav-link">INICIO</a></li>
                <li class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle">INVERSIÓN ▾</a>
                    <ul class="dropdown-menu">
                        <li><a href="fondoia.html" class="dropdown-item">FONDO DE IA</a></li>
                        <li><a href="fondo2026.html" class="dropdown-item">FONDO BERKSHIRE</a></li>
                        <li><a href="spacex.html" class="dropdown-item">IPO SPACEX</a></li>
                    </ul>
                </li>
                <li class="nav-item"><a href="#servicios" class="nav-link">SERVICIOS</a></li>
                <li class="nav-item"><a href="apertura.html" class="nav-link">APERTURA</a></li>
                <li class="nav-item"><a href="#contacto" class="nav-link">CONTACTO</a></li>
            </ul>"""

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace from <ul class="nav-menu"> to the corresponding </ul>
    # Use a regex that matches <ul class="nav-menu">...</ul> non-greedy
    pattern = r'<ul class="nav-menu">.*?</ul>'
    
    new_content = re.sub(pattern, new_nav, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

