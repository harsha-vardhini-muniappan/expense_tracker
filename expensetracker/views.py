from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.utils import timezone

def expense_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    expenses = Expense.objects.all().order_by('-date')

    if query:
        expenses = expenses.filter(title__icontains=query)
    if category:
        expenses = expenses.filter(category__icontains=category)

    total = sum(exp.amount for exp in expenses)

    return render(request, 'expense_list.html', {
        'expenses': expenses,
        'total': total,
        'query': query,
        'category': category
    })


def add_expense(request):
    if request.method == 'POST':
        title = request.POST['title']
        amount = request.POST['amount']
        category = request.POST['category']
        date = request.POST['date']
        description = request.POST.get('description', '')

        Expense.objects.create(
            title=title,
            amount=amount,
            category=category,
            date=date,
            description=description
        )
        return redirect('/')
    return render(request, 'add_expense.html')


def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == 'POST':
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.description = request.POST.get('description', '')
        expense.save()
        return redirect('/')
    return render(request, 'edit_expense.html', {'expense': expense})


def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('/')
