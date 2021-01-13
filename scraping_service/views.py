from django.shortcuts import render
import datetime


def home(request):
    """View of the Home Page.
    Returns context as name and date"""
    date = datetime.datetime.now().date()
    name = 'Dave'
    _context = {'date': date, 'name': name}
    return render(request, 'base.html', _context)
