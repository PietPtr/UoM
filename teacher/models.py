from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    study_load = models.IntegerField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Aim(models.Model):
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.course, self.description)


class Action(models.Model):
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    aims = models.ManyToManyField(Aim)

    def __str__(self):
        return self.description


class Material(models.Model):
    file = models.FileField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (file.name, course)
