from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your Name: ', max_length=100)

class IngredientForm(forms.Form):
    ingredients = forms.CharField(label='Ingredients', max_length=1000)
    max_missing_ings = forms.IntegerField(label='Max. Missing Ingredients', max_value=50)

# class IntForm(forms.Form):
    