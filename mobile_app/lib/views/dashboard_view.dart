import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/modelos.dart';
import '../services/api_service.dart';
import '../theme/tema.dart';
import 'embarcacao_detalhe_view.dart';
import 'login_view.dart';
import 'nova_embarcacao_view.dart';

class DashboardView extends StatefulWidget {
  const DashboardView({super.key});

  @override
  State<DashboardView> createState() => _DashboardViewState();
}

class _DashboardViewState extends State<DashboardView> {
  final _apiService = ApiService();
  int _currentIndex = 0;
  bool _isLoading = true;

  // Dados partilhados
  String _nomeUsuario = 'Pescador';
  String _tipoUsuario = 'pescador';
  List<Embarcacao> _embarcacoes = [];
  List<AlertaModel> _alertas = [];
  Usuario? _perfilUsuario;

  // Controllers para o formulário de perfil
  final _formKey = GlobalKey<FormState>();
  final _nomeController = TextEditingController();
  final _telefoneController = TextEditingController();
  final _documentoController = TextEditingController();
  bool _isSavingPerfil = false;

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
    final perfil = await _apiService.getPerfil();

    setState(() {
      _nomeUsuario = nome;
      _tipoUsuario = tipo;
      _embarcacoes = barcos;
      _alertas = avisos;
      _perfilUsuario = perfil;
      
      if (perfil != null) {
        _nomeController.text = perfil.nomeCompleto;
        _telefoneController.text = perfil.telefone;
        _documentoController.text = perfil.numeroDocumento;
      }
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

  Future<void> _salvarPerfil() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSavingPerfil = true);

    final dados = {
      'nome_completo': _nomeController.text.trim(),
      'telefone': _telefoneController.text.trim(),
      'numero_documento': _documentoController.text.trim(),
    };

    final sucesso = await _apiService.atualizarPerfil(dados);

    setState(() => _isSavingPerfil = false);

    if (sucesso && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Perfil atualizado com sucesso!'),
          backgroundColor: TemaMaritimo.verdeMar,
        ),
      );
      _carregarDados(); // Recarrega para atualizar a saudação no painel
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
    if (_isLoading) {
      return const Scaffold(
        backgroundColor: TemaMaritimo.areiaClara,
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      backgroundColor: TemaMaritimo.areiaClara,
      appBar: AppBar(
        title: Text(_getAppBarTitle()),
        automaticallyImplyLeading: false,
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: [
          _buildPainelTab(),
          _buildAlertasTab(),
          _buildPerfilTab(),
        ],
      ),
      floatingActionButton: _currentIndex == 0 && _tipoUsuario == 'pescador'
          ? FloatingActionButton.extended(
              onPressed: () async {
                final resultado = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const NovaEmbarcacaoView()),
                );
                if (resultado == true) {
                  _carregarDados();
                }
              },
              backgroundColor: TemaMaritimo.laranjaCoral,
              icon: const Icon(Icons.add, color: Colors.white),
              label: const Text(
                'Nova Embarcação',
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
              ),
            )
          : null,
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          boxShadow: [
            BoxShadow(color: Colors.black26, blurRadius: 10, spreadRadius: 1),
          ],
        ),
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (index) => setState(() => _currentIndex = index),
          backgroundColor: TemaMaritimo.azulProfundo,
          selectedItemColor: TemaMaritimo.laranjaCoral,
          unselectedItemColor: Colors.white70,
          selectedLabelStyle: const TextStyle(fontWeight: FontWeight.bold),
          showUnselectedLabels: true,
          type: BottomNavigationBarType.fixed,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.directions_boat_outlined),
              activeIcon: Icon(Icons.directions_boat),
              label: 'Painel',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.notifications_outlined),
              activeIcon: Icon(Icons.notifications),
              label: 'Alertas',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person_outline),
              activeIcon: Icon(Icons.person),
              label: 'Perfil',
            ),
          ],
        ),
      ),
    );
  }

  String _getAppBarTitle() {
    switch (_currentIndex) {
      case 0:
        return 'INTRANSMAR Beira';
      case 1:
        return 'Notificações e Avisos';
      case 2:
        return 'Perfil do Pescador';
      default:
        return 'INTRANSMAR';
    }
  }

  // --- ABA 1: PAINEL ---
  Widget _buildPainelTab() {
    return RefreshIndicator(
      onRefresh: () async => _carregarDados(),
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Olá, $_nomeUsuario',
              style: const TextStyle(
                fontFamily: 'Outfit',
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: TemaMaritimo.azulProfundo,
              ),
            ),
            const SizedBox(height: 4),
            const Text(
              'Gestão de Embarcações - Beira',
              style: TextStyle(color: TemaMaritimo.cinzaRede, fontSize: 14),
            ),
            const SizedBox(height: 24),

            // Grid de estatísticas
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
                    onTap: () => setState(() => _currentIndex = 1),
                    child: _buildStatCard(
                      'Alertas Ativos',
                      _alertas.length.toString(),
                      Icons.notifications,
                      TemaMaritimo.laranjaCoral,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 28),

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
                ? _buildEmptyState('Nenhuma embarcação cadastrada no sistema.')
                : ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: _embarcacoes.length,
                    itemBuilder: (context, index) {
                      final emb = _embarcacoes[index];
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        elevation: 1,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: ListTile(
                          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          leading: const CircleAvatar(
                            backgroundColor: Color(0xFFE2F0F5),
                            child: Icon(Icons.directions_boat, color: TemaMaritimo.azulOceano),
                          ),
                          title: Text(
                            emb.nome,
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                          ),
                          subtitle: Padding(
                            padding: const EdgeInsets.only(top: 4.0),
                            child: Text(
                              'Matrícula: ${emb.numeroMatricula}\nTipo: ${emb.tipoEmbarcacao}',
                              style: const TextStyle(height: 1.3),
                            ),
                          ),
                          trailing: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.end,
                            children: [
                              _buildBadge(emb.estadoRegisto),
                              const SizedBox(height: 4),
                              const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
                            ],
                          ),
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
    );
  }

  Widget _buildStatCard(String titulo, String valor, IconData icone, Color cor) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Container(
        padding: const EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8),
          border: Border(left: BorderSide(color: cor, width: 4)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icone, color: cor, size: 28),
            const SizedBox(height: 12),
            Text(
              valor,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: TemaMaritimo.azulProfundo,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              titulo,
              style: const TextStyle(fontSize: 12, color: TemaMaritimo.cinzaRede, fontWeight: FontWeight.w500),
            ),
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
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        estado.toUpperCase(),
        style: TextStyle(
          color: texto,
          fontSize: 10,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  Widget _buildEmptyState(String mensagem) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 40),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          const Icon(Icons.info_outline, size: 40, color: TemaMaritimo.cinzaRede),
          const SizedBox(height: 12),
          Text(
            mensagem,
            style: const TextStyle(color: TemaMaritimo.cinzaRede, fontWeight: FontWeight.w500),
          ),
        ],
      ),
    );
  }

  // --- ABA 2: ALERTAS ---
  Widget _buildAlertasTab() {
    return RefreshIndicator(
      onRefresh: () async => _carregarDados(),
      child: _alertas.isEmpty
          ? SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              child: Container(
                height: MediaQuery.of(context).size.height * 0.7,
                alignment: Alignment.center,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.notifications_off_outlined, size: 56, color: TemaMaritimo.cinzaRede),
                    SizedBox(height: 16),
                    Text(
                      'Não tem notificações ou alertas no momento.',
                      style: TextStyle(color: TemaMaritimo.cinzaRede, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(20.0),
              itemCount: _alertas.length,
              itemBuilder: (context, index) {
                final alerta = _alertas[index];
                
                IconData icone = Icons.info_outline;
                Color cor = TemaMaritimo.azulOceano;
                
                if (alerta.tipoAlerta.contains('licenca') || alerta.tipoAlerta.contains('titulo')) {
                  icone = Icons.verified_outlined;
                  cor = TemaMaritimo.verdeMar;
                } else if (alerta.tipoAlerta.contains('expirando') || alerta.tipoAlerta.contains('vistoria')) {
                  icone = Icons.warning_amber_outlined;
                  cor = TemaMaritimo.laranjaCoral;
                } else if (alerta.tipoAlerta.contains('rejeitada') || alerta.tipoAlerta.contains('falhou')) {
                  icone = Icons.error_outline_outlined;
                  cor = TemaMaritimo.vermelhoCoral;
                }

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  elevation: 1,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Container(
                    decoration: BoxDecoration(
                      border: Border(left: BorderSide(color: cor, width: 4)),
                    ),
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(icone, color: cor, size: 20),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                alerta.tipoDisplay,
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 15,
                                  color: TemaMaritimo.azulProfundo,
                                ),
                              ),
                            ),
                            Text(
                              alerta.dataCriacao.isNotEmpty
                                  ? alerta.dataCriacao.split('T')[0] 
                                  : '',
                              style: const TextStyle(fontSize: 11, color: TemaMaritimo.cinzaRede),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Text(
                          alerta.mensagem,
                          style: const TextStyle(fontSize: 13, color: Colors.black87, height: 1.4),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }

  // --- ABA 3: PERFIL ---
  Widget _buildPerfilTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Center(
              child: Stack(
                children: [
                  CircleAvatar(
                    radius: 46,
                    backgroundColor: Color(0xFFE2F0F5),
                    child: Icon(
                      Icons.person,
                      size: 56,
                      color: TemaMaritimo.azulOceano,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            Text(
              _perfilUsuario?.email ?? '',
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 15,
                color: TemaMaritimo.cinzaRede,
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(height: 28),
            
            TextFormField(
              controller: _nomeController,
              decoration: const InputDecoration(
                labelText: 'Nome Completo',
                prefixIcon: Icon(Icons.person_outline),
              ),
              validator: (value) =>
                  value == null || value.isEmpty ? 'Insira o seu nome completo' : null,
            ),
            const SizedBox(height: 16),
            
            TextFormField(
              controller: _telefoneController,
              decoration: const InputDecoration(
                labelText: 'Contacto Telefónico',
                prefixIcon: Icon(Icons.phone_outlined),
              ),
              keyboardType: TextInputType.phone,
              validator: (value) =>
                  value == null || value.isEmpty ? 'Insira o seu contacto telefónico' : null,
            ),
            const SizedBox(height: 16),
            
            TextFormField(
              controller: _documentoController,
              decoration: const InputDecoration(
                labelText: 'N.º de Documento (BI / NUIT)',
                prefixIcon: Icon(Icons.badge_outlined),
              ),
              validator: (value) =>
                  value == null || value.isEmpty ? 'Insira o número do seu documento' : null,
            ),
            const SizedBox(height: 28),
            
            ElevatedButton(
              onPressed: _isSavingPerfil ? null : _salvarPerfil,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
              child: _isSavingPerfil
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                    )
                  : const Text(
                      'Guardar Alterações',
                      style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white),
                    ),
            ),
            const SizedBox(height: 24),
            
            OutlinedButton.icon(
              onPressed: _sair,
              icon: const Icon(Icons.logout, color: TemaMaritimo.vermelhoCoral, size: 18),
              label: const Text(
                'Terminar Sessão',
                style: TextStyle(color: TemaMaritimo.vermelhoCoral, fontWeight: FontWeight.bold),
              ),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 14),
                side: const BorderSide(color: TemaMaritimo.vermelhoCoral, width: 1.5),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
          ],
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
