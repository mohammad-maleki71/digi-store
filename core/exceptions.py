from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        logger.exception("Unexpected exception", exc_info=exc)

        return Response(
            {
                "success": False,
                "status_code": 500,
                "errors": {
                    "detail": "Internal Server Error"
                }
            },
            status=500,
        )

    response.data = {
        "success": False,
        "status_code": response.status_code,
        "errors": response.data,
    }

    return response

