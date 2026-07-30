import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme/tema.dart';

class RecuperarSenhaView extends StatefulWidget {
  const RecuperarSenhaView({super.key});

  @override
  State<RecuperarSenhaView> createState() => _RecuperarSenhaViewState();
}

class _RecuperarSenhaViewState extends State<RecuperarSenhaView> {
  final _emailController = TextEditingController();
  final _apiService = ApiService();
  bool _isLoading = false;

  Future<void> _submeter() async {
    final email = _emailController.text.trim();
    if (email.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor, introduza o seu e-mail.')),
      );
      return;
    }

    setState(() => _isLoading = true);
    
    final sucesso = await _apiService.recuperarSenha(email);
    
    if (mounted) {
      setState(() => _isLoading = false);
      
      if (sucesso) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('E-mail Enviado', style: TextStyle(color: TemaGeral.corPrincipal)),
            content: const Text('Se o e-mail existir no nosso sistema, receberá um link para redefinir a sua palavra-passe em breve.'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context); // Fechar dialog
                  Navigator.pop(context); // Voltar para o login
                },
                child: const Text('OK', style: TextStyle(color: TemaGeral.corPrincipal)),
              ),
            ],
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Ocorreu um erro. Verifique a ligação à internet e tente novamente.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: TemaGeral.corFundo,
      appBar: AppBar(
        title: const Text('Recuperar Senha', style: TextStyle(color: Colors.white)),
        backgroundColor: TemaGeral.corPrincipal,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(
                Icons.lock_reset,
                size: 80,
                color: TemaGeral.corPrincipal,
              ),
              const SizedBox(height: 24),
              const Text(
                'Esqueceu-se da sua palavra-passe?',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: TemaGeral.corTextoEscuro,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              const Text(
                'Introduza o endereço de e-mail associado à sua conta. Iremos enviar-lhe um link para poder redefinir a sua senha no nosso sistema.',
                style: TextStyle(
                  fontSize: 16,
                  color: TemaGeral.corTextoSecundario,
                  height: 1.5,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 40),
              TextField(
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: InputDecoration(
                  labelText: 'E-mail',
                  prefixIcon: const Icon(Icons.email, color: TemaGeral.corAcento),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: TemaGeral.corAcento, width: 2),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isLoading ? null : _submeter,
                style: ElevatedButton.styleFrom(
                  backgroundColor: TemaGeral.corSecundaria,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: _isLoading 
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                      )
                    : const Text(
                        'Enviar Link de Recuperação',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }
}
