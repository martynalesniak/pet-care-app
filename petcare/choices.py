from django.db import models

class Characteristic(models.TextChoices):
    PLAYFUL = 'Playful', 'Playful'
    SHY = 'Shy', 'Shy'
    FRIENDLY = 'Friendly', 'Friendly'
    ACTIVE = 'Active', 'Active'
    LAZY = 'Lazy', 'Lazy'
    INDEPENDENT = 'Independent', 'Independent'
    LOYAL = 'Loyal', 'Loyal'
    INTELLIGENT = 'Intelligent', 'Intelligent'

class EnergyLevel(models.IntegerChoices):
    LOW = 1, 'Low'  
    MEDIUM_LOW = 2, 'Medium Low'  
    MEDIUM = 3, 'Medium' 
    MEDIUM_HIGH = 4, 'Medium High' 
    HIGH = 5, 'High' 