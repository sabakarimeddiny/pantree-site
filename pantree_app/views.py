from django.shortcuts import render
from .src.pantree.panTree import panTree
from .models import User


from .forms import IngredientForm

def get_ingredients(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IngredientForm(request.POST,auto_id="ingForm_%s")
        # check whether it's valid:
        if form.is_valid(): # also fills the cleaned_data attr
            raw = form.cleaned_data.get('ingredients')
            must_haves = form.cleaned_data.get('must_have_ings')
            if request.POST.get("submitAndSave"):# or request.POST.get("save"):
                user = User.objects.get(username=request.POST['username'].strip())
                user.ings = (raw + ',' + must_haves).strip()
                user.save()
                if request.POST.get("save") == "Save":
                    return render(request, 'ingredients.html', {'form': form})
            sep_ing_list = [x.strip() for x in raw.split(',')]
            sep_must_have_list = [x.strip() for x in must_haves.split(',')]
            p = panTree(sep_ing_list, 
                        sep_must_have_list)
            num = p.db.count()
            if len(p.rank) != 0:
                return result(request, num, p.rank)
            else:
                return result(request, num, ['pantree could not find anything :('])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IngredientForm(auto_id="ingForm_%s")

    return render(request, 'ingredients.html', {'form': form})

def result(request, num, result):
    return render(request, 'result.html', {'num': num, 'result' : result})

def login(request):
    return render(request, 'login.html')
