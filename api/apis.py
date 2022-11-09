from re import search
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Merchant, Store, Item, Category
from .serializers import MerchantSerializer, StoreSerializer, ItemSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class MerchantViewset(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    http_method_names: list = ['get', 'put', 'patch']

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        return super().perform_update(serializer)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]


class StoreViewset(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['merchant', 'name']
    search_fields = ['name', 'merchant__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        return super().perform_update(serializer)


class CustomCategoryFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category', None)
        if category:
            return queryset.filter(category__name__icontains=category)
        parent = request.query_params.get('parent', None)
        if parent:
            return queryset.filter(parent=parent)
        parent__isnull = request.query_params.get('parent__isnull', None)
        if parent__isnull:
            return queryset.filter(parent__isnull=True)
        return queryset


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (CustomCategoryFilter, filters.SearchFilter)
    filterset_fields = ['name', 'parent']
    search_fields = ['name', 'parent__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        return super().perform_update(serializer)


class ItemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['store', 'store__merchant', 'category']
    search_fields = ['name', 'store__name',
                     'store__merchant__name', 'category__name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        return super().perform_update(serializer)
