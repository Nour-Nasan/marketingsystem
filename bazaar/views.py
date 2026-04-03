from django.shortcuts import get_object_or_404, redirect, render

from users.decorators import bazar_organizer_required

from .forms import BazaarForm
from .models import Bazaar


@bazar_organizer_required
def my_bazaars(request):
    bazaars = Bazaar.objects.filter(organizer=request.user).order_by('-start_datetime')
    return render(request, 'bazaar/my_bazaars.html', {'bazaars': bazaars})


@bazar_organizer_required
def add_bazaar(request):
    if request.method == 'POST':
        form = BazaarForm(request.POST, request.FILES)
        if form.is_valid():
            bazaar = form.save(commit=False)
            bazaar.organizer = request.user
            bazaar.save()
            return redirect('bazaar:my_bazaars')
    else:
        form = BazaarForm()
    return render(request, 'bazaar/bazaar_form.html', {'form': form, 'is_edit': False})


@bazar_organizer_required
def edit_bazaar(request, bazaar_id):
    bazaar = get_object_or_404(Bazaar, pk=bazaar_id, organizer=request.user)
    if request.method == 'POST':
        form = BazaarForm(request.POST, request.FILES, instance=bazaar)
        if form.is_valid():
            form.save()
            return redirect('bazaar:my_bazaars')
    else:
        form = BazaarForm(instance=bazaar)
    return render(
        request,
        'bazaar/bazaar_form.html',
        {'form': form, 'is_edit': True, 'bazaar': bazaar},
    )


@bazar_organizer_required
def delete_bazaar(request, bazaar_id):
    bazaar = get_object_or_404(Bazaar, pk=bazaar_id, organizer=request.user)
    if request.method == 'POST':
        bazaar.delete()
        return redirect('bazaar:my_bazaars')
    return render(request, 'bazaar/delete_bazaar.html', {'bazaar': bazaar})
