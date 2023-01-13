from django.db import models

# Create your models here.


class Login(models.Model):
    username = models.CharField(max_length=250, blank=False)
    password = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.username


class EmailLogin(models.Model):
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.email


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=300, blank=False)

    def __str__(self):
        return self.phone_number
        

def PhoneNumberView(request):
    form = PhoneNumberForm(request.POST or None)

    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'index.html', context)
