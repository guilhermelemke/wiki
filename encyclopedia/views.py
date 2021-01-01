from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
import markdown2
import random

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/article.html", {
            "entry": markdown2.markdown(util.get_entry(name)),
            "title": name,
        })
    else:
        return render(request, "encyclopedia/error.html")

def random_article(request):
    entry = random.choice(util.list_entries())
    return redirect('article', name=entry)

def search(request):
    original_query = (request.GET['q'])
    query = original_query
    entries = util.list_entries()
    results = []
    for entry in entries:
        entry.lower()
        if query in entry:
            results.append(entry)
    
    if query in entries:
        return redirect('article', name=query)
    elif results:
        return render(request, "encyclopedia/search.html", {
                "entries": results
            })
    else:
        return render(request, "encyclopedia/error.html")

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    markdown = forms.CharField(widget=forms.Textarea)

def create_entry(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]

            # Add the new task to our list of tasks
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html")
            else:
                util.save_entry(title, markdown)

            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("index"))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })


def edit_entry(request, title):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]

            # Add the new task to our list of tasks
            util.save_entry(title, markdown)

            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("article", args=[title]))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })

    return render(request, "encyclopedia/edit.html", {
        "form": NewPageForm(initial={'title': title, 'markdown': util.get_entry(title)})
    })
