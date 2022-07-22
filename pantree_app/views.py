from django.shortcuts import render, redirect
from django.urls import reverse
from .src.pantree.panTree import panTree
from .models import CustomUser


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
            if request.POST.get("submitAndSave") or request.POST.get("save"):
                user = CustomUser.objects.get(email=request.POST['email'].strip())
                ings = (raw + ',' + must_haves).strip()
                ings = ','.join([x.strip() for x in ings.split(',') if x != ''])
                user.ings = ings
                user.save()
                # if request.POST.get("save"):
                #     return render(request, 'ingredients.html', {'form': form})
            sep_ing_list = [x.strip() for x in raw.split(',')]
            sep_must_have_list = [x.strip() for x in must_haves.split(',')]
            p = panTree(sep_ing_list, 
                        sep_must_have_list)
            num = p.db.count()
            if len(p.rank) != 0:
                print(p.rank[:3])
                return result(request, num, p.rank)
            else:
                return result(request, num, ['pantree could not find anything :('])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IngredientForm(auto_id="ingForm_%s")

    return render(request, 'ingredients.html', {'form': form})

def result(request, num, rank):
    # return redirect(request, 'result_page', {'num': num, 'result' : rank})
    return render(request, 'result.html', {'num': num, 'rank' : rank})

def login(request):
    return render(request, 'login.html')
