#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use File::Copy;

my $SRC_DIR = '/Users/diegorivero/.gemini/antigravity/scratch/ecuador-invest';
my $DST_DIR = '/Users/diegorivero/.gemini/antigravity/scratch/pilar-patrimonio';

# Force UTF-8 on standard outputs
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

print "Starting Perl migration process...\n";

# 1. Copy static assets (non-HTML)
opendir(my $dh, $SRC_DIR) or die "Cannot open directory $SRC_DIR: $!";
while (my $item = readdir($dh)) {
    next if $item =~ /^\./; # Skip . and ..
    my $src_path = "$SRC_DIR/$item";
    my $dst_path = "$DST_DIR/$item";
    
    next if -d $src_path; # Skip directories
    next if $item =~ /\.html$/; # Skip template HTMLs
    next if $item eq 'setup.py' or $item eq 'update_nav.py'; # Skip utility scripts
    
    copy($src_path, $dst_path) or die "Copy failed: $!";
    print "Copied asset: $item\n";
}
closedir($dh);

# 2. Perform brand replacements on style.css and main.js
sub replace_brand {
    my ($content) = @_;
    $content =~ s/Ecuador Invest/Pilar Patrimonio/g;
    $content =~ s/ECUADOR INVEST/PILAR PATRIMONIO/g;
    $content =~ s/ecuador-invest/pilar-patrimonio/g;
    $content =~ s/EcuadorInvest/PilarPatrimonio/g;
    return $content;
}

foreach my $item ('style.css', 'main.js') {
    my $path = "$DST_DIR/$item";
    open(my $fh, '<:encoding(UTF-8)', $path) or die "Cannot open $path: $!";
    local $/;
    my $content = <$fh>;
    close($fh);
    
    $content = replace_brand($content);
    
    open(my $out, '>:encoding(UTF-8)', $path) or die "Cannot open $path for writing: $!";
    print $out $content;
    close($out);
    print "Processed brand in $item\n";
}

# Define layouts and snippets with proper UTF-8 support
my $PILAR_LOGO = q|<a href="index.html" class="navbar-logo">
                <div class="pilar-monogram">
                    <div class="pilar-bar pilar-bar-1"></div>
                    <div class="pilar-bar pilar-bar-2"></div>
                    <div class="pilar-bar pilar-bar-3"></div>
                </div>
                <span class="logo-text">PILAR PATRIMONIO</span>
            </a>|;

my $PILAR_FOOTER_LOGO = q|<div class="footer-logo">
                    <div class="pilar-monogram">
                        <div class="pilar-bar pilar-bar-1"></div>
                        <div class="pilar-bar pilar-bar-2"></div>
                        <div class="pilar-bar pilar-bar-3"></div>
                    </div>
                    <span class="logo-text" style="font-size: 0.75rem;">PILAR PATRIMONIO</span>
                </div>|;

my $THREE_COUNTRY_FOOTER = q|<div class="footer-contact-grid">
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
            </div>|;

sub process_html {
    my ($content, $c_code, $c_name, $p_name, $m_name) = @_;
    
    # 1. Brand replacement
    $content = replace_brand($content);
    
    # 2. Map file links from Ecuador layout to Pilar Patrimonio layout
    $content =~ s/fondoia\.html/ia\.html/g;
    $content =~ s/fondo2026\.html/fw\.html/g;
    
    # 3. Replace navbar logo img with monogram logo
    $content =~ s|<a href="index\.html" class="navbar-logo"[^>]*>.*?</a>\s*(?=<div class="menu-toggle")|$PILAR_LOGO\n            |gs;
    
    # 4. Replace footer logo img with monogram logo
    $content =~ s|<div class="footer-logo"[^>]*>.*?</div>\s*(?=<div class="footer-links")|$PILAR_FOOTER_LOGO\n                |gs;
    
    # 5. Replace footer contact grid with the robust 3-country grid
    $content =~ s|<div class="footer-contact-grid"[^>]*>.*?</div>\s*(?=<div class="footer-bottom")|$THREE_COUNTRY_FOOTER\n            |gs;
    
    # 6. Re-standardize the dropdown navigation menu item labels (so they are in uppercase and cleanly updated)
    # The source files already have correct dropdown HTML. We just ensure "FONDO DE IA", etc. are correctly pointed.
    
    # 7. Select country code in dropdown forms
    if ($c_code) {
        # Remove selected from any option in select block
        $content =~ s/\s*selected//g;
        
        # Inject selected into correct option
        $content =~ s/value="\Q$c_code\E"/value="$c_code" selected/g;
    }
    
    # 8. Customize landing content if specified
    if ($c_name) {
        $content =~ s/desde Ecuador/desde $c_name/g;
        $content =~ s/desde el Ecuador/desde $c_name/g;
        $content =~ s/desarrollado desde Ecuador/desarrollado desde $c_name/g;
    }
    
    if ($p_name) {
        $content =~ s/plataforma VektorCap/plataforma $p_name/g;
        $content =~ s/Plataforma VektorCap/plataforma $p_name/g;
    }
    
    if ($m_name) {
        $content =~ s/vektorcap-mockup\.png/$m_name/g;
        if ($m_name eq 'phone-mockup.png' and $content !~ /logo-invest-cover/) {
            $content =~ s/class="phone-image">/class="phone-image"><div class="logo-invest-cover"><\/div>/g;
        }
    }
    
    return $content;
}

# 3. Process each page configuration
my @pages_to_generate = (
    # [dst_file, src_file, country_code, country_name, platform_name, mockup_name]
    ['index.html', 'index.html', '+56', undef, undef, undef],
    ['ia.html', 'fondoia.html', '+56', 'Chile', 'VektorCap', 'vektorcap-mockup.png'],
    ['ia2.html', 'fondoia.html', '+593', 'Ecuador', 'VektorCap', 'vektorcap-mockup.png'],
    ['ia3.html', 'fondoia.html', '+51', 'Perú', 'VektorCap', 'vektorcap-mockup.png'],
    ['ia4.html', 'fondoia.html', '+51', 'Perú', 'VektorCap', 'vektorcap-mockup.png'],
    ['fw.html', 'fondo2026.html', '+51', 'Perú', undef, undef],
    ['spacex.html', 'spacex.html', '+593', undef, 'VektorCap', 'vektorcap-mockup.png'],
    ['spacex2.html', 'spacex.html', '+51', 'Perú', 'VektorCap', 'vektorcap-mockup.png'],
    ['oro.html', 'oro.html', '+56', undef, undef, undef],
    ['plataforma.html', 'plataforma.html', '+56', undef, undef, undef],
    ['apertura.html', 'apertura.html', '+56', undef, undef, undef],
    ['contacto.html', 'contacto.html', '+56', undef, undef, undef],
    ['gracias.html', 'gracias.html', undef, undef, undef],
    ['politica-de-privacidad.html', 'politica-de-privacidad.html', undef, undef, undef],
    ['rocket-xray.html', 'rocket-xray.html', undef, undef, undef],
);

foreach my $page_ref (@pages_to_generate) {
    my ($dst_name, $src_name, $c_code, $c_name, $p_name, $m_name) = @$page_ref;
    my $src_file_path = "$SRC_DIR/$src_name";
    my $dst_file_path = "$DST_DIR/$dst_name";
    
    if (! -e $src_file_path) {
        print "Warning: Source layout $src_name not found! Skipping.\n";
        next;
    }
    
    open(my $fh, '<:encoding(UTF-8)', $src_file_path) or die "Cannot open $src_file_path: $!";
    local $/;
    my $content = <$fh>;
    close($fh);
    
    my $processed_content = process_html($content, $c_code, $c_name, $p_name, $m_name);
    
    open(my $out, '>:encoding(UTF-8)', $dst_file_path) or die "Cannot open $dst_file_path for writing: $!";
    print $out $processed_content;
    close($out);
    print "Generated page: $dst_name\n";
}

print "Migration completed successfully!\n";
