from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Host(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    ip_addr= models.GenericIPAddressField(unique=True)
    port=models.SmallIntegerField(default=22)
    idc = models.ForeignKey("IDC",blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name="主机表"


class RemoteUser(models.Model):
    auth_type_choices=((0,'ssh-password'),(1,"ssh-key"))
    auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
    username =  models.CharField(max_length=32)
    password =  models.CharField(max_length=64,blank=True,null=True)

    class Meta:
        verbose_name="远程用户表"

    def __str__(self):
        return self.username

class  HostToRemoteUser(models.Model):
    host =models.ForeignKey("Host",on_delete=models.CASCADE)
    remote_user=models.ForeignKey("RemoteUser",on_delete=models.CASCADE)

    class Meta:
        unique_together=("host","remote_user")
        verbose_name="主机关联远程用户表"

    def __str__(self):
        return "%s %s"%(self.host,self.remote_user)

class HostGroup(models.Model):
    name=models.CharField(max_length=64)
    host_to_remote_users=models.ManyToManyField("HostToRemoteUser")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="主机组"

class IDC(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name="IDC表"




class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self,email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''账号表'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )


    password = models.CharField(_('password'), max_length=128,help_text=mark_safe("<a href='password/'>修改密码</a>"))

    last_login=models.DateTimeField(blank=True, null=True, verbose_name='last login')
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    host_to_remote_users=models.ManyToManyField("HostToRemoteUser",blank=True,null=True)
    host_groups =models.ManyToManyField("HostGroup",blank=True,null=True)
    objects = UserProfileManager()

    #stu_account = models.ForeignKey("CustomerInfo",verbose_name="关联学员帐号",blank=True,null=True,help_text="只有学员报名后方可为其创建帐号",on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'   #让哪个字段做用户名
    REQUIRED_FIELDS = ['name']  #必须填字段

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    #是否有什么权限
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_active
    #
    def __str__(self):
        return "%s"%self.name


class AuditLog(models.Model):
        """存储审计日志"""
        user = models.ForeignKey("UserProfile",verbose_name="堡垒机帐号",on_delete=models.CASCADE)
        host_to_remote_user = models.ForeignKey("HostToRemoteUser",on_delete=models.CASCADE)
        log_type_choice = ((0,'login'),(1,'cmd'),(2,'logout'))
        log_type =models.SmallIntegerField(choices=log_type_choice)
        content = models.CharField(max_length=255)
        date =models.DateTimeField(auto_now_add=True)

        class Meta:
            verbose_name="存储审计日志表"
        def __str__(self):
            return "%s %s"%(self.user,self.content)




class Task(models.Model):
    """批量任务，大任务"""
    task_type_choices =  (("cmd",'批量命令'),("file_transfer","文件传输"))
    task_type = models.CharField(choices=task_type_choices,max_length=64)
    content = models.CharField(max_length=255,verbose_name="任务内容")
    user = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s"%(self.task_type,self.content)


class TaskLogDetail(models.Model):
    """存储大任务子结果"""
    task = models.ForeignKey("Task",on_delete=models.CASCADE)
    host_to_remote_user = models.ForeignKey("HostToRemoteUser",on_delete=models.CASCADE)
    result = models.TextField(verbose_name="任务执行结果",blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status_choices = ((0,"initialized"),(1,"sucess"),(2,"failed"),(3,"timeout"))
    status = models.SmallIntegerField(choices=status_choices,default=0)
    def __str__(self):
        return "%s %s"%(self.task,self.host_to_remote_user)





