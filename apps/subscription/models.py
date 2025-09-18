# from django.db import models
# from django.conf import settings
# User = models.get_user_model()
# # Create your models here.
# class UserSubscription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     subscription_type = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"User {self.user_id} - {self.subscription_type}"