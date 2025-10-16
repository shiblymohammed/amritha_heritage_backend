from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import DailySpecial
from .serializers import DailySpecialSerializer, DailySpecialCreateSerializer

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings




class DailySpecialViewSet(viewsets.ModelViewSet):
    queryset = DailySpecial.objects.all()
    serializer_class = DailySpecialSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DailySpecialCreateSerializer
        return DailySpecialSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active daily specials"""
        active_specials = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_specials, many=True)
        return Response({
            'results': serializer.data,
            'count': active_specials.count()
        })

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle the is_active status of a daily special"""
        special = self.get_object()
        special.is_active = not special.is_active
        special.save()
        serializer = self.get_serializer(special)
        return Response({
            'message': f"Daily special {'activated' if special.is_active else 'deactivated'} successfully",
            'data': serializer.data
        })





#emaill sending logic


@csrf_exempt # Important for APIs called from a separate frontend
def make_reservation_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
        print(f"Received data: {data}")  # Debug log
        
        # Handle both formats - direct data or nested reservation
        if 'reservation' in data:
            # Old format with nested reservation
            reservation = data.get('reservation', {})
            items = data.get('items', [])
            total_amount = data.get('totalAmount', 0)
        else:
            # New format with direct data
            reservation = data
            items = []
            total_amount = 0

        # --- Send Email Notification ---
        subject = f"New Table Reservation: {reservation.get('name')} on {reservation.get('date')}"
        
        # You can use a simple text message or an HTML template
        html_message = render_to_string('new_reservation.html', {
            'reservation': reservation,
            'items': items,
            'total_amount': total_amount,
        })
        plain_message = f"New reservation from {reservation.get('name')}. Please check the admin dashboard."

        send_mail(
            subject=subject,
            message=plain_message, # Fallback for email clients that don't support HTML
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['shibilymohammed75@gmail.com'], # Your admin email
            html_message=html_message,
            fail_silently=False,  # Now that email is working, we can catch errors
        )

        return JsonResponse({'message': 'Reservation successful and notification sent.'}, status=200)

    except Exception as e:
        # Log the error for debugging
        print(f"Error in make_reservation_api: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback
        return JsonResponse({'error': 'Failed to process reservation.'}, status=500)