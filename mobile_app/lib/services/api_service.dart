import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/modelos.dart';

class ApiService {
  // Para usar o Flutter Web ou o telemóvel físico (via ADB reverse), 'localhost' funciona perfeitamente para ambos.
  // Comando USB: adb reverse tcp:8000 tcp:8000
  static const String baseUrl = 'http://localhost:8000/api';
  
  final _storage = const FlutterSecureStorage();

  Future<String?> getToken() async {
    return await _storage.read(key: 'auth_token');
  }

  Future<Map<String, String>> _getHeaders() async {
    final token = await getToken();
    return {
      'Content-Type': 'application/json; charset=UTF-8',
      if (token != null) 'Authorization': 'Token $token',
    };
  }

  Future<Map<String, dynamic>?> registar(String nomeCompleto, String email, String telefone, String numeroDocumento, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/registar/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'nome_completo': nomeCompleto,
          'email': email,
          'telefone': telefone,
          'numero_documento': numeroDocumento,
          'password': password,
        }),
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        await _storage.write(key: 'auth_token', value: data['token']);
        await _storage.write(key: 'user_nome', value: data['nome']);
        await _storage.write(key: 'user_tipo', value: data['tipo_utilizador']);
        return data;
      } else {
        final errorData = jsonDecode(response.body);
        return {'erro': errorData['erro'] ?? 'Erro desconhecido.'};
      }
    } catch (e) {
      print('Erro de Registo API: $e');
    }
    return null;
  }

  Future<Map<String, dynamic>?> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await _storage.write(key: 'auth_token', value: data['token']);
        await _storage.write(key: 'user_nome', value: data['nome']);
        await _storage.write(key: 'user_tipo', value: data['tipo_utilizador']);
        return data;
      }
    } catch (e) {
      print('Erro de Login API: $e');
    }
    return null;
  }

  Future<void> logout() async {
    await _storage.deleteAll();
  }

  Future<List<Embarcacao>> getEmbarcacoes() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/embarcacoes/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        // DRF com paginação retorna { 'results': [...] }
        final body = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = body['results'] ?? [];
        return results.map((e) => Embarcacao.fromJson(e)).toList();
      }
    } catch (e) {
      print('Erro ao obter embarcações: $e');
    }
    return [];
  }

  Future<bool> solicitarRegistoEmbarcacao(Map<String, dynamic> dadosEmbarcacao) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/embarcacoes/'),
        headers: await _getHeaders(),
        body: jsonEncode(dadosEmbarcacao),
      );

      // 201 Created é o código de sucesso esperado de um POST na REST API
      return response.statusCode == 201;
    } catch (e) {
      print('Erro ao registar embarcação: $e');
    }
    return false;
  }

  Future<List<AlertaModel>> getAlertas() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/alertas/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        final body = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = body['results'] ?? [];
        return results.map((e) => AlertaModel.fromJson(e)).toList();
      }
    } catch (e) {
      print('Erro ao obter alertas: $e');
    }
    return [];
  }

  Future<Usuario?> getPerfil() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/perfil/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        return Usuario.fromJson(jsonDecode(utf8.decode(response.bodyBytes)));
      }
    } catch (e) {
      print('Erro ao obter perfil: $e');
    }
    return null;
  }

  Future<List<ConfiguracaoAlertaModel>> getConfiguracoes() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/configuracoes/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        final body = jsonDecode(utf8.decode(response.bodyBytes));
        final List<dynamic> results = body is Map ? (body['results'] ?? []) : body;
        return results.map((e) => ConfiguracaoAlertaModel.fromJson(e)).toList();
      }
    } catch (e) {
      print('Erro ao obter configuracoes: $e');
    }
    return [];
  }

  Future<bool> salvarConfiguracao(ConfiguracaoAlertaModel config) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/configuracoes/${config.id}/'),
        headers: await _getHeaders(),
        body: jsonEncode(config.toJson()),
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Erro ao salvar configuracao: $e');
    }
    return false;
  }

  Future<bool> atualizarPerfil(Map<String, dynamic> dados) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/perfil/'),
        headers: await _getHeaders(),
        body: jsonEncode(dados),
      );

      if (response.statusCode == 200) {
        // Atualizar o nome armazenado localmente se foi alterado
        if (dados.containsKey('nome_completo')) {
          await _storage.write(key: 'user_nome', value: dados['nome_completo']);
        }
        return true;
      }
    } catch (e) {
      print('Erro ao atualizar perfil: $e');
    }
    return false;
  }

  Future<bool> recuperarSenha(String email) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/password-reset/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      );
      
      if (response.statusCode == 200) {
        return true;
      }
    } catch (e) {
      print('Erro ao recuperar senha: $e');
    }
    return false;
  }
}
