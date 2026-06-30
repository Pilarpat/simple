import os
import re

target_dir = '/Users/diegorivero/.gemini/antigravity/scratch/simple-invest'

# 1. Rename files
files_to_copy = {
    'fw.html': 'fondo-warren.html',
    'ia4.html': 'fondoia.html',
}

for src, dst in files_to_copy.items():
    src_path = os.path.join(target_dir, src)
    dst_path = os.path.join(target_dir, dst)
    if os.path.exists(src_path):
        os.system(f'cp {src_path} {dst_path}')

# Also create openai.html from ia4.html base
if os.path.exists(os.path.join(target_dir, 'ia4.html')):
    os.system(f'cp {os.path.join(target_dir, "ia4.html")} {os.path.join(target_dir, "openai.html")}')

# Also create oro.html from fw.html base to have a clean start
if os.path.exists(os.path.join(target_dir, 'fw.html')):
    os.system(f'cp {os.path.join(target_dir, "fw.html")} {os.path.join(target_dir, "oro.html")}')

# Delete old html files except the ones we want
keep_htmls = ['index.html', 'fondo-warren.html', 'fondoia.html', 'spacex.html', 'openai.html', 'oro.html']
for filename in os.listdir(target_dir):
    if filename.endswith('.html') and filename not in keep_htmls:
        os.remove(os.path.join(target_dir, filename))

# 2. Text Replacements
def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Brand replacements
    content = content.replace('Pilar Patrimonio', 'Simple Invest')
    content = content.replace('PILAR PATRIMONIO', 'SIMPLE INVEST')
    content = content.replace('pilar-patrimonio', 'simple-invest')

    # Footer replacement
    # We want to remove the footer-contact-grid and replace it with a centered Colombia one.
    footer_regex = re.compile(r'<div class="footer-contact-grid">.*?</div>\s*<div class="footer-bottom">', re.DOTALL)
    
    new_footer = """<div class="footer-contact-grid" style="grid-template-columns: 1fr; justify-items: center; max-width: 400px; margin: 0 auto;">
                <!-- Colombia -->
                <a href="tel:+573009231912" class="contact-card" style="width: 100%; max-width: 300px;">
                    <div class="contact-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                        </svg>
                    </div>
                    <div class="contact-country">🇨🇴 Colombia</div>
                    <div class="contact-number">+57 300 923 1912</div>
                </a>
            </div>
            <div class="footer-bottom">"""
    
    content = footer_regex.sub(new_footer, content)

    # Form Default Selection: Remove 'selected' from any option, add to Colombia (+57)
    content = content.replace('selected', '')
    content = content.replace('<option value="+57">🇨🇴 +57</option>', '<option value="+57" selected>🇨🇴 +57</option>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Apply to all HTML files and JS/CSS if needed
for filename in os.listdir(target_dir):
    filepath = os.path.join(target_dir, filename)
    if filename.endswith('.html') or filename == 'main.js':
        replace_in_file(filepath)

print("Migration completed.")
