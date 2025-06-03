import os
import django

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Supprimer toutes les applications sociales Google existantes
google_apps = SocialApp.objects.filter(provider='google')
print(f"Nombre d'applications Google trouvées: {google_apps.count()}")

if google_apps.count() > 1:
    # Garder seulement la première et supprimer les autres
    first_app = google_apps.first()
    for app in google_apps.exclude(id=first_app.id):
        print(f"Suppression de l'application Google en double (ID: {app.id})")
        app.delete()
    
    # S'assurer que l'application restante est correctement configurée
    first_app.name = "Google"
    first_app.client_id = "1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com"
    first_app.secret = "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"
    first_app.save()
    print(f"Application Google restante mise à jour (ID: {first_app.id})")
    
    # S'assurer que l'application est associée au site
    site = Site.objects.get(id=1)
    if site not in first_app.sites.all():
        first_app.sites.add(site)
        print(f"Site associé à l'application Google")
    
elif google_apps.count() == 0:
    # Créer une nouvelle application si aucune n'existe
    site = Site.objects.get(id=1)
    app = SocialApp.objects.create(
        provider='google',
        name='Google',
        client_id='1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com',
        secret='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'
    )
    app.sites.add(site)
    print(f"Nouvelle application Google créée (ID: {app.id})")
else:
    # Mettre à jour l'application existante
    app = google_apps.first()
    app.name = "Google"
    app.client_id = "1077033830192-7kibtoe53d8clc6pgo8nm0ibsmfvko8t.apps.googleusercontent.com"
    app.secret = "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"
    app.save()
    
    # S'assurer que l'application est associée au site
    site = Site.objects.get(id=1)
    if site not in app.sites.all():
        app.sites.add(site)
    print(f"Application Google existante mise à jour (ID: {app.id})")

print("Terminé!")
