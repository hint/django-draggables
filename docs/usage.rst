Usage
=====

You can use **django-draggables** for sorting your models on changelist view
as well as sorting the inlines.

Setup your models first
-----------------------

As an opposite to **django-draggables**'s predcessor, *django-inline-ordering*,
this module does not require your models to inherit an abstract model class.
Instead of this, you have to add a ``draggables.fields.DraggableAutoField`` to
any model you want to make sortable. The field can be named anything, so it will
satisfy your innermost geek desires. Furthermore, custom admin classes (see
below) will introspect your models to find out what it's named, so that's the
only thing to change on your model.

If ``draggables.fields.DraggableAutoField`` does not exist on some model,
it will not be draggable and **django-draggables** will fail silently. However
if you add two or more ``draggables.fields.DraggableAutoField`` instances to
any of the models introspected by ``draggables.admin.DraggableAdmin``, it will
raise a ``ImproperlyConfigured`` exception.

It *might* be a good idea to add
ordering attribute to your model Meta class, so sorting works out-of-the-box
in the frontend. Of course ordering *can* slow down the queries, so have that
in mind please.

Changelist usage
----------------

Your main admin class must inherit ``draggables.admin.DraggableAdmin``. This
class inherits ``django.contrib.admin.ModelAdmin`` so you can use it either
as a parent class for your admin class or as a mixin in class. You don't need
to subclass your inline admin classes.

Inline usage
------------

At the time of writing support for inlines is experimental, but working at
least under Django 1.2 with tabular inlines.
