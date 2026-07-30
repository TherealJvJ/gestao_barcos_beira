import 'package:flutter/material.dart';
import '../models/modelos.dart';
import '../theme/tema.dart';

class AlertasView extends StatelessWidget {
  final List<AlertaModel> alertas;

  const AlertasView({super.key, required this.alertas});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notificações e Alertas'),
      ),
      body: alertas.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Icon(Icons.notifications_none, size: 64, color: TemaMaritimo.cinzaRede),
                  SizedBox(height: 16),
                  Text('Não tem notificações no momento.', style: TextStyle(color: TemaMaritimo.cinzaRede)),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: alertas.length,
              itemBuilder: (context, index) {
                final alerta = alertas[index];
                
                // Escolher ícone e cor com base no tipo de alerta
                IconData icone = Icons.info;
                Color cor = TemaMaritimo.azulOceano;
                
                if (alerta.tipoAlerta.contains('licenca') || alerta.tipoAlerta.contains('titulo')) {
                  icone = Icons.verified_user;
                  cor = TemaMaritimo.verdeMar;
                } else if (alerta.tipoAlerta.contains('expirando')) {
                  icone = Icons.warning_amber_rounded;
                  cor = TemaMaritimo.laranjaCoral;
                } else if (alerta.tipoAlerta.contains('rejeitada')) {
                  icone = Icons.error_outline;
                  cor = TemaMaritimo.vermelhoCoral;
                }

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(
                    side: BorderSide(color: cor, width: 4),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(icone, color: cor),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                alerta.tipoDisplay ?? 'Notificação',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16,
                                  color: TemaMaritimo.azulProfundo,
                                ),
                              ),
                            ),
                            Text(
                              alerta.dataCriacao.isNotEmpty
                                  ? alerta.dataCriacao.split('T')[0] 
                                  : '',
                              style: const TextStyle(fontSize: 12, color: TemaMaritimo.cinzaRede),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(
                          alerta.mensagem,
                          style: const TextStyle(fontSize: 14),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
