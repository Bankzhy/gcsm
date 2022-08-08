from django.db import models
from django.utils import timezone
# Create your models here.
class ProjectMaster(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, blank=False, null=False)
    method_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    class_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "project_master"

class MethodWaitMaster(models.Model):
    method_id = models.AutoField(primary_key=True)
    method_name = models.CharField(max_length=100, blank=False, null=False)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    param_count = models.PositiveIntegerField(default=0, blank=False, null=False)
    return_type = models.CharField(max_length=100, blank=False, null=False)
    project_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    path = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    reviewed = models.BooleanField(default=False)

    class Meta:
        db_table = "method_wait_master"
        unique_together = ('method_id', 'project_id')


class NegMethodMaster(models.Model):
    method_id = models.PositiveIntegerField(primary_key=True)
    review_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "neg_method_master"


class QuesMaster(models.Model):
    ques_id = models.AutoField(primary_key=True)
    ques = models.CharField(max_length=100, blank=False, null=False)
    detail = models.CharField(max_length=1000, blank=False, null=False, default="")
    add_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        db_table = "ques_master"


class PosMethodMaster(models.Model):
    method_id = models.PositiveIntegerField(primary_key=True)
    review_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    level = models.PositiveIntegerField(default=0, blank=False, null=False)
    ex_pos = models.CharField(max_length=100,default="", blank=False, null=False)

    class Meta:
        db_table = "pos_method_master"


class MethodQues(models.Model):
    method_ques_id = models.AutoField(primary_key=True)
    ques_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    method_id = models.PositiveIntegerField(default=0, blank=False, null=False)
    answer = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = "method_ques"