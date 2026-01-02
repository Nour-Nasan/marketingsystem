from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm
from users.decorators import seller_required


@seller_required
def manage_categories(request):
    categories = Category.objects.filter(seller=request.user)
    return render(request, 'categories/manage_categories.html', {'categories': categories})


@seller_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.seller = request.user
            category.save()
            return redirect('categories:manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'categories/add_category.html', {'form': form})

@seller_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, seller=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories:manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/edit_category.html', {'form': form, 'category': category})


@seller_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, seller=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('categories:manage_categories')
    return render(request, 'categories/delete_category.html', {'category': category})
