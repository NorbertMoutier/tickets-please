import os
import django
import sys

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsplease.settings')
django.setup()

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

def create_test_user():
    print("Création d'un utilisateur de test...")
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(email='test@example.com').exists():
        print("L'utilisateur de test existe déjà.")
        user = User.objects.get(email='test@example.com')
    else:
        # Créer un nouvel utilisateur
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123456'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Utilisateur créé avec succès: {user.username} (ID: {user.id})")
    
    # Vérifier/créer l'adresse email vérifiée pour django-allauth
    if not EmailAddress.objects.filter(email='test@example.com').exists():
        EmailAddress.objects.create(
            user=user,
            email='test@example.com',
            primary=True,
            verified=True
        )
        print("Adresse email vérifiée créée pour l'utilisateur.")
    else:
        print("L'adresse email vérifiée existe déjà.")
    
    print("\nVous pouvez maintenant vous connecter avec:")
    print("Email: test@example.com")
    print("Mot de passe: password123456")
    
    return True

if __name__ == "__main__":
    print("=== CRÉATION D'UN UTILISATEUR DE TEST ===")
    success = create_test_user()
    if success:
        print("\nUtilisateur de test créé avec succès!")
    else:
        print("\nErreur lors de la création de l'utilisateur de test.")
        sys.exit(1)
