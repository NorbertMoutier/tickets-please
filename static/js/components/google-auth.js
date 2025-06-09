/**
 * Gestion de l'authentification Google via popup
 */

// Variables globales pour l'authentification
let authPopup = null;
let authInProgress = false;
let authTimeoutId = null;

/**
 * Ferme la popup d'authentification si elle est ouverte
 */
function closeAuthPopupIfOpen() {
    if (authPopup && !authPopup.closed) {
        authPopup.close();
    }
    
    if (authTimeoutId) {
        clearTimeout(authTimeoutId);
        authTimeoutId = null;
    }
    
    authPopup = null;
}

/**
 * Redirige vers la page de compte après connexion réussie
 */
function redirectToAccount() {
    window.location.href = '/account/';
}

/**
 * Ouvre la popup d'authentification Google
 * @param {string} url - L'URL d'authentification
 */
function openGoogleAuthPopup(url) {
    // Ne pas ouvrir plusieurs popups
    if (authInProgress) {
        console.log('Authentification déjà en cours, annulation');
        return;
    }
    
    // Fermer toute popup existante
    closeAuthPopupIfOpen();
    
    console.log('Ouverture de la popup d\'authentification Google');
    authInProgress = true;
    
    // Ouvrir la popup
    var width = 600;
    var height = 600;
    var left = (window.innerWidth - width) / 2;
    var top = (window.innerHeight - height) / 2;
    
    authPopup = window.open(
        url,
        'googleAuthPopup',
        'width=' + width + ',height=' + height + ',top=' + top + ',left=' + left + ',resizable=yes,scrollbars=yes,status=yes'
    );
    
    // Vérifier si la popup a bien été ouverte
    if (!authPopup || authPopup.closed) {
        console.error('Impossible d\'ouvrir la popup, les popups sont peut-être bloqués');
        authInProgress = false;
        return;
    }
    
    // Mettre en place un timeout de sécurité pour annuler l'authentification si elle prend trop de temps
    authTimeoutId = setTimeout(function() {
        console.log('Timeout d\'authentification atteint');
        if (authInProgress) {
            authInProgress = false;
            closeAuthPopupIfOpen();
            alert('L\'authentification a pris trop de temps. Veuillez réessayer.');
        }
    }, 120000); // 2 minutes
    
    // Vérifier régulièrement si la popup a été fermée manuellement
    var checkPopupInterval = setInterval(function() {
        if (authPopup && authPopup.closed) {
            clearInterval(checkPopupInterval);
            if (authInProgress) {
                console.log('Popup fermée manuellement');
                authInProgress = false;
                if (authTimeoutId) {
                    clearTimeout(authTimeoutId);
                    authTimeoutId = null;
                }
            }
        }
    }, 1000);
}

/**
 * Vérifie périodiquement l'état d'authentification
 */
function checkAuthStatus() {
    console.log('Vérification de l\'authentification...');
    
    fetch('/check-auth-status/')
        .then(response => response.json())
        .then(data => {
            console.log('État d\'authentification:', data);
            
            if (data.is_authenticated) {
                console.log('Utilisateur authentifié, redirection vers la page compte');
                window.location.href = '/account/';
            }
        })
        .catch(error => {
            console.error('Erreur de vérification:', error);
        });
}

/**
 * Initialise les fonctionnalités d'authentification Google
 */
function initGoogleAuth() {
    document.addEventListener('DOMContentLoaded', function() {
        // Message de l'iframe qui signale que l'authentification est terminée
        window.addEventListener('message', function(event) {
            if (event.data === 'auth_success') {
                console.log('Message reçu : Authentification réussie');
                authInProgress = false;
                closeAuthPopupIfOpen();
                setTimeout(redirectToAccount, 500);
            }
        }, false);
        
        // Google Sign In Popup
        const googleSignInBtn = document.getElementById('googleSignInBtn');
        if (googleSignInBtn) {
            googleSignInBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openGoogleAuthPopup('/google-auth-popup/');
            });
        }
        
        // Google Log In Popup
        const googleLogInBtn = document.getElementById('googleLogInBtn');
        if (googleLogInBtn) {
            googleLogInBtn.addEventListener('click', function(e) {
                e.preventDefault();
                openGoogleAuthPopup('/google-auth-popup/');
            });
        }
        
        // Vérifier l'état d'authentification régulièrement si nous sommes sur la page de connexion
        if (window.location.pathname.includes('sign-in') || window.location.pathname.includes('sign_in')) {
            // Vérifier toutes les 2 secondes
            setInterval(checkAuthStatus, 2000);
            // Vérifier aussi immédiatement après un court délai
            setTimeout(checkAuthStatus, 500);
        }
    });
}

// Export pour l'utilisation dans d'autres scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        initGoogleAuth, 
        openGoogleAuthPopup, 
        closeAuthPopupIfOpen, 
        redirectToAccount,
        checkAuthStatus 
    };
}
