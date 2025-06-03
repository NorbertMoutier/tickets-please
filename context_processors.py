def translations(request):
    TRANSLATIONS = {
        'fr': {
            'Features': 'Fonctionnalités',
            'How it works': 'Comment ça marche',
            'Testimonials': 'Témoignages',
            'Sign in': 'Se connecter',
            'Join the beta': 'Rejoindre la bêta',
            'All your travel tickets, one tap away.': 'Tous vos billets de voyage, en un clic.',
            'Stop digging through emails. Tickets Please gathers every QR-code and booking for you—online and offline.': 'Arrêtez de fouiller dans vos emails. Tickets Please rassemble tous vos QR-codes et réservations—en ligne et hors ligne.',
            'Watch demo': 'Voir la démo',
            'From chaos to peace of mind': 'Du chaos à la tranquillité d\'esprit',
            'The travel ticket nightmare': 'Le cauchemar des billets de voyage',
            'Lost in endless email threads, missed bookings, and last-minute scrambles to find QR codes.': 'Perdus dans des fils d\'emails sans fin, réservations manquées et recherches de dernière minute pour trouver les QR codes.',
            'Tickets Please simplicity': 'La simplicité de Tickets Please',
            'Everything in one place, sorted chronologically, accessible offline, with smart reminders.': 'Tout au même endroit, trié chronologiquement, accessible hors ligne, avec des rappels intelligents.',
            'Travel smarter, not harder': 'Voyagez plus intelligemment, pas plus difficilement',
            'Tickets Please takes the stress out of travel organization so you can focus on the experience.': 'Tickets Please élimine le stress de l\'organisation des voyages pour que vous puissiez vous concentrer sur l\'expérience.',
        }
    }
    
    current_lang = request.LANGUAGE_CODE
    translations = TRANSLATIONS.get(current_lang, {})
    
    def translate(text):
        return translations.get(text, text)
    
    return {
        'translate': translate
    }
