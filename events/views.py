from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventTicketType, EventBooking, EventReview

def event_list(request):
    """Display all events"""
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')
    
    past_events = Event.objects.filter(
        date__lt=timezone.now()
    ).order_by('-date')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    
    return render(request, 'events/event_list.html', context)

def event_detail(request, event_id):
    """Display detailed information about a specific event"""
    event = get_object_or_404(Event, id=event_id)
    user_booking = None
    if request.user.is_authenticated:
        user_booking = EventBooking.objects.filter(
            user=request.user,
            event=event
        ).first()
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_booking': user_booking
    })

@login_required
def book_ticket(request, event_id, ticket_id):
    """Handle ticket booking"""
    if request.method != 'POST':
        return redirect('events:event_detail', event_id=event_id)
    
    event = get_object_or_404(Event, id=event_id)
    ticket_type = get_object_or_404(EventTicketType, id=ticket_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError("Quantity must be positive")
        
        if quantity > ticket_type.quantity_available:
            messages.error(request, "Not enough tickets available")
            return redirect('events:event_detail', event_id=event_id)
        
        # Calculate total amount
        total_amount = ticket_type.price * quantity
        
        # Create booking
        booking = EventBooking.objects.create(
            user=request.user,
            event=event,
            ticket_type=ticket_type,
            quantity=quantity,
            total_amount=total_amount
        )
        
        # Update available tickets
        ticket_type.quantity_available -= quantity
        ticket_type.save()
        
        messages.success(request, "Ticket booked successfully!")
        return redirect('events:my_bookings')  # You'll need to create this view
        
    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity specified")
        return redirect('events:event_detail', event_id=event_id)

@login_required
def my_bookings(request):
    """Display user's bookings"""
    bookings = EventBooking.objects.filter(
        user=request.user
    ).order_by('-booking_date')
    
    return render(request, 'events/my_bookings.html', {
        'bookings': bookings
    })

@login_required
def add_review(request, event_id):
    """Add a review for an event"""
    if request.method != 'POST':
        return redirect('events:event_detail', event_id=event_id)
    
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user has attended the event
    has_booking = EventBooking.objects.filter(
        user=request.user,
        event=event,
        payment_status='COMPLETED'
    ).exists()
    
    if not has_booking:
        messages.error(request, "You can only review events you've attended")
        return redirect('events:event_detail', event_id=event_id)
    
    try:
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '').strip()
        
        if not (1 <= rating <= 5):
            raise ValueError("Invalid rating")
        
        if not comment:
            messages.error(request, "Please provide a comment")
            return redirect('events:event_detail', event_id=event_id)
        
        EventReview.objects.create(
            event=event,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, "Review added successfully!")
        
    except (ValueError, TypeError):
        messages.error(request, "Invalid rating value")
    
    return redirect('events:event_detail', event_id=event_id)

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(EventBooking, id=booking_id, user=request.user)
    
    # Only allow cancellation if event hasn't happened yet
    if booking.event.date < timezone.now():
        booking.payment_status = 'CANCELLED'
        booking.save()
        
        # Return tickets to available pool
        ticket_type = booking.ticket_type
        ticket_type.quantity_available += booking.quantity
        ticket_type.save()
        
        messages.success(request, "Booking cancelled successfully")
    else:
        messages.error(request, "Cannot cancel past events")
    
    return redirect('events:my_bookings')

@login_required
def create_event(request):
    """Create a new event"""
    if request.method == 'POST':
        try:
            # Get basic event data
            event = Event.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                date=request.POST['date'],
                location=request.POST['location'],
                location_map_link=request.POST.get('location_map_link', ''),
                organizer=request.user,
                organizer_website=request.POST.get('organizer_website', ''),
                organizer_phone=request.POST.get('organizer_phone', ''),
                agenda=request.POST.get('agenda', ''),
                speakers=request.POST.get('speakers', ''),
                faq=request.POST.get('faq', ''),
                terms_conditions=request.POST.get('terms_conditions', '')
            )

            # Handle main image
            if 'main_image' in request.FILES:
                event.main_image = request.FILES['main_image']
                event.save()

            # Create ticket types
            ticket_types = request.POST.getlist('ticket_type_name[]')
            prices = request.POST.getlist('ticket_type_price[]')
            quantities = request.POST.getlist('ticket_type_quantity[]')
            descriptions = request.POST.getlist('ticket_type_description[]')

            for i in range(len(ticket_types)):
                EventTicketType.objects.create(
                    event=event,
                    name=ticket_types[i],
                    price=prices[i],
                    quantity_available=quantities[i],
                    description=descriptions[i]
                )

            messages.success(request, "Event created successfully!")
            return redirect('events:event_detail', event_id=event.id)

        except Exception as e:
            messages.error(request, f"Error creating event: {str(e)}")
            return render(request, 'events/create_event.html')

    return render(request, 'events/create_event.html') 