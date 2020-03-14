from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation

import re
date_validation = '^20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'


def index(request):
    reservations = Reservation.objects.order_by('number')
    reservations_status_query = Reservation.objects.values('status').distinct()
    status_list = []
    for i in reservations_status_query:
        status_list.append(i['status'])
    date_type = ['all_date, arrival, departure']

    if 'number' in request.GET:
        number = request.GET['number'].strip()
        if number:
            reservations = reservations.filter(number__icontains=number)

    if 'start_date' and 'end_date' in request.GET:
        start_date = request.GET['start_date'].strip()
        end_date = request.GET['end_date'].strip()
        date_type = request.GET['date_type']

        if re.match(date_validation, start_date) and re.match(date_validation, end_date):
            if start_date is not None and start_date != '' and end_date is not None and end_date != ''\
                    and date_type is not 'all_date':
                if date_type is None and date_type == '':
                    messages.info(request, 'Please choose date type')
                elif date_type == 'arrival':
                    reservations = reservations.filter(arrival__range=[start_date, end_date]).order_by('arrival')
                elif date_type == 'departure':
                    reservations = reservations.filter(departure__range=[start_date, end_date]).order_by('departure')
            if date_type == 'all_date':
                reservations = reservations.order_by('number')
        else:
            messages.error(request, 'Please enter correct date format (yyyy-mm-dd)')

    if 'status' in request.GET:
        status = request.GET['status']
        if status == 'all':
            reservations = reservations
        else:
            reservations = reservations.filter(status__iexact=status)

    paginator = Paginator(reservations, 500)
    page = request.GET.get('page')

    try:
        reservations = paginator.get_page(page)
    except(EmptyPage, InvalidPage):
        reservations = paginator.get_page(1)

    page_index = reservations.number - 1
    max_index = len(paginator.page_range)
    start_index = page_index - 10 if page_index >= 10 else 0
    end_index = page_index + 10 if page_index <= max_index - 10 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'reservations': reservations,
        'page_range': page_range,
        'values': request.GET,
        'status_list': status_list,
        'date_type': date_type,
    }
    print(context['values'])
    return render(request, 'index.html', context)


def reservation(request, reservation_id):

    reservation = get_object_or_404(Reservation, pk=reservation_id)

    context = {
        'reservation': reservation
    }
    if request.method == 'POST':
        if request.POST.get('arrival_date'):
            arrival_date = request.POST['arrival_date'].strip()
            if re.match(date_validation, arrival_date):
                reservation_to_update = Reservation.objects.get(id=reservation_id)
                reservation_to_update.arrival = arrival_date
                reservation_to_update.save()
            else:
                messages.error(request, 'Please enter correct date format (yyyy-mm-dd)')

        elif request.POST.get('departure_date'):
            departure_date = request.POST['departure_date'].strip()
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
