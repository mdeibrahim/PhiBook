
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.views import APIView
from rest_framework.response import Response

class CreateSubscriptionView(APIView):
    def get(self, request):
        amount = request.data.get("amount")
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        address = request.data.get("address")
        city = request.data.get("city")

        settings = {
            'store_id': 'ummah68cb7095975ca',
            'store_pass': 'ummah68cb7095975ca@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(settings)
        post_body = {
            'total_amount': amount,
            'currency': "BDT",
            'tran_id': "12345",
            'success_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Kittyply_edit1.jpg/440px-Kittyply_edit1.jpg",
            'fail_url': "https://docs.stripe.com/payments/checkout/custom-success-page",
            'cancel_url': "https://docs.stripe.com/payments/checkout/custom-success-page",
            'emi_option': 0,
            'cus_name': name,
            'cus_email': email,
            'cus_phone': phone,
            'cus_add1': address,
            'cus_city': city,
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Test",
            'product_category': "Digital Products",
            'product_profile': "general"
        }
        response = sslcz.createSession(post_body)  
        gateway_url = response.get('GatewayPageURL')
        if gateway_url:
            return Response({
                'status': 'success',
                'gateway_url': gateway_url
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Could not create payment session',
                'response': response
            }, status=400)