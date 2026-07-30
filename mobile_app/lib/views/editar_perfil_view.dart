import 'package:flutter/material.dart';
import '../models/modelos.dart';
import '../services/api_service.dart';
import '../theme/tema.dart';

class EditarPerfilView extends StatefulWidget {
  const EditarPerfilView({super.key});

  @override
  State<EditarPerfilView> createState() => _EditarPerfilViewState();
}

class _EditarPerfilViewState extends State<EditarPerfilView> {
  final _formKey = GlobalKey<FormState>();
  final _apiService = ApiService();
  
  bool _isLoading = true;
  bool _isSaving = false;
  
  Usuario? _usuario;
  
  final _nomeController = TextEditingController();
  final _telefoneController = TextEditingController();
  final _documentoController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _carregarPerfil();
  }

  Future<void> _carregarPerfil() async {
    setState(() => _isLoading = true);
    final perfil = await _apiService.getPerfil();
    if (perfil != null) {
      setState(() {
        _usuario = perfil;
        _nomeController.text = perfil.nomeCompleto;
        _telefoneController.text = perfil.telefone;
        _documentoController.text = perfil.numeroDocumento;
        _isLoading = false;
      });
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Erro ao carregar o perfil')),
        );
        Navigator.pop(context);
      }
    }
  }

  Future<void> _salvarPerfil() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSaving = true);

    final dados = {
      'nome_completo': _nomeController.text.trim(),
      'telefone': _telefoneController.text.trim(),
      'numero_documento': _documentoController.text.trim(),
    };

    final sucesso = await _apiService.atualizarPerfil(dados);

    setState(() => _isSaving = false);

    if (sucesso && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Perfil atualizado com sucesso!'),
          backgroundColor: TemaMaritimo.verdeMar,
        ),
      );
      Navigator.pop(context, true); // Retorna true para sinalizar que houve atualização
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Falha ao atualizar o perfil. Verifique a ligação.'),
          backgroundColor: TemaMaritimo.vermelhoCoral,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Editar Perfil'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Icon(
                      Icons.account_circle,
                      size: 80,
                      color: TemaMaritimo.azulOceano,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      _usuario?.email ?? '',
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 16,
                        color: TemaMaritimo.cinzaRede,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 32),
                    
                    TextFormField(
                      controller: _nomeController,
                      decoration: const InputDecoration(
                        labelText: 'Nome Completo',
                        prefixIcon: Icon(Icons.person),
                      ),
                      validator: (value) =>
                          value == null || value.isEmpty ? 'Nome é obrigatório' : null,
                    ),
                    const SizedBox(height: 16),
                    
                    TextFormField(
                      controller: _telefoneController,
                      decoration: const InputDecoration(
                        labelText: 'Número de Telefone',
                        prefixIcon: Icon(Icons.phone),
                      ),
                      keyboardType: TextInputType.phone,
                      validator: (value) =>
                          value == null || value.isEmpty ? 'Telefone é obrigatório' : null,
                    ),
                    const SizedBox(height: 16),
                    
                    TextFormField(
                      controller: _documentoController,
                      decoration: const InputDecoration(
                        labelText: 'Nº de Documento (BI/Passaporte)',
                        prefixIcon: Icon(Icons.badge),
                      ),
                    ),
                    const SizedBox(height: 32),
                    
                    ElevatedButton(
                      onPressed: _isSaving ? null : _salvarPerfil,
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: _isSaving
                          ? const CircularProgressIndicator(color: Colors.white)
                          : const Text(
                              'Guardar Alterações',
                              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
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
    _nomeController.dispose();
    _telefoneController.dispose();
    _documentoController.dispose();
    super.dispose();
  }
}
