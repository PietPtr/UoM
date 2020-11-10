from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def study_load(self):
        load = Action.objects.filter(course_id=self.id).aggregate(
            models.Sum('load'))['load__sum']
        return 0 if load == None else load

    def weeks(self):
        return Week.objects.filter(course_id=self.id).aggregate(models.Max('number'))['number__max']


class Week(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "'%s' week %s" % (self.course, self.number)


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
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    @classmethod
    def create(cls, description, course, week, load):
        ordering = Action.objects.all().count()
        action = cls(description=description,
                     course=course, load=load, week=week, ordering=ordering)
        return action

    def clean(self):
        if self.course.id != self.week.course.id:
            raise ValidationError(
                'Action week does not belong to action course')
