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

class LogModel(models.Model):
    log_id = models.AutoField(unique= True ,primary_key=True)
    request_id = models.IntegerField()
    request_granted =  models.BooleanField(blank=False) 
    equipment = models.ForeignKey(EquipmentModel,on_delete=models.CASCADE)
    requested_by_user = models.ForeignKey(UserModel,on_delete=models.CASCADE, related_name='requested_by')
    actioned_by =  models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='actioned_by')

    class Meta:
        verbose_name = "Log Model"
        
    def __str__(self):
        return str(self.log_id)

class IssueBookModel(models.Model):
    issue_id = models.AutoField(unique= True ,primary_key=True)
    equipment = models.ForeignKey(EquipmentModel,on_delete=models.CASCADE)
    requested_by_user = models.ForeignKey(UserModel,on_delete=models.CASCADE, related_name='employee')
    actioned_by =  models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='manager')
    

    class Meta:
        verbose_name = "IssueBook Model"
        
    def __str__(self):
        return str(self.issue_id)