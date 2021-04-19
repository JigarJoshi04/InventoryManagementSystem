from django.db import models
from users.models import UserModel
from equipments.models import EquipmentModel

# Create your models here.
class RequestModel(models.Model):
    request_id = models.AutoField(unique= True ,primary_key=True)
    equipment = models.ForeignKey(EquipmentModel,on_delete=models.CASCADE)
    requested_by_user = models.ForeignKey(UserModel,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Request Model"
        
    def __str__(self):
        return str(self.request_id)