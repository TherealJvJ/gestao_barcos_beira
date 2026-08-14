import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme/tema.dart';

class NovaEmbarcacaoView extends StatefulWidget {
  const NovaEmbarcacaoView({super.key});

  @override
  State<NovaEmbarcacaoView> createState() => _NovaEmbarcacaoViewState();
}

class _NovaEmbarcacaoViewState extends State<NovaEmbarcacaoView> {
  final _formKey = GlobalKey<FormState>();
  final _apiService = ApiService();
  bool _isLoading = false;

  final _nomeController = TextEditingController();
  final _matriculaController = TextEditingController();
  final _comprimentoController = TextEditingController();
  final _potenciaController = TextEditingController();
  final _anoController = TextEditingController();
  final _obsController = TextEditingController();

  String _tipoEmbarcacao = 'canoa';
  String _material = 'madeira';

  void _submeterFormulario() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final dados = {
      'nome': _nomeController.text.trim(),
      'numero_matricula': _matriculaController.text.trim(),
      'tipo_embarcacao': _tipoEmbarcacao,
      'comprimento': double.parse(_comprimentoController.text.trim()),
      'potencia_motor': int.parse(_potenciaController.text.trim()),
      'ano_construcao': int.parse(_anoController.text.trim()),
      'material': _material,
      'observacoes': _obsController.text.trim(),
    };

    final sucesso = await _apiService.solicitarRegistoEmbarcacao(dados);

    setState(() => _isLoading = false);

    if (sucesso) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Embarcação registada com sucesso! Aguarda aprovação.'),
            backgroundColor: TemaMaritimo.verdeMar,
          ),
        );
        Navigator.pop(context, true); // Retorna 'true' para indicar que deve atualizar a lista
      }
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erro ao registar embarcação. Verifique os dados (A matrícula deve ser única).'),
            backgroundColor: TemaMaritimo.vermelhoCoral,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Registar Nova Embarcação'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: const [
                            Icon(Icons.assignment_outlined, color: TemaMaritimo.azulOceano, size: 20),
                            SizedBox(width: 8),
                            Text(
                              'Dados da Embarcação',
                              style: TextStyle(
                                fontFamily: 'Outfit',
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: TemaMaritimo.azulProfundo,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        const Text(
                          'Preencha os dados abaixo para solicitar o registo no INTRANSMAR. '
                          'Após a submissão, o processo ficará Pendente para avaliação.',
                          style: TextStyle(color: TemaMaritimo.cinzaRede),
                        ),
                        const Divider(height: 32),

                        // Nome
                        TextFormField(
                          controller: _nomeController,
                          decoration: const InputDecoration(labelText: 'Nome da Embarcação *'),
                          validator: (v) => v!.isEmpty ? 'Campo obrigatório' : null,
                        ),
                        const SizedBox(height: 16),

                        // Matrícula
                        TextFormField(
                          controller: _matriculaController,
                          decoration: const InputDecoration(labelText: 'Nº de Matrícula *'),
                          validator: (v) => v!.isEmpty ? 'Campo obrigatório' : null,
                        ),
                        const SizedBox(height: 16),

                        // Tipo de Embarcação
                        DropdownButtonFormField<String>(
                          value: _tipoEmbarcacao,
                          decoration: const InputDecoration(labelText: 'Tipo de Embarcação *'),
                          items: const [
                            DropdownMenuItem(value: 'canoa', child: Text('Canoa')),
                            DropdownMenuItem(value: 'canoa_motor', child: Text('Canoa a Motor')),
                            DropdownMenuItem(value: 'lancha', child: Text('Lancha')),
                          ],
                          onChanged: (val) => setState(() => _tipoEmbarcacao = val!),
                        ),
                        const SizedBox(height: 16),

                        // Material
                        DropdownButtonFormField<String>(
                          value: _material,
                          decoration: const InputDecoration(labelText: 'Material *'),
                          items: const [
                            DropdownMenuItem(value: 'madeira', child: Text('Madeira')),
                            DropdownMenuItem(value: 'fibra', child: Text('Fibra de Vidro')),
                            DropdownMenuItem(value: 'aluminio', child: Text('Alumínio')),
                          ],
                          onChanged: (val) => setState(() => _material = val!),
                        ),
                        const SizedBox(height: 16),

                        // Row: Comprimento e Potência
                        Row(
                          children: [
                            Expanded(
                              child: TextFormField(
                                controller: _comprimentoController,
                                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                                decoration: const InputDecoration(labelText: 'Comprimento (m) *'),
                                validator: (v) {
                                  if (v!.isEmpty) return 'Obrigatório';
                                  final num = double.tryParse(v);
                                  if (num == null) return 'Inválido';
                                  if (num > 10) return 'Máximo 10m';
                                  return null;
                                },
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: TextFormField(
                                controller: _potenciaController,
                                keyboardType: TextInputType.number,
                                decoration: const InputDecoration(labelText: 'Potência (CV) *'),
                                validator: (v) {
                                  if (v!.isEmpty) return 'Obrigatório (0 se s/ motor)';
                                  final num = int.tryParse(v);
                                  if (num == null) return 'Inválido';
                                  if (num > 100) return 'Máximo 100CV';
                                  return null;
                                },
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),

                        // Ano Construção
                        TextFormField(
                          controller: _anoController,
                          keyboardType: TextInputType.number,
                          decoration: const InputDecoration(labelText: 'Ano de Construção *'),
                          validator: (v) {
                            if (v!.isEmpty) return 'Obrigatório';
                            final ano = int.tryParse(v);
                            if (ano == null || ano < 1900 || ano > DateTime.now().year) return 'Ano inválido';
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),

                        // Observações
                        TextFormField(
                          controller: _obsController,
                          maxLines: 3,
                          decoration: const InputDecoration(
                            labelText: 'Observações (Opcional)',
                            alignLabelWithHint: true,
                          ),
                        ),
                        const SizedBox(height: 32),

                        // Botão Submeter
                        SizedBox(
                          width: double.infinity,
                          height: 50,
                          child: ElevatedButton.icon(
                            onPressed: _submeterFormulario,
                            icon: const Icon(Icons.send),
                            label: const Text('Submeter Solicitação'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: TemaMaritimo.azulOceano,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
    );
  }
}
