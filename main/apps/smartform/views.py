from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import smartform_suggestion, get_list_from_smartform_response
from .serializers import AddressSuggestionSerializer, AddressResponseSerializer


class AddressesSearchView(APIView):
    serializer_class = AddressSuggestionSerializer
    http_method_names = ['post']

    def get_serializer(self, data=dict):
        return self.serializer_class(data=data)

    @swagger_auto_schema(
        operation_description="address suggestion",
        responses={200: AddressResponseSerializer()})
    def post(self, request, *args, **kwargs) -> Response:
        data = request.data if request is not None else {}
        serializer = self.get_serializer(data)
        serializer.is_valid(raise_exception=True)
        street = serializer.validated_data.get('street', '')
        number = serializer.validated_data.get('number', '')
        city = serializer.validated_data.get('city', '')
        zip_code = serializer.validated_data.get('post_code', '')
        suggesting_field = serializer.validated_data.get('suggesting_field', None)

        resp = smartform_suggestion(street, number, city, zip_code, suggesting_field)
        result_lst = get_list_from_smartform_response(resp)
        return Response(data={
            "results": result_lst,
        })
