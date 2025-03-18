# Step 1: Initialize the Django Project
# Run the following command in your terminal
# django-admin startproject myproject

# Step 2: Create an app
# Navigate into your project directory and run:
# python manage.py startapp myapp

# Step 3: Define a Model
# myapp/models.py
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

# Register the model in the admin panel
# myapp/admin.py
from django.contrib import admin
from .models import Item

admin.site.register(Item)

# Step 4: Create a View
# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm

def home(request):
    return HttpResponse("Welcome to My Django Project!")

def item_list(request):
    items = Item.objects.all()
    return render(request, 'myapp/item_list.html', {'items': items})

def item_form(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return HttpResponse(f"Item Created: {item.name}")
    else:
        form = ItemForm()
    return render(request, 'myapp/item_form.html', {'form': form})

# Step 5: URL Mapping
# myapp/urls.py
from django.urls import path
from .views import home, item_list, item_form

urlpatterns = [
    path('', home, name='home'),
    path('items/', item_list, name='item_list'),
    path('add-item/', item_form, name='item_form'),
]

# Step 6: Template Rendering
# Create templates folder: myapp/templates/myapp/
# myapp/templates/myapp/item_list.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>Item List</title>
</head>
<body>
    <h1>Item List</h1>
    <ul>
        {% for item in items %}
            <li>{{ item.name }} - {{ item.description }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# myapp/templates/myapp/item_form.html
"""
<!DOCTYPE html>
<html>
<head>
    <title>Add Item</title>
</head>
<body>
    <h1>Add a New Item</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# Step 7: Static Data Display
# The "Welcome to My Django Project!" message in the `home` view is static data.

# Step 8: Form Processing
# myapp/forms.py
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']

# Final Step: Register URLs in the Project
# myproject/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# Now, run migrations and start the server:
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
