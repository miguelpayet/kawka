from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from kawka.settings import MEDIA_ROOT
from kawka.settings import MEDIA_URL
from kawka.views.index_view import IndexView
from kawka.views.pedido_form_view import PedidoFormView
from kawka.views.pedido_mail_view import PedidoMailView
from kawka.views.calcula_precio import SumaView
from kawka.views.calcula_delivery import CalculaDeliveryView


urlpatterns = [path('admin/', admin.site.urls),
               path('', IndexView.as_view(), name='index'),
               path('delivery/', CalculaDeliveryView.as_view(), name='delivery'),
               path('email/<pedido>', PedidoMailView.as_view(), name='pedido'),
               path('pedido/', PedidoFormView.as_view(), name='pedido'),
               path('sumar/', SumaView.as_view(), name='sumar'),
               ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
