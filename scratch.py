import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_barcos.settings')
django.setup()

from core.models import Alerta
from core.services.sms_service import enviar_sms

a = Alerta.objects.last()
if a:
    print(f"Alerta: {a.mensagem}")
    print(f"Estado: {a.estado}")
    print(f"Numero: {a.numero_telefone}")
    res = enviar_sms(a.numero_telefone, a.mensagem)
    print(res)
else:
    print("Nenhum alerta encontrado.")
