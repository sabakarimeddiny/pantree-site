from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your Name: ', max_length=100)

class IngredientForm(forms.Form):
    ingredients = forms.CharField(label='ingredients I have', max_length=10000, required=False)
    must_have_ings = forms.CharField(label = 'only show me recipes that have', max_length=1000, required=False)
    # max_missing_ings = forms.IntegerField(label='max. number of missing ingredients (optional)', max_value=100, required=False)

# class IntForm(forms.Form):
    