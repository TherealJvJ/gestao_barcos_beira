"""Middlewares do sistema gestao_barcos."""

class NeverCacheMiddleware:
    """
    Middleware que adiciona cabeçalhos HTTP para impedir que o browser
    guarde em cache as páginas visitadas por utilizadores autenticados.
    Isto impede que o utilizador consiga voltar para a página anterior
    usando o botão 'Voltar' do browser após fazer logout.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        content_type = response.get('Content-Type', '')
        # Impedir o cache em todas as páginas HTML para evitar problemas de CSRF e navegação pós-logout
        if 'text/html' in content_type:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
