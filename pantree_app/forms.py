from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your Name: ', max_length=100)

class IngredientForm(forms.Form):
    ingredients = forms.CharField(label='ingredients I have', max_length=1000)
    must_have_ings = forms.CharField(label = 'show me only recipes that have (optional)', max_length=1000, initial='')
    max_missing_ings = forms.IntegerField(label='max. number of missing ingredients', max_value=50, required=False)

# class IntForm(forms.Form):
    