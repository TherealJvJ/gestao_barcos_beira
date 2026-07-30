import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/modelos.dart';
import '../services/api_service.dart';
import '../theme/tema.dart';
import 'embarcacao_detalhe_view.dart';
import 'login_view.dart';
import 'nova_embarcacao_view.dart';
import 'alertas_view.dart';
import 'editar_perfil_view.dart';

class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  State<DashboardView> createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  final _apiService = ApiService();
  String _nomeUsuario = 'Pescador';
  String _tipoUsuario = 'pescador';
  List<Embarcacao> _embarcacoes = [];
  List<AlertaModel> _alertas = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _carregarDados();
  }

  Future<void> _carregarDados() async {
    setState(() => _isLoading = true);
    
    const storage = FlutterSecureStorage();
    final nome = await storage.read(key: 'user_nome') ?? 'Pescador';
    final tipo = await storage.read(key: 'user_tipo') ?? 'pescador';
    
    final barcos = await _apiService.getEmbarcacoes();
    final avisos = await _apiService.getAlertas();

    setState(() {
      _nomeUsuario = nome;
      _tipoUsuario = tipo;
      _embarcacoes = barcos;
      _alertas = avisos;
      _isLoading = false;
    });
  }

  void _sair() async {
    await _apiService.logout();
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginView()),
      );
    }
  }

  void _abrirPerfil() async {
    final atualizado = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const EditarPerfilView()),
    );
    if (atualizado == true) {
      _carregarDados();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('⚓ INTRANSMAR'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            tooltip: 'Perfil',
            onPressed: _abrirPerfil,
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _sair,
          ),
        ],
      ),
      floatingActionButton: _tipoUsuario == 'pescador'
          ? FloatingActionButton.extended(
              onPressed: () async {
                final resultado = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const NovaEmbarcacaoView()),
                );
                // Se a nova embarcação foi submetida com sucesso, recarrega os dados
                if (resultado == true) {
                  _carregarDados();
                }
              },
              backgroundColor: TemaMaritimo.laranjaCoral,
              icon: const Icon(Icons.add),
              label: const Text('Nova Embarcação'),
            )
          : null,
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: () async => _carregarDados(),
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Olá, $_nomeUsuario! 🎣',
                      style: const TextStyle(
                        fontFamily: 'Outfit',
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: TemaMaritimo.azulProfundo,
                      ),
                    ),
                                        const SizedBox(height: 4),
                    const Text('Gestão de Barcos — Beira'),
                    const SizedBox(height: 24),

                    // Grid de estatísticas simples
                    Row(
                      children: [
                        Expanded(
                          child: _buildStatCard(
                            'Embarcações',
                            _embarcacoes.length.toString(),
                            Icons.directions_boat,
                            TemaMaritimo.azulOceano,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: GestureDetector(
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => AlertasView(alertas: _alertas),
                                ),
                              );
                            },
                            child: _buildStatCard(
                              'Alertas',
                              _alertas.length.toString(),
                              Icons.notifications,
                              TemaMaritimo.laranjaCoral,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),

                    const Text(
                      'Minhas Embarcações',
                      style: TextStyle(
                        fontFamily: 'Outfit',
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: TemaMaritimo.azulProfundo,
                      ),
                    ),
                    const SizedBox(height: 12),

                    _embarcacoes.isEmpty
                        ? _buildEmptyState('Nenhuma embarcação encontrada')
                        : ListView.builder(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            itemCount: _embarcacoes.length,
                            itemBuilder: (context, index) {
                              final emb = _embarcacoes[index];
                              return Card(
                                margin: const EdgeInsets.only(bottom: 12),
                                child: ListTile(
                                  leading: const Icon(
                                    Icons.directions_boat,
                                    color: TemaMaritimo.azulOceano,
                                    size: 36,
                                  ),
                                  title: Text(
                                    emb.nome,
                                    style: const TextStyle(fontWeight: FontWeight.bold),
                                  ),
                                  subtitle: Text(
                                    '${emb.numeroMatricula} · ${emb.tipoEmbarcacao}',
                                  ),
                                  trailing: _buildBadge(emb.estadoRegisto),
                                  onTap: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => EmbarcacaoDetalheView(embarcacao: emb),
                                      ),
                                    );
                                  },
                                ),
                              );
                            },
                          ),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildStatCard(String titulo, String valor, IconData icone, Color cor) {
    return Card(
      child: Container(
        padding: const EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          border: Border(left: BorderSide(color: cor, width: 4)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icone, color: cor, size: 28),
            const SizedBox(height: 8),
            Text(
              valor,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: TemaMaritimo.azulProfundo,
              ),
            ),
            Text(titulo, style: const TextStyle(fontSize: 12, color: TemaMaritimo.cinzaRede)),
          ],
        ),
      ),
    );
  }

  Widget _buildBadge(String estado) {
    Color bg = TemaMaritimo.laranjaCoral.withOpacity(0.15);
    Color texto = TemaMaritimo.laranjaCoral;

    if (estado == 'aprovado' || estado == 'aprovada') {
      bg = TemaMaritimo.verdeMar.withOpacity(0.15);
      texto = TemaMaritimo.verdeMar;
    } else if (estado == 'rejeitado' || estado == 'rejeitada') {
      bg = TemaMaritimo.vermelhoCoral.withOpacity(0.15);
      texto = TemaMaritimo.vermelhoCoral;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        estado.toUpperCase(),
        style: TextStyle(
          color: texto,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  Widget _buildEmptyState(String mensagem) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 40),
      child: Column(
        children: [
          const Icon(Icons.info_outline, size: 48, color: TemaMaritimo.cinzaRede),
          const SizedBox(height: 8),
          Text(mensagem, style: const TextStyle(color: TemaMaritimo.cinzaRede)),
        ],
      ),
    );
  }
}
