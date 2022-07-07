# from django.http import HttpResponseRedirect
from django.shortcuts import render
from .src.pantree.panTree import panTree


from .forms import IngredientForm

def get_ingredients(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IngredientForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            raw = form.cleaned_data.get('ingredients')
            sep = [x.strip() for x in raw.split(',')]
            p = panTree(sep, '/Users/sabakarimeddiny/Documents/pantree-site/pantree_app/src/data/bank.json')
            p.process()
            return result(request, p.rank)
        # render(request, 'thanks.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IngredientForm()

    return render(request, 'ingredients.html', {'form': form})

def result(request, result):
    return render(request, 'result.html', {'result' : result})