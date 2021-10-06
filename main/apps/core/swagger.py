from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


path_id_param_int = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, type=openapi.TYPE_INTEGER)]
)

path_id_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("id", openapi.IN_PATH, type=openapi.TYPE_STRING)]
)

path_role_param_str = swagger_auto_schema(
    manual_parameters=[openapi.Parameter("role", openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)],
)
