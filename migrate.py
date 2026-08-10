import os
import shutil
import re

SRC_DIR = '/Users/diegorivero/.gemini/antigravity/scratch/ecuador-invest'
DST_DIR = '/Users/diegorivero/.gemini/antigravity/scratch/pilar-patrimonio'

def main():
    print("Starting migration process...")
    
    # 1. Copy static assets (non-HTML)
    for item in os.listdir(SRC_DIR):
        src_path = os.path.join(SRC_DIR, item)
        dst_path = os.path.join(DST_DIR, item)
        
        if os.path.isdir(src_path):
            continue  # No subdirectories in source folder
        
        if item.endswith('.html') or item == 'setup.py' or item == 'update_nav.py':
            continue  # Skip HTML source templates and utility scripts
            
        # Copy file
        shutil.copy2(src_path, dst_path)
        print(f"Copied asset: {item}")
        
    # 2. Perform brand replacements on style.css and main.js
    def replace_brand(content):
        # Silent replacement: brand name, monogram text, folder paths
        content = content.replace('Ecuador Invest', 'Pilar Patrimonio')
        content = content.replace('ECUADOR INVEST', 'PILAR PATRIMONIO')
        content = content.replace('ecuador-invest', 'pilar-patrimonio')
        content = content.replace('EcuadorInvest', 'PilarPatrimonio')
        return content

    for item in ['style.css', 'main.js']:
        path = os.path.join(DST_DIR, item)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = replace_brand(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed brand in {item}")

    # Define reusable layouts and snippets
    PILAR_LOGO = """<a href="index.html" class="navbar-logo">
                <div class="pilar-monogram">
                    <div class="pilar-bar pilar-bar-1"></div>
                    <div class="pilar-bar pilar-bar-2"></div>
                    <div class="pilar-bar pilar-bar-3"></div>
                </div>
                <span class="logo-text">PILAR PATRIMONIO</span>
            </a>"""

    PILAR_FOOTER_LOGO = """<div class="footer-logo">
                    <div class="pilar-monogram">
                        <div class="pilar-bar pilar-bar-1"></div>
                        <div class="pilar-bar pilar-bar-2"></div>
                        <div class="pilar-bar pilar-bar-3"></div>
                    </div>
                    <span class="logo-text" style="font-size: 0.75rem;">PILAR PATRIMONIO</span>
                </div>"""

    THREE_COUNTRY_FOOTER = """<div class="footer-contact-grid">
                <!-- Chile -->
                <a href="tel:+56233849641" class="contact-card">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                        </svg>
                    </div>
                    <div class="contact-country">🇨🇱 Chile</div>
                    <div class="contact-number">+56 2 3384 9641</div>
                </a>
                <!-- Uruguay -->
                <a href="tel:+59893591326" class="contact-card">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                        </svg>
                    </div>
                    <div class="contact-country">🇺🇾 Uruguay</div>
                    <div class="contact-number">+598 93 591 326</div>
                </a>
                <!-- Ecuador -->
                <a href="tel:+59327085340" class="contact-card">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                        </svg>
                    </div>
                    <div class="contact-country">🇪🇨 Ecuador</div>
                    <div class="contact-number">+593 2 708 5340</div>
                </a>
            </div>"""

    PILAR_NAV = """<ul class="nav-menu">
                <li class="nav-item"><a href="index.html" class="nav-link">INICIO</a></li>
                <li class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle">INVERSIÓN ▾</a>
                    <ul class="dropdown-menu">
                        <li><a href="ia.html" class="dropdown-item">FONDO DE IA</a></li>
                        <li><a href="fw.html" class="dropdown-item">FONDO BERKSHIRE</a></li>
                        <li><a href="spacex.html" class="dropdown-item">IPO SPACEX</a></li>
                        <li><a href="oro.html" class="dropdown-item">ORO</a></li>
                    </ul>
                </li>
                <li class="nav-item"><a href="index.html#servicios" class="nav-link">SERVICIOS</a></li>
                <li class="nav-item"><a href="apertura.html" class="nav-link">APERTURA</a></li>
                <li class="nav-item"><a href="contacto.html" class="nav-link">CONTACTO</a></li>
            </ul>"""

    def process_html(content, country_code=None, country_name=None, platform_name=None, mockup_name=None):
        # 1. Brand replacement
        content = replace_brand(content)
        
        # 2. Map file links from Ecuador layout to Pilar Patrimonio layout
        content = content.replace('fondoia.html', 'ia.html')
        content = content.replace('fondo2026.html', 'fw.html')
        
        # 3. Replace navbar logo img with monogram logo
        logo_pattern = re.compile(r'<a href="index.html" class="navbar-logo"[^>]*>.*?</a>\s*(?=<div class="menu-toggle")', re.DOTALL)
        content = logo_pattern.sub(PILAR_LOGO + "\n            ", content)
        
        # 4. Replace footer logo img with monogram logo
        footer_logo_pattern = re.compile(r'<div class="footer-logo"[^>]*>.*?</div>\s*(?=<div class="footer-links")', re.DOTALL)
        content = footer_logo_pattern.sub(PILAR_FOOTER_LOGO + "\n                ", content)
        
        # 5. Replace footer contact grid with the robust 3-country grid
        footer_contact_pattern = re.compile(r'<div class="footer-contact-grid"[^>]*>.*?</div>\s*(?=<div class="footer-bottom")', re.DOTALL)
        content = footer_contact_pattern.sub(THREE_COUNTRY_FOOTER + "\n            ", content)
        
        # 6. Re-standardize the navigation menu (using lookahead to not stop at nested dropdown ul)
        nav_pattern = re.compile(r'<ul class="nav-menu">.*?</ul>\s*(?=<div class="menu-toggle"|</div>)', re.DOTALL)
        # Wait, in pilar website the menu is followed by </div> closing the navbar-container.
        # But actually, let's keep step 6 robust or skip replacing main nav-menu since the source already has correct html and it's simpler.
        # Let's just comment out or make it a pass, like in migrate.pl:
        # Actually, let's comment it out or keep it safe:
        # content = nav_pattern.sub(PILAR_NAV, content)
        # We can just skip standardizing the main navigation menu regex if the source already has it perfectly.
        # But wait, to be safe, let's just match to the end of the menu container.
        # Let's just not run it or comment it out so it matches migrate.pl.
        
        # 7. Select country code in dropdown forms
        if country_code:
            # Remove all selected flags
            content = content.replace('selected', '')
            # Inject selected into the correct option
            content = content.replace(f'value="{country_code}"', f'value="{country_code}" selected')

        # 8. Customize landing content if specified
        if country_name:
            content = content.replace('desde Ecuador', f'desde {country_name}')
            content = content.replace('desde el Ecuador', f'desde {country_name}')
            content = content.replace('desarrollado desde Ecuador', f'desarrollado desde {country_name}')
            
        if platform_name:
            # Swap VektorCap references in text for Azul or similar
            content = content.replace('plataforma VektorCap', f'plataforma {platform_name}')
            content = content.replace('Plataforma VektorCap', f'plataforma {platform_name}')
            
        if mockup_name:
            # Swap mockup images in HTML
            content = content.replace('vektorcap-mockup.png', mockup_name)
            # Add logo-invest-cover overlay to Azul phone mockup if it's there
            if mockup_name == 'phone-mockup.png' and 'logo-invest-cover' not in content:
                content = content.replace(
                    'class="phone-image">',
                    'class="phone-image"><div class="logo-invest-cover"></div>'
                )
                
        return content

    # 3. Process each page configuration
    pages_to_generate = [
        # (dst_file, src_file, country_code, country_name, platform_name, mockup_name)
        ('index.html', 'index.html', '+56', None, None, None),
        ('ia.html', 'fondoia.html', '+56', 'Chile', 'VektorCap', 'vektorcap-mockup.png'),
        ('ia2.html', 'fondoia.html', '+593', 'Ecuador', 'VektorCap', 'vektorcap-mockup.png'),
        ('ia3.html', 'fondoia.html', '+51', 'Perú', 'VektorCap', 'vektorcap-mockup.png'),
        ('ia4.html', 'fondoia.html', '+51', 'Perú', 'VektorCap', 'vektorcap-mockup.png'),
        ('fw.html', 'fondo2026.html', '+51', 'Perú', None, None),
        ('spacex.html', 'spacex.html', '+593', None, 'VektorCap', 'vektorcap-mockup.png'),
        ('spacex2.html', 'spacex.html', '+51', 'Perú', 'VektorCap', 'vektorcap-mockup.png'),
        ('oro.html', 'oro.html', '+56', None, None, None),
        ('plataforma.html', 'plataforma.html', '+56', None, None, None),
        ('apertura.html', 'apertura.html', '+56', None, None, None),
        ('contacto.html', 'contacto.html', '+56', None, None, None),
        ('gracias.html', 'gracias.html', None, None, None),
        ('politica-de-privacidad.html', 'politica-de-privacidad.html', None, None, None),
        ('rocket-xray.html', 'rocket-xray.html', None, None, None),
    ]

    for dst_name, src_name, c_code, c_name, p_name, m_name in pages_to_generate:
        src_file_path = os.path.join(SRC_DIR, src_name)
        dst_file_path = os.path.join(DST_DIR, dst_name)
        
        if not os.path.exists(src_file_path):
            print(f"Warning: Source layout {src_name} not found! Skipping.")
            continue
            
        with open(src_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        processed_content = process_html(content, c_code, c_name, p_name, m_name)
        
        with open(dst_file_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        print(f"Generated page: {dst_name}")

    print("Migration completed successfully!")

if __name__ == "__main__":
    main()
