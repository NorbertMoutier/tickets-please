/**
 * Animation d'avion avec traînée de nuages
 * Ce script gère l'animation d'un avion qui se déplace sur l'écran
 * et laisse derrière lui une traînée de nuages qui s'estompent
 */

class PlaneAnimation {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.planeImage = new Image();
        this.cloudImage = new Image();
        
        // Charger les images
        this.planeImage.src = '/static/logos/avion.png';
        this.cloudImage.src = '/static/logos/nuage.png';
        
        // Initialiser les dimensions du canvas
        this.initCanvas();
        
        // Tableau pour stocker les avions
        this.planes = [];
        
        // Initialiser l'avion
        this.initPlanes();
        
        // Ajouter les gestionnaires d'événements
        this.addEventListeners();
        
        // Démarrer l'animation
        this.animate();
    }
    
    /**
     * Initialise les dimensions du canvas pour qu'il occupe tout l'écran
     */
    initCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        // Gérer le redimensionnement de la fenêtre
        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        });
    }
    
    /**
     * Initialise les propriétés de l'avion
     */
    initPlanes() {
        const angle0 = Math.random() * Math.PI * 2;
        const speed = 1.3; // Vitesse légèrement réduite pour mieux voir la courbe

        // Un seul avion qui démarre au centre de l'écran
        this.planes.push({
            x: this.canvas.width / 2,  // Centre horizontal
            y: this.canvas.height / 2, // Centre vertical
            size: 48,
            speed: speed,
            dx: Math.cos(angle0),  // Direction X normalisée
            dy: Math.sin(angle0),  // Direction Y normalisée
            angle: angle0,         // Angle initial aléatoire
            clouds: [],
            lastCloudTime: Date.now(),
            lastPosition: null,
            isDragging: false,
            savedDx: 0,
            savedDy: 0,
            // Paramètres pour la trajectoire courbée - plus accentués
            turnSpeed: (Math.random() * 0.8 + 0.3) * Math.PI / 180, // 0.3-1.1° par frame (plus de courbe)
            turnDir: Math.random() < 0.5 ? -1 : 1, // Sens de rotation aléatoire
            changeDirectionProbability: 0.3, // Probabilité de changer de direction à chaque frame
            time: 0,
            wiggleAmplitude: 5 // Amplitude du wiggle en degrés
        });
    }
    
    /**
     * Ajoute les gestionnaires d'événements pour l'interaction avec l'avion
     */
    addEventListeners() {
        // Événements de souris
        this.canvas.addEventListener('mousedown', this.handleMouseDown.bind(this));
        this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.canvas.addEventListener('mouseup', this.handleMouseUp.bind(this));
        this.canvas.addEventListener('mouseleave', this.handleMouseUp.bind(this));
        
        // Événements tactiles
        this.canvas.addEventListener('touchstart', this.handleTouchStart.bind(this));
        this.canvas.addEventListener('touchmove', this.handleTouchMove.bind(this));
        this.canvas.addEventListener('touchend', this.handleTouchEnd.bind(this));
        this.canvas.addEventListener('touchcancel', this.handleTouchEnd.bind(this));
    }
    
    /**
     * Normalise le vecteur de direction pour maintenir une vitesse constante
     */
    normalizeDirection() {
        const magnitude = Math.sqrt(this.plane.dx * this.plane.dx + this.plane.dy * this.plane.dy);
        if (magnitude > 0) {
            this.plane.dx /= magnitude;
            this.plane.dy /= magnitude;
        }
    }
    
    /**
     * Met à jour la position de l'avion avec une trajectoire visiblement courbée
     */
    updatePlane() {
        const now = Date.now();
        const plane = this.planes[0];
        
        // Initialiser la dernière position s'il n'y en a pas encore
        if (plane.lastPosition === null) {
            plane.lastPosition = { x: plane.x, y: plane.y };
        }
        
        // Ne déplacer l'avion que s'il n'est pas en train d'être déplacé manuellement
        if (!plane.isDragging) {
            // Mettre à jour le temps pour l'animation
            plane.time = performance.now() * 0.001; // Temps en secondes
            
            // Probabilité de changement de direction pour une trajectoire plus naturelle
            if (Math.random() < plane.changeDirectionProbability) {
                plane.turnDir *= -1; // Inverser la direction de virage
                
                // Varier légèrement la vitesse de virage à chaque changement
                plane.turnSpeed = (Math.random() * 0.8 + 0.3) * Math.PI / 180;
            }
            
            // Faire tourner légèrement l'avion
            plane.angle += plane.turnDir * plane.turnSpeed;
            
            // Ajouter un effet de virage sinusoïdal (wiggle) plus prononcé
            const wiggle = (plane.wiggleAmplitude * Math.sin(plane.time * 0.5)) * Math.PI / 180;
            plane.angle += wiggle * 0.2; // Réduction de l'effet pour éviter des virages trop brusques
            
            // Mettre à jour la direction de déplacement
            plane.dx = Math.cos(plane.angle);
            plane.dy = Math.sin(plane.angle);
            
            // Mettre à jour la position
            plane.x += plane.dx * plane.speed;
            plane.y += plane.dy * plane.speed;
        }
        
        // Faire réapparaître l'avion de l'autre côté s'il sort de l'écran
        if (plane.x < -plane.size) {
            plane.x = this.canvas.width + plane.size;
        } else if (plane.x > this.canvas.width + plane.size) {
            plane.x = -plane.size;
        }
        
        if (plane.y < -plane.size) {
            plane.y = this.canvas.height + plane.size;
        } else if (plane.y > this.canvas.height + plane.size) {
            plane.y = -plane.size;
        }
        
        // Créer un nouveau nuage tous les 2 secondes (fréquence basse)
        if (now - plane.lastCloudTime >= 2000) {
            // Position légèrement derrière l'avion
            const offset = 10; // Distance derrière l'avion
            const cloudX = plane.x - (plane.dx * offset);
            const cloudY = plane.y - (plane.dy * offset);
            
            // Taille aléatoire pour plus de variété
            const size = 15 + Math.random() * 10;
            
            plane.clouds.push({
                x: cloudX,
                y: cloudY,
                size: size,
                timestamp: now,
                opacity: 1.0
            });
            
            // Mettre à jour la dernière position et l'horodatage
            plane.lastPosition = { x: plane.x, y: plane.y };
            plane.lastCloudTime = now;
        }
        
        // Mettre à jour l'opacité des nuages et nettoyer ceux qui sont invisibles
        const now_sec = now / 1000; // Convertir en secondes
        
        // Pour chaque nuage, diminuer son opacité (10% par seconde)
        for (let i = 0; i < plane.clouds.length; i++) {
            const cloud = plane.clouds[i];
            const elapsedSec = (now - cloud.timestamp) / 1000;
            cloud.opacity = Math.max(0, 1.0 - (elapsedSec * 0.1)); // -10% par seconde
        }
        
        // Supprimer les nuages complètement transparents (après 10 secondes)
        plane.clouds = plane.clouds.filter(cloud => cloud.opacity > 0);
    }
    
    /**
     * Dessine les nuages laissés par l'avion
     */
    drawTrails() {
        const plane = this.planes[0];
        // Dessiner chaque nuage de la traînée
        for (let i = 0; i < plane.clouds.length; i++) {
            const cloud = plane.clouds[i];
            this.ctx.save();
            this.ctx.globalAlpha = cloud.opacity * 0.7; // Opacité réduite pour un effet plus subtil
            this.ctx.drawImage(
                this.cloudImage,
                cloud.x - cloud.size / 2,
                cloud.y - cloud.size / 2,
                cloud.size,
                cloud.size
            );
            this.ctx.restore();
        }
    }
    
    /**
     * Dessine l'avion à sa position actuelle
     */
    drawPlane() {
        const plane = this.planes[0];
        // Dessiner l'avion
        const width = plane.size * 2;
        const height = plane.size;
        
        this.ctx.save();
        // Positionner l'avion
        this.ctx.translate(plane.x, plane.y);
        // Faire tourner l'avion selon sa direction (ajouter Math.PI/2 si l'image pointe vers le haut)
        this.ctx.rotate(plane.angle + Math.PI/2);
        // Appliquer une légère transparence
        this.ctx.globalAlpha = 0.9;
        // Dessiner l'image centrée sur la position
        this.ctx.drawImage(this.planeImage, -width/2, -height/2, width, height);
        // Réinitialiser l'opacité
        this.ctx.globalAlpha = 1.0;
        this.ctx.restore();
    }
    
    /**
     * Fonction d'animation principale
     */
    animate() {
        // Effacer le canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Mettre à jour et dessiner chaque avion
        for (let i = 0; i < this.planes.length; i++) {
            this.updatePlane();
            this.drawTrails();
            this.drawPlane();
        }
        
        // Boucle d'animation
        requestAnimationFrame(this.animate.bind(this));
    }
    
    /**
     * Vérifie si un point (x,y) se trouve sur l'avion
     */
    isClickOnPlane(x, y) {
        const plane = this.planes[0];
        const dx = x - plane.x;
        const dy = y - plane.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < plane.size; // Si le clic est dans le rayon de l'avion
    }
    
    /**
     * Gestion du clic de souris
     */
    handleMouseDown(e) {
        const plane = this.planes[0];
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        if (this.isClickOnPlane(x, y)) {
            // Sauvegarder la direction actuelle
            plane.savedDx = plane.dx;
            plane.savedDy = plane.dy;
            
            // Arrêter le mouvement
            plane.dx = 0;
            plane.dy = 0;
            plane.isDragging = true;
            
            // Changer le style du curseur
            this.canvas.style.cursor = 'grabbing';
        }
    }
    
    /**
     * Gestion du déplacement de la souris
     */
    handleMouseMove(e) {
        const plane = this.planes[0];
        if (plane.isDragging) {
            const rect = this.canvas.getBoundingClientRect();
            plane.x = e.clientX - rect.left;
            plane.y = e.clientY - rect.top;
        }
    }
    
    /**
     * Gestion du relâchement de la souris
     */
    handleMouseUp() {
        const plane = this.planes[0];
        if (plane.isDragging) {
            // Restaurer la direction sauvegardée
            plane.dx = plane.savedDx;
            plane.dy = plane.savedDy;
            plane.isDragging = false;
            
            // Réinitialiser le curseur
            this.canvas.style.cursor = 'default';
        }
    }
    
    /**
     * Gestion du toucher (pour appareils mobiles)
     */
    handleTouchStart(e) {
        const plane = this.planes[0];
        e.preventDefault();
        const rect = this.canvas.getBoundingClientRect();
        const touch = e.touches[0];
        const x = touch.clientX - rect.left;
        const y = touch.clientY - rect.top;
        
        if (this.isClickOnPlane(x, y)) {
            // Sauvegarder la direction actuelle
            plane.savedDx = plane.dx;
            plane.savedDy = plane.dy;
            
            // Arrêter le mouvement
            plane.dx = 0;
            plane.dy = 0;
            plane.isDragging = true;
        }
    }
    
    /**
     * Gestion du déplacement du doigt
     */
    handleTouchMove(e) {
        const plane = this.planes[0];
        e.preventDefault();
        if (plane.isDragging) {
            const rect = this.canvas.getBoundingClientRect();
            const touch = e.touches[0];
            plane.x = touch.clientX - rect.left;
            plane.y = touch.clientY - rect.top;
        }
    }
    
    /**
     * Gestion de la fin du toucher
     */
    handleTouchEnd(e) {
        e.preventDefault();
        this.handleMouseUp(); // Réutiliser la même fonction que pour la souris
    }
}

// Fonction d'initialisation à appeler sur le document ready
function initPlaneAnimation(canvasId = 'planeCanvas') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => init(canvasId));
    } else {
        init(canvasId);
    }
}

function init(canvasId) {
    if (document.getElementById(canvasId)) {
        new PlaneAnimation(canvasId);
    } else {
        console.warn(`Canvas with id '${canvasId}' not found`);
    }
}

// Démarrer automatiquement quand le script est chargé
initPlaneAnimation('planeCanvas');

// Export pour l'utilisation dans d'autres scripts (Node.js)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PlaneAnimation, initPlaneAnimation };
}
