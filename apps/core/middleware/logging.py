import time
import logging
import uuid
from django.utils.deprecation import MiddlewareMixin
from apps.core.logging.correlation import set_correlation_id

logger = logging.getLogger('apps.api')

class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
        set_correlation_id(correlation_id)
        request.correlation_id = correlation_id

    def process_response(self, request, response):
        if hasattr(request, 'correlation_id'):
            response['X-Correlation-ID'] = request.correlation_id
        if not hasattr(request, 'start_time'):
            return response

        duration = time.time() - request.start_time

        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        user_id = request.user.id if request.user.is_authenticated else "Anonymous"

        log_data = {
            'method': request.method,
            'path': request.get_full_path(),
            'status_code': response.status_code,
            'duration': f"{duration:.3f}s",
            'ip': ip,
            'user_id': user_id,
        }

        # Log only non-200 or slow requests at INFO level, others at DEBUG if needed
        # Or just log all API requests at INFO level as requested
        if request.path.startswith('/api/'):
            msg = f"{log_data['method']} {log_data['path']} {log_data['status_code']} ({log_data['duration']}) IP: {log_data['ip']} User: {log_data['user_id']}"

            if response.status_code >= 500:
                logger.error(msg, extra={'request_data': log_data})
            elif response.status_code >= 400:
                logger.warning(msg, extra={'request_data': log_data})
            else:
                logger.info(msg, extra={'request_data': log_data})

        return response

    def process_exception(self, request, exception):
        # This will be caught by Django's default handler and logged to 'django.request'
        # which we already capture in our config.
        pass
