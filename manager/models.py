from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User, Group


class File(models.Model):
    # 文件名
    name = models.CharField(max_length=255)

    # 文件属主（外键关联到User模型）
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_files')

    # 文件属组（外键关联到Group模型）
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_files')

    # 权限位（整数字段）
    # 假设我们使用一个3位的整数来表示权限，每位代表读、写、执行权限
    # 例如，7代表读、写、执行都有，6代表读、写权限，4代表只读权限
    permissions = models.IntegerField()
