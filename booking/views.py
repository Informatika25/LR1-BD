from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ReservationForm
from .models import Equipment, Reservation
from django.utils.dateparse import parse_date


@login_required
def reservation_list(request):
    items = (
        Reservation.objects.filter(user=request.user)
        .select_related("equipment")
        .order_by("start")
    )

    equipment_id = request.GET.get("equipment")
    start_date = request.GET.get("date")

    if equipment_id and equipment_id.isdigit():
        items = items.filter(equipment_id=equipment_id)
    if start_date:
        try:
            parsed = parse_date(start_date)
        except ValueError:
            parsed = None
        if parsed:
            items = items.filter(start__date=parsed)

    equipments = Equipment.objects.all()
    return render(
        request,
        "booking/list.html",
        {
            "items": items,
            "equipments": equipments,
            "selected_equipment": equipment_id or "",
            "selected_date": start_date or "",
        },
    )

@login_required
def reservation_create(request):
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect("reservation_list")
    return render(request, "booking/form.html", {"form": form})

@login_required
def reservation_edit(request, pk):
    item = get_object_or_404(Reservation, pk=pk, user=request.user)
    if not item.confirmed:
        return redirect("reservation_list")
    form = ReservationForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("reservation_list")
    return render(request, "booking/form.html", {"form": form})

@login_required
@require_POST
def reservation_cancel(request, pk):
    item = get_object_or_404(Reservation, pk=pk, user=request.user)
    item.confirmed = False
    item.save(update_fields=["confirmed"])
    return redirect("reservation_list")

@login_required
@require_POST
def reservation_delete(request, pk):
    item = get_object_or_404(Reservation, pk=pk, user=request.user)
    item.delete()
    return redirect("reservation_list")

def register(request):
    if request.user.is_authenticated:
        return redirect("reservation_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("reservation_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})