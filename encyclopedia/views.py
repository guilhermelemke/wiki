from django.shortcuts import render, redirect
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/article.html", {
            "entry": markdown2.markdown(util.get_entry(name))
        })
    else:
        return render(request, "encyclopedia/error.html")

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

def create(request):
    return render(request, "encyclopedia/create.html")