from django.db import models

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    note = models.CharField(max_length=200, default='')  # 為新字段設置默認值為空字符串
    created_at = models.DateTimeField(auto_now_add=True)
