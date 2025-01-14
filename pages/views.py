# pages/views.py
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from pages.models import Item, ToDoList

def homePageView(request):
    # return request object and specify page.
    return render(request, 'home.html', {
        'mynumbers':[1,2,3,4,5,6,],
        'firstName': 'Brian',
        "lastName": "Lee"
    })


import pdb;
def homePost(request):
    # Use request object to extract choice.

    choice = -999
    gmat = -999 # Initialize gmat variable.

    try:
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']
        # Extract value from request object by control name.
        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice    = int(currentChoice)
        gmat = float(gmatStr)
    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage':'*** The data submitted is invalid. Please try again.',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice':choice,'gmat':gmat},))


import pickle
import pandas as pd
import os
from django.conf import settings

def results(request, choice, gmat):
    print("*** Inside reults()")
    model_path = os.path.join(settings.BASE_DIR, 'model_pkl')

    # load saved model
    with open(model_path , 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf._append({'gmat':gmat,
                                            'work_experience':workExperience},
                                        ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat':gmat,
                'prediction':singlePrediction})


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')

def firstNameView(request):
    return render(request, 'brian.html')

def todos(request):
    items = Item.objects
    itemErrandDetail = items.select_related('todolist')
    print(itemErrandDetail[0].todolist.name)
    print(itemErrandDetail[0].text)
    print(itemErrandDetail[0].id)
    return render(request, 'ToDoItems.html',
                {'ToDoItemDetail': itemErrandDetail})

