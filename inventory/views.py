from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from core.utils import IsOwnerOrManager
from companys.models import Company
from .models import InventoryItem
from .serializers import InventoryItemSerializer

@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrManager])
def inventory_list_create(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)

    if request.method == "GET":
        category = request.query_params.get("category")
        queryset = InventoryItem.objects.filter(company=company)

        if category:
            queryset = queryset.filter(category=category)

        serializer = InventoryItemSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data.copy()
        data["company"] = company.id

        serializer = InventoryItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrManager])
def inventory_detail(request, company_slug, pk):
    company = get_object_or_404(Company, slug=company_slug)
    item = get_object_or_404(InventoryItem, pk=pk, company=company)

    if request.method == "GET":
        serializer = InventoryItemSerializer(item)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = InventoryItemSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
