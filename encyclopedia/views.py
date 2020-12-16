from django.shortcuts import render
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