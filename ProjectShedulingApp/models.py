from django.db import models
from django.contrib.auth.models import AbstractUser

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

# 3. Personne (abstrait)
class Person(AbstractUser):
    id = models.AutoField(primary_key=True)
    avatar = models.ImageField(verbose_name="avatar", upload_to="profile_photos/", blank=True, null=True) 
    matricule = models.CharField(max_length=50, unique=True)
    phoneNumber = models.CharField(max_length=20)

    class Meta:
        abstract = True

# Nouveau modèle User concret
class CustomUser(Person):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

class Student(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    niveau = models.CharField(max_length=50)

class Teacher(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='teachers')

# 6. Département
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 7. Service administratif
class AdministrativeService(models.Model):
    SERVICE_TYPES = [
        ('SCOLARITE', 'Scolarité'),
        ('FINANCIER', 'Financier'),
        ('AUTRE', 'Autre'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 8. Membre administratif
class MembreAdmin(models.Model):
    ADMIN_TYPES = [
        ('RESPONSABLE', 'Responsable'),
        ('AGENT', 'Agent'),
        ('AUTRE', 'Autre'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ADMIN_TYPES)
    poste = models.CharField(max_length=100)
    administrative_service = models.ForeignKey(AdministrativeService, on_delete=models.CASCADE, related_name='membres')

    def __str__(self):
        return self.name

# 9. Requête
class Requete(models.Model):
    STATUS_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('TRAITEE', 'Traitée'),
        ('REFUSEE', 'Refusée'),
    ]
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    administrative_service = models.ForeignKey(AdministrativeService, on_delete=models.CASCADE, related_name='requetes')
    personne = models.ForeignKey('PersonneBase', on_delete=models.CASCADE, related_name='requetes')

# 10. Personne de base pour gestion générique
class PersonneBase(models.Model):
    name = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=20)

    def __str__(self):
        return self.name
