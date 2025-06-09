/**
 * Gestion de la navigation et du menu mobile
 */

document.addEventListener('DOMContentLoaded', function() {
    // Gestion du menu mobile
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Gestion du dropdown du compte utilisateur
    const accountDropdown = document.getElementById('accountDropdown');
    const accountMenu = document.getElementById('accountMenu');
    
    if (accountDropdown && accountMenu) {
        accountDropdown.addEventListener('click', function(e) {
            accountMenu.classList.toggle('hidden');
        });
        
        // Fermer le menu si on clique ailleurs
        document.addEventListener('click', function(e) {
            if (!accountDropdown.contains(e.target)) {
                accountMenu.classList.add('hidden');
            }
        });
    }
    
    // Gestion du changement de style de la navbar lors du défilement
    const navbar = document.getElementById('navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('nav-scrolled');
                navbar.classList.remove('py-4');
                navbar.classList.add('py-2');
            } else {
                navbar.classList.remove('nav-scrolled');
                navbar.classList.remove('py-2');
                navbar.classList.add('py-4');
            }
        });
    }
    
    // Gestion des liens de navigation avec smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                    
                    // Fermer le menu mobile après avoir cliqué
                    if (mobileMenu) {
                        mobileMenu.classList.add('hidden');
                    }
                }
            }
        });
    });
});
