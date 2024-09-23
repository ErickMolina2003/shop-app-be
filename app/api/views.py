from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Product, Purchase
from .serializers import ProductSerializer, PurchaseSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def handleData(request):
    if request.method == 'GET':
        items = Product.objects.all()
        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()    
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def handlePurchase(request):
    if request.method == 'GET':
        items = Purchase.objects.all()
        serializer = PurchaseSerializer(items, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data
        purchases = []
        
        for item in data:
            product_id = item['product']['id']
            amount_to_buy = item['amountToBuy']
            try:
                product = Product.objects.get(id=product_id)
                if product.amount >= amount_to_buy:
                    product.amount -= amount_to_buy
                    product.save()

                    total_price = product.price * amount_to_buy
                    purchase = Purchase.objects.create(product=product, amount=amount_to_buy, total_price=total_price)
                    purchases.append(purchase)
                else:
                    return Response({'error': f'Not enough stock for {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {product_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Purchase registered successfully', 'purchases': [str(p) for p in purchases], 'status': status.HTTP_200_OK }, status=status.HTTP_200_OK)  
    