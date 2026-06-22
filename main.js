document.addEventListener('DOMContentLoaded', () => {

    /* 0. MOBILE HAMBURGER MENU */
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
        });

        // Close menu on link click
        navMenu.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.classList.remove('no-scroll');
            });
        });
    }

    /* 1. CONTACT FORM AJAX POST */
    /*
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            // Restored after FormSubmit activation
        });
    }
    */

    /* 2. INTERSECTION OBSERVER FOR FADE-IN */
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const fadeInObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // observer.unobserve(entry.target); // Optional: uncomment to animate only once
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in-up');
    fadeElements.forEach(el => {
        fadeInObserver.observe(el);
    });

    /* 2. NAVBAR SCROLL EFFECT */
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    /* 3. FAQ ACCORDION LOGIC */
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            const content = header.nextElementSibling;

            // Close other open items (optional, for accordion style)
            document.querySelectorAll('.accordion-item').forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.accordion-content').style.maxHeight = null;
                }
            });

            // Toggle current item
            if (item.classList.contains('active')) {
                item.classList.remove('active');
                content.style.maxHeight = null;
            } else {
                item.classList.add('active');
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });

    /* 4. NUMBER COUNTER (For Performance Section) */
    const numberObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                if (!target.classList.contains('counted')) {
                    target.classList.add('counted');
                    target.classList.add('counted');
                    const targetVal = parseFloat(target.dataset.target || 72.5);
                    const useComma = target.dataset.comma === "true";
                    animateNumber(target, targetVal, 2000, 1, useComma);
                }
            }
        });
    }, { threshold: 0.5 });

    function animateNumber(element, finalValue, duration, decimals, useComma = false) {
        let startTime = null;
        const step = (currentTime) => {
            if (!startTime) startTime = currentTime;
            const progress = Math.min((currentTime - startTime) / duration, 1);

            const easeProgress = progress * (2 - progress);
            const currentVal = easeProgress * finalValue;

            if (useComma) {
                // Formatting large integers with Spanish locale (dots for thousands)
                element.childNodes[0].nodeValue = Math.floor(currentVal).toLocaleString('es-ES');
            } else {
                let formatted = currentVal.toFixed(decimals);
                element.childNodes[0].nodeValue = formatted;
            }

            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                if (useComma) {
                    element.childNodes[0].nodeValue = finalValue.toLocaleString('es-ES');
                } else {
                    element.childNodes[0].nodeValue = finalValue.toFixed(decimals);
                }
            }
        };
        window.requestAnimationFrame(step);
    }

    const largeNumber = document.querySelector('.large-number');
    if (largeNumber) {
        numberObserver.observe(largeNumber);
    }

    /* 5. PHONE PARALLAX ANIMATION (PREMIUM LERP) */
    const approachSection = document.getElementById('approach');
    const phoneParallaxTarget = document.querySelector('.phone-parallax-target');
    const phoneReflection = document.querySelector('.phone-reflection');

    if (approachSection && phoneParallaxTarget) {
        let currentScale = 0.9;
        let targetScale = 0.9;
        let currentY = 120;
        let targetY = 120;
        let currentRotate = 4;
        let targetRotate = 4;
        let currentReflectX = 200;
        let targetReflectX = 200;

        const lerp = (start, end, factor) => {
            return start + (end - start) * factor;
        };

        const updatePhoneParallax = () => {
            const rect = approachSection.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            if (rect.top <= windowHeight && rect.bottom >= 0) {
                // Progress from 0 (section entering viewport) to 1 (section fully in viewport/middle)
                const totalScroll = windowHeight + (rect.height / 2);
                let progress = (windowHeight - rect.top) / totalScroll;
                progress = Math.max(0, Math.min(1, progress));

                // Ease out sine
                const easeOut = Math.sin((progress * Math.PI) / 2);

                targetScale = 0.82 + (0.23 * easeOut); // 0.82 -> 1.05
                targetY = 250 - (280 * easeOut); // 250px -> -30px
                targetRotate = 8 - (12 * easeOut); // 8deg -> -4deg
                targetReflectX = 250 - (280 * easeOut); // 250% -> -30%
            }

            // Lerp towards target for that buttery smooth "premium" feel
            currentScale = lerp(currentScale, targetScale, 0.05);
            currentY = lerp(currentY, targetY, 0.05);
            currentRotate = lerp(currentRotate, targetRotate, 0.05);
            currentReflectX = lerp(currentReflectX, targetReflectX, 0.05);

            phoneParallaxTarget.style.transform = `translateY(${currentY}px) scale(${currentScale}) rotate(${currentRotate}deg)`;

            if (phoneReflection) {
                phoneReflection.style.backgroundPosition = `${currentReflectX}% ${currentReflectX}%`;
            }

            window.requestAnimationFrame(updatePhoneParallax);
        };

        // Start loop
        window.requestAnimationFrame(updatePhoneParallax);
    }

    /* 6. CIRCUIT LIGHTS ANIMATION */
    const circuitSection = document.getElementById('context');
    if (circuitSection) {
        const lightsContainer = document.createElement('div');
        lightsContainer.className = 'circuit-lights-wrapper';
        circuitSection.appendChild(lightsContainer);

        const colors = ['#00ffcc', '#ff00ff', '#0099ff', '#00ff66', '#ffcc00'];

        // Create 35 data packets
        for (let i = 0; i < 35; i++) {
            const light = document.createElement('div');

            const isHorizontal = Math.random() > 0.5;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const length = Math.random() * 40 + 20;
            const thickness = Math.random() * 1.5 + 0.5;
            const top = Math.random() * 35 + 65;
            const left = Math.random() * 100;
            const duration = Math.random() * 1.5 + 0.8;
            const delay = Math.random() * 5;
            const direction = Math.random() > 0.5 ? 1 : -1;

            light.style.position = 'absolute';
            light.style.background = color;
            light.style.boxShadow = `0 0 8px ${color}`;
            light.style.top = `${top}%`;
            light.style.left = `${left}%`;
            light.style.opacity = '0';
            light.style.mixBlendMode = 'color-dodge';
            light.style.zIndex = '0';
            light.style.borderRadius = '50px';

            if (isHorizontal) {
                light.style.width = `${length}px`;
                light.style.height = `${thickness}px`;
                light.style.setProperty('--tx', `${300 * direction}px`);
                light.style.animation = `shootHorizontal ${duration}s linear ${delay}s infinite`;
            } else {
                light.style.width = `${thickness}px`;
                light.style.height = `${length}px`;
                light.style.setProperty('--ty', `${300 * direction}px`);
                light.style.animation = `shootVertical ${duration}s linear ${delay}s infinite`;
            }

            lightsContainer.appendChild(light);
        }
    }

    /* 7. PERFORMANCE 2025 STAGGERED FADE & NUMBER ANIMATION */
    const staggerObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');

                const numElement = entry.target.querySelector('.perf-number');
                if (numElement && !numElement.classList.contains('counted')) {
                    numElement.classList.add('counted');
                    const targetVal = parseFloat(numElement.getAttribute('data-target'));
                    const useComma = numElement.getAttribute('data-comma') === 'true';
                    animateNumber(numElement, targetVal, 1600, 2, useComma);
                }

                staggerObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    const staggerElements = document.querySelectorAll('.stagger-fade');
    staggerElements.forEach((el, index) => {
        el.style.transitionDelay = `${(index % 8) * 0.15}s`;
        staggerObserver.observe(el);
    });

    /* 8. PERFORMANCE SLIDER PANEL CLONING & LOGIC */
    const perfSlider = document.getElementById('perfSlider');
    if (perfSlider) {
        const list2025 = document.querySelector('#panel-2025 .performance-list');
        const list2024 = document.getElementById('list-2024');
        if (list2025 && list2024) {
            const rowNodes = list2025.querySelectorAll('.perf-row');

            const target2024 = {
                'NVDA': { val: 170.90, sign: '+' },
                'AMD': { val: 18.06, sign: '-' },
                'MSFT': { val: 12.03, sign: '+' },
                'ARM': { val: 64.12, sign: '+' },
                'ORCL': { val: 58.15, sign: '+' },
                'TSLA': { val: 62.44, sign: '+' }
            };

            rowNodes.forEach(row => {
                const clone = row.cloneNode(true);
                clone.classList.remove('is-visible');

                const ticker = clone.querySelector('.perf-ticker').innerText.trim();
                const numberEl = clone.querySelector('.perf-number');
                const prefixEl = clone.querySelector('.perf-prefix');
                const valContainer = clone.querySelector('.perf-value');

                // The updateCount logic was erroneously inserted here and has been removed.
                if (target2024[ticker] && numberEl) {
                    numberEl.setAttribute('data-target', target2024[ticker].val);
                    numberEl.innerText = '0.00';
                    numberEl.classList.remove('counted');

                    if (target2024[ticker].sign === '+') {
                        valContainer.classList.remove('negative');
                        valContainer.classList.add('positive');
                        prefixEl.innerText = '+';
                    } else {
                        valContainer.classList.remove('positive');
                        valContainer.classList.add('negative');
                        prefixEl.innerText = '-';
                    }
                }

                list2024.appendChild(clone);
                // Also add to observer since it's a new element
                staggerObserver.observe(clone);
            });

            // Re-apply staggered delay explicitly for cloned elements
            Array.from(list2024.children).forEach((el, idx) => {
                el.style.transitionDelay = `${(idx % 8) * 0.15}s`;
            });
        }

        const prevArrow = document.querySelector('.prev-arrow');
        const nextArrow = document.querySelector('.next-arrow');
        const rightFade = document.querySelector('.slider-right-fade');

        const updateSliderUI = () => {
            if (perfSlider.scrollLeft <= 50) {
                prevArrow.classList.add('hide');
                nextArrow.classList.remove('hide');
                rightFade.classList.remove('hide');
            } else {
                prevArrow.classList.remove('hide');
                nextArrow.classList.add('hide');
                rightFade.classList.add('hide');
            }
        };

        perfSlider.addEventListener('scroll', updateSliderUI, { passive: true });

        nextArrow.addEventListener('click', () => {
            perfSlider.scrollBy({ left: window.innerWidth, behavior: 'smooth' });
        });

        prevArrow.addEventListener('click', () => {
            perfSlider.scrollBy({ left: -window.innerWidth, behavior: 'smooth' });
        });
    }
});
