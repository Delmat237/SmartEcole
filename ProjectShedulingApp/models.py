from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError

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
'''class Person(AbstractUser):
    id = models.AutoField(primary_key=True)
    avatar = models.ImageField(verbose_name="avatar", upload_to="profile_photos/", blank=True, null=True) 
    matricule = models.CharField(max_length=50, unique=True)
    phoneNumber = models.CharField(max_length=20)

    class Meta:
        abstract = True
'''
# Nouveau modèle User concret

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
        ('admin', 'Administrateur'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="student")

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile',null=True, blank=True)
    email = models.EmailField(
    max_length=255,  # Limite la longueur de l'email
    unique=True,  # Assure que chaque email est distinct
    blank=False,  # Empêche de laisser le champ vide
    null=False,  # Le champ ne peut pas être NULL dans la base de données
    verbose_name="Adresse email",  # Nom lisible en admin,
    default="nothing@gmail.com"
)

    #avatar = models.ImageField(verbose_name="avatar", upload_to="profile_photos/", null=True,blank=True)  # Suppression du `related_name`
    matricule = models.CharField(max_length=50, unique=True, default="00000")
    phone_number = models.CharField(max_length=20, default="0000000")
    niveau = models.CharField(max_length=50, default="0")
    password = models.CharField(("password"), max_length=128,default="nothing")

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='teachers')
    matricule = models.CharField(max_length=50, unique=True, default="00000")
    phone_number = models.CharField(max_length=20, default="0000000")
    password = models.CharField(("password"), max_length=128,default="nothing")
    


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
    #personne = models.ForeignKey('PersonneBase', on_delete=models.CASCADE, related_name='requetes')

# 10. Personne de base pour gestion générique
class PersonneBase(models.Model):
    name = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=20)

    def __str__(self):
        return self.name




class ClassRoom(models.Model):
    """
    Salle de classe
    """
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    building = models.CharField(max_length=50)
    floor = models.IntegerField()
    room_number = models.CharField(max_length=10)
    has_projector = models.BooleanField(default=False)
    has_computers = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Salle de classe"
        verbose_name_plural = "Salles de classe"
        
    def __str__(self):
        return f"{self.name} - {self.building} ({self.room_number})"


class Computer(models.Model):
    """
    Ordinateur
    """
    inventory_number = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    specs = models.TextField()
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=(
        ('available', 'Disponible'),
        ('reserved', 'Réservé'),
        ('maintenance', 'En maintenance'),
    ), default='available')
    location = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "Ordinateur"
        verbose_name_plural = "Ordinateurs"
        
    def __str__(self):
        return f"{self.brand} {self.model} - {self.inventory_number}"


class Projector(models.Model):
    """
    Vidéo projecteur
    """
    inventory_number = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    resolution = models.CharField(max_length=20)
    purchase_date = models.DateField()
    status = models.CharField(max_length=20, choices=(
        ('available', 'Disponible'),
        ('reserved', 'Réservé'),
        ('maintenance', 'En maintenance'),
    ), default='available')
    location = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "Vidéo Projecteur"
        verbose_name_plural = "Vidéo Projecteurs"
        
    def __str__(self):
        return f"{self.brand} {self.model} - {self.inventory_number}"
    



'''
class Department(models.Model):
    """
    Département académique
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        
    def __str__(self):
        return self.name

'''
class Service(models.Model):
    """
    Service administratif
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        
    def __str__(self):
        return self.name



class Reservation(models.Model):
    """
    Réservation d'une ressource
    """
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        ('cancelled', 'Annulée'),
    )

    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations')
    resource_type = models.CharField(max_length=20, choices=[('classroom', 'Salle de classe'), ('computer', 'Ordinateur'), ('projector', 'Vidéo projecteur')])
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    projector = models.ForeignKey(Projector, on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Réservation ({self.resource_type}) - {self.requester.username} ({self.start_datetime.strftime('%d/%m/%Y')})"

    def cancel_reservation(self):
        """Annuler la réservation."""
        if self.status in ['approved', 'pending']:
            self.status = 'cancelled'
            self.save()
        else:
            raise ValidationError("Impossible d'annuler une réservation déjà rejetée ou annulée.")


