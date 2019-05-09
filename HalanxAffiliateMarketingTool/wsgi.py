from django.core.wsgi import get_wsgi_application

from utility.environments import set_settings_module

set_settings_module()
application = get_wsgi_application()
