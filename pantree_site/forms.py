from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import CustomUser
from pantree_app.models import CustomUser


# Create your forms here.

class NewUserForm(UserCreationForm):
	# email = forms.EmailField(required=True)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
		self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
		self.fields['password1'].widget.attrs.update({'placeholder': ('Password')})        
		self.fields['password2'].widget.attrs.update({'placeholder': ('Repeat password')})

	class Meta:
		model = CustomUser
		fields = ("email", "password1", "password2")
		widgets = {
            # 'username' : forms.TextInput(attrs={'placeholder': 'Username'}),
            'email' : forms.TextInput(attrs={'placeholder': 'Email'}),
			'password1' : forms.TextInput(attrs={'placeholder': 'Username'}),
			'password2' : forms.TextInput(attrs={'placeholder': 'test'}),
        }

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user