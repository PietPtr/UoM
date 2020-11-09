from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Aim(models.Model):
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.course, self.description)


class Material(models.Model):
    # TODO: misschien mogelijkheid nodig om files betere namen te geven
    # TODO: misschien moet het ook een description krijgen of zo in de teacher view
    file = models.FileField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.file.name, self.course)


class Action(models.Model):
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    aims = models.ManyToManyField(Aim, blank=True)
    materials = models.ManyToManyField(Material, blank=True)
    load = models.IntegerField()
    ordering = models.IntegerField()

    def __str__(self):
        return self.description
