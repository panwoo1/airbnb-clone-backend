from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking
from bookings.serializers import (
    CreateExperienceBookingSerializer,
    PublicBookingSerializer,
)
from categories.models import Category

from . import models, serializers


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = models.Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            all_experiences,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            perk_pks = request.data.get("perks")

            if not category_pk:
                raise ParseError("Category is requried.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.object.get(pk=category_pk):
                    raise ParseError("The category kind should be 'experience'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    if perk_pks:
                        for perk_pk in perk_pks:
                            perk = models.Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)
            except Exception:
                raise ParseError("Perk not found.")
            serializer = serializers.ExperienceDetailSerializer(
                experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):

        experience = self.get_object(pk)

        if experience.host != request.user:
            raise PermissionDenied

        serializer = ExperienceDetail(
            experience,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            category_pk = request.data.get("category")
            perk_pks = request.data.get("perks")
            try:
                category = Category.objects.get(pk=category_pk)
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()
                    if perk_pks:
                        experience.perks.clear()
                        for perk_pk in perk_pks:
                            perk = models.Perk.objects.get(pk=perk_pk)
                            experience.perks.add(perk)
                        return Response(
                            serializers.ExperienceDetailSerializer(experience).data
                        )
            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):

        experience = self.get_object(pk)

        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).data()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Perks(APIView):
    def get(self, request):
        all_perks = models.Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return models.Perk.objects.get(pk=pk)
        except models.Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                serializers.PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
