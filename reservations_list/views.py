from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation

import re


def index(request):
    reservations = Reservation.objects.order_by('number')

    paginator = Paginator(reservations, 20)
    page = request.GET.get('page')

    try:
        reservations = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        reservations = paginator.get_page(1)

    index = reservations.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'reservations': reservations,
        'page_range': page_range

    }
    return render(request, 'index.html', context)


def reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    date_validation = '^20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'

    context = {
        'reservation': reservation
    }
    if request.method == 'POST':
        if request.POST.get('arrival_date'):
            arrival_date = request.POST['arrival_date']
            if re.match(date_validation, arrival_date):
                reservation_to_update = Reservation.objects.get(id=reservation_id)
                reservation_to_update.arrival = arrival_date
                reservation_to_update.save()
            else:
                messages.error(request, 'Please enter correct date format (yyyy-mm-dd)')

        elif request.POST.get('departure_date'):
            departure_date = request.POST['departure_date']
            if re.match(date_validation, departure_date):
                reservation_to_update = Reservation.objects.get(id=reservation_id)
                reservation_to_update.departure = departure_date
                reservation_to_update.save()
            else:
                messages.error(request, 'Please enter correct date format (yyyy-mm-dd)')

        elif request.POST.get('cancel_reservation'):
            reservation_to_update = Reservation.objects.get(id=reservation_id)
            reservation_to_update.status = 'CANCELLED'
            reservation_to_update.save()
            messages.info(request, 'Reservation has been cancelled')
        elif request.POST.get('reopen_reservation'):
            reservation_to_update = Reservation.objects.get(id=reservation_id)
            reservation_to_update.status = 'NEW'
            reservation_to_update.save()
            messages.info(request, 'Reservation has been re-opened')
        return redirect('reservation', reservation_id)
    else:

        return render(request, 'reservation.html', context)
