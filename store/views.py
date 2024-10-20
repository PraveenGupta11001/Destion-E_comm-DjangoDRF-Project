from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Only admin users can create/update/delete products
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super(ProductViewSet, self).get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admins can see all orders
            return Order.objects.all()
        return Order.objects.filter(customer=user)

    def create(self, request, *args, **kwargs):
        total_price = 0
        products_data = request.data.get('products', [])
        order_items = []
        products_to_update = []

        for product_data in products_data:
            try:
                product = get_object_or_404(Product, id=product_data['id'])
                quantity = product_data['quantity']
                if product.stock >= quantity:
                    total_price += product.price * quantity
                    order_items.append({'product': product, 'quantity': quantity, 'price': product.price})
                    product.stock -= quantity  # Deduct stock
                    products_to_update.append(product)  # Save product later in bulk
                else:
                    return Response({'error': f'Insufficient stock for product {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create order
        order = Order.objects.create(customer=request.user, total_price=total_price)
        for item in order_items:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['price'])

        # Bulk update all products at once to optimize DB calls
        Product.objects.bulk_update(products_to_update, ['stock'])

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def cancel_order(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk, customer=request.user)
        if order.status == 'pending':
            order.status = 'canceled'
            order.save()

            # Restock products
            for item in order.orderitem_set.all():
                item.product.stock += item.quantity
                item.product.save()

            return Response({'status': 'Order canceled, items restocked'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order cannot be canceled'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAdminUser])
    def ship_order(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if order.status == 'pending':
            order.status = 'shipped'
            order.save()
            return Response({'status': 'Order shipped'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order cannot be shipped'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAdminUser])
    def deliver_order(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if order.status == 'shipped':
            order.status = 'delivered'
            order.save()
            return Response({'status': 'Order delivered'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order cannot be delivered'}, status=status.HTTP_400_BAD_REQUEST)
