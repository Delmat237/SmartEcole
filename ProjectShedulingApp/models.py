from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# 1. Catégorie de ressource
class CategoryResource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 2. Ressource (modèle de base désormais concret)
class MaterielPedagogique(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

# Héritage concret (OneToOne relation possible si besoin)
class Ordinateur(MaterielPedagogique):
    adresse_mac = models.CharField(max_length=17, unique=True)  
    processeur = models.CharField(max_length=50)
    ram = models.IntegerField()  
    stockage = models.IntegerField()  # En Go

class VideoProjecteur(MaterielPedagogique):
    resolution = models.CharField(max_length=20)  
    connectivite = models.CharField(max_length=50) 
    luminosite = models.IntegerField()  

class SalleDeClasse(MaterielPedagogique):
    capacite = models.IntegerField()  
    numero_salle = models.CharField(max_length=10, unique=True)


# 6. Département
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    
class Student(models.Model):
    matricule = models.CharField(max_length=50, unique=True)  # Identifiant unique
    niveau = models.IntegerField()
    name = models.CharField(max_length=100)  # Nom de l'étudiant
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)  # Mot de passe pour l'authentification
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, default='student')  # Rôle par défaut

class Teacher(models.Model):
    matricule = models.CharField(max_length=50, unique=True)  # Identifiant unique
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)  
    phone_number = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, default='teacher')  # Rôle par défaut
  
    
# 7. Service administratif
class AdministrativeService(models.Model):
    SERVICE_TYPES = [
        ('SCOLARITE', 'Scolarité'),
        ('FINANCIER', 'Financier'),
        ('AUTRE', 'Autre'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField(blank=True)


class MembreAdmin(models.Model):
    ADMIN_TYPES = [
        ('RESPONSABLE', 'Responsable'),
        ('AGENT', 'Agent'),
        ('AUTRE', 'Autre'),
    ]
    matricule = models.CharField(max_length=50, unique=True)  # Identifiant unique
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ADMIN_TYPES)
    poste = models.CharField(max_length=100)
    administrative_service = models.ForeignKey(AdministrativeService, on_delete=models.CASCADE, related_name='membres')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)  # Mot de passe pour l'authentification
    role = models.CharField(max_length=20, default='admin')  # Rôle par défaut


class Requete(models.Model):
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('TRAITEE', 'Traitée'),
        ('REFUSEE', 'Refusée'),
    ]

    objet = models.CharField(max_length=255)  # Le sujet ou le titre de la requête
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_ATTENTE')
    administrative_service = models.ForeignKey(
        'AdministrativeService',
        on_delete=models.CASCADE,
        related_name='requetes'
    )
    personne = models.ForeignKey(
        'PersonneBase',
        on_delete=models.CASCADE,
        related_name='requetes'
    )
    pieces_jointes = models.FileField(
        upload_to='requetes/pieces_jointes/',
        null=True,
        blank=True
    )  # Optionnel

# 10. Personne de base pour gestion générique
class PersonneBase(models.Model):
    matricule = models.CharField(max_length=50, unique=True)  # Identifiant unique
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('REFUSEE', 'Refusée'),
        ('ANNULEE', 'Annulée'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Champs pour lien générique vers ordinateur, vidéoprojecteur ou salle
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    ressource = GenericForeignKey('content_type', 'object_id')

    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_ATTENTE')
    created_at = models.DateTimeField(auto_now_add=True)

