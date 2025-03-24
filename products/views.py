from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from .services import ProductService
from .models import Product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        product = self.get_object()
        updated_product = ProductService.update_product(product, serializer.validated_data)
        serializer.instance = updated_product

    def perform_destroy(self, instance):
        ProductService.delete_product(instance)
