from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """  store non-auth related information about user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chinesename = models.CharField(max_length=10)
    task = models.IntegerField(default=0)

    def add_task(self):
        self.task += 1
        self.save()

    def has_task(self):
        return self.task > 0


class Text(models.Model):
    """ store all text(example: usage) for whole site"""
    name = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=20, unique=True)
    content = models.TextField()


class TagList(models.Model):
    """ store all tag for function and skill"""
    CLASSES_LIST = [
        ('LB', 'library'),
        ('TP', 'topic')
    ]
    classes = models.CharField(choices=CLASSES_LIST)
    tag = models.CharField(max_length=20)


class RequestLog(models.Model):
    """ base class for all issue and modify request log """
    REQUEST_TYPE_LIST = [
        ('request', 'Request'),
        ('issue', 'Issue')
    ]
    request_type = models.CharField(choices=REQUEST_TYPE_LIST)
    subject = models.TextField(max_length=40)
    solution = models.TextField()
    note = models.TextField()
    confirm = models.BooleanField(default=False)
    creator = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    approver = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField('update time', auto_now_add=True)

    class Meta:
        abstract = True


class Library(models.Model):
    """ for python's build-in type, module and library """
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=400)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time', auto_now=True)
    visible = models.BooleanField(default=True)

    def hide(self):
        self.visible = False
        self.save()


class LibraryRequest(RequestLog):
    """ The issue of Library """
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


class Function(models.Model):
    """ for python's methods """
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=20)
    description = models.TextField(max_length=400)
    example = models.TextField(max_length=400)
    instance = models.TextField()
    tag = models.ForeignKey(TagList, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time', auto_now=True)
    visible = models.BooleanField(default=True)

    def hide(self):
        self.visible = False
        self.save()


class FunctionRequest(RequestLog):
    """ The issue of Function """
    function = models.ForeignKey(Function, on_delete=models.CASCADE)


class Topic(models.Model):
    """ The topic for less code """
    title = models.CharField(unique=True, max_length=40)
    description = models.TextField(max_length=400)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time', auto_now=True)
    visible = models.BooleanField(default=True)

    def hide(self):
        self.visible = False
        self.save()


class TopicRequest(RequestLog):
    """ The issue of Topic """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Skill(models.Model):
    """ The coding skills for each less code topic """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(unique=True, max_length=40)
    background = models.TextField(max_length=400)
    solution = models.TextField()
    tag = models.ForeignKey(TagList, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time', auto_now=True)
    visible = models.BooleanField(default=True)

    def hide(self):
        self.visible = False
        self.save()


class SkillRequest(RequestLog):
    """ The issue of Skill """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
