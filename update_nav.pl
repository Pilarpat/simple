#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

my $new_nav = q|            <ul class="nav-menu">
                <li class="nav-item"><a href="index.html" class="nav-link">INICIO</a></li>
                <li class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle">INVERSIÓN ▾</a>
                    <ul class="dropdown-menu">
                        <li><a href="fondoia.html" class="dropdown-item">FONDO DE IA</a></li>
                        <li><a href="fondo2026.html" class="dropdown-item">FONDO BERKSHIRE</a></li>
                        <li><a href="spacex.html" class="dropdown-item">IPO SPACEX</a></li>
                        <li><a href="oro.html" class="dropdown-item">ORO</a></li>
                    </ul>
                </li>
                <li class="nav-item"><a href="plataforma.html" class="nav-link">PLATAFORMA</a></li>
                <li class="nav-item"><a href="index.html#servicios" class="nav-link">SERVICIOS</a></li>
                <li class="nav-item"><a href="apertura.html" class="nav-link">APERTURA</a></li>
                <li class="nav-item"><a href="contacto.html" class="nav-link">CONTACTO</a></li>
            </ul>|;

opendir(my $dh, ".") or die "Cannot open directory: $!";
while (my $file = readdir($dh)) {
    next unless $file =~ /\.html$/;
    next if $file eq "plataforma.html"; # Keep active class in plataforma.html!
    
    open(my $fh, "<:encoding(UTF-8)", $file) or die "Cannot open $file: $!";
    local $/;
    my $content = <$fh>;
    close($fh);
    
    my $updated = $content;
    $updated =~ s|<ul class="nav-menu">.*?</ul>|$new_nav|gs;
    
    if ($updated ne $content) {
        open(my $out, ">:encoding(UTF-8)", $file) or die "Cannot open $file for writing: $!";
        print $out $updated;
        close($out);
        print "Updated navbar in $file\n";
    }
}
closedir($dh);
print "Navbar updates completed in ecuador-invest!\n";
