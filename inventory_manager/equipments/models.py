from django.db import models
from users.models import UserModel

class EquipmentModel(models.Model):
    equipment_id = models.AutoField(unique= True ,primary_key=True)
    equipment_name = models.CharField(max_length=500,blank=True)
    is_available = models.BooleanField(default=True) 
    added_by_user = models.ForeignKey(UserModel,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Equipment Model"
        
    def __str__(self):
        return self.equipment_name