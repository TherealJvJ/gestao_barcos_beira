import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/modelos.dart';
import '../services/api_service.dart';
import '../theme/tema.dart';

class EmbarcacaoDetalheView extends StatefulWidget {
  final Embarcacao embarcacao;

  const EmbarcacaoDetalheView({super.key, required this.embarcacao});

  @override
  State<EmbarcacaoDetalheView> createState() => _EmbarcacaoDetalheViewState();
}

class _EmbarcacaoDetalheViewState extends State<EmbarcacaoDetalheView> {
  final _apiService = ApiService();
  bool _isDownloading = false;

  void _baixarPDF(String urlSufixo, String nomeFicheiro) async {
    setState(() => _isDownloading = true);

    try {
      final token = await _apiService.getToken();
      // Anexar o token na query string para o backend autenticar o pedido via browser
      final url = '${ApiService.baseUrl}/$urlSufixo?token=$token';
      final uri = Uri.parse(url);

      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        throw Exception('Não foi possível abrir o navegador para download.');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Erro ao aceder ao documento PDF.'),
            backgroundColor: TemaMaritimo.vermelhoCoral,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isDownloading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final emb = widget.embarcacao;
    return Scaffold(
      appBar: AppBar(
        title: Text(emb.nome),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Ficha Técnica
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '📋 Ficha Técnica',
                      style: TextStyle(
                        fontFamily: 'Outfit',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: TemaMaritimo.azulProfundo,
                      ),
                    ),
                    const Divider(),
                    _buildFichaItem('Matrícula', emb.numeroMatricula),
                    _buildFichaItem('Tipo', emb.tipoEmbarcacao),
                    _buildFichaItem('Material', emb.material),
                    _buildFichaItem('Comprimento', '${emb.comprimento} m'),
                    _buildFichaItem('Potência Motor', '${emb.potenciaMotor} CV'),
                    _buildFichaItem('Ano de Construção', emb.anoConstrucao.toString()),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Documentos
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '📜 Documentos',
                      style: TextStyle(
                        fontFamily: 'Outfit',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: TemaMaritimo.azulProfundo,
                      ),
                    ),
                    const Divider(),
                    
                    // Título de Propriedade
                    ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: const Text('Título de Propriedade (Permanente)'),
                      subtitle: emb.titulo != null
                          ? Text('Nº ${emb.titulo!.numeroTitulo}\nEmitido em: ${emb.titulo!.dataEmissao}')
                          : const Text('Não emitido', style: TextStyle(color: Colors.red)),
                      trailing: emb.titulo != null
                          ? IconButton(
                              icon: const Icon(Icons.download, color: TemaMaritimo.azulOceano),
                              onPressed: _isDownloading
                                  ? null
                                  : () => _baixarPDF('titulos/${emb.titulo!.id}/pdf/', 'Titulo_${emb.titulo!.numeroTitulo}.pdf'),
                            )
                          : null,
                    ),
                    const Divider(),

                    // Licença de Navegação
                    ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: const Text('Licença de Navegação (Anual)'),
                      subtitle: emb.licencaActiva != null
                          ? Text('Nº ${emb.licencaActiva!.numeroLicenca}\nValidade: 31/12/${emb.licencaActiva!.anoReferencia}')
                          : const Text('Não emitida ou expirada', style: TextStyle(color: Colors.red)),
                      trailing: emb.licencaActiva != null
                          ? IconButton(
                              icon: const Icon(Icons.download, color: TemaMaritimo.azulOceano),
                              onPressed: _isDownloading
                                  ? null
                                  : () => _baixarPDF('licencas/${emb.licencaActiva!.id}/pdf/', 'Licenca_${emb.licencaActiva!.numeroLicenca}.pdf'),
                            )
                          : null,
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFichaItem(String rotulo, String valor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(rotulo, style: const TextStyle(fontWeight: FontWeight.bold)),
          Text(valor),
        ],
      ),
    );
  }
}
