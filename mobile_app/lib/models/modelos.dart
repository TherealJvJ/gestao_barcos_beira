class Usuario {
  final int id;
  final String nomeCompleto;
  final String email;
  final String telefone;
  final String numeroDocumento;
  final String tipoUtilizador;

  Usuario({
    required this.id,
    required this.nomeCompleto,
    required this.email,
    required this.telefone,
    required this.numeroDocumento,
    required this.tipoUtilizador,
  });

  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      id: json['id'],
      nomeCompleto: json['nome_completo'],
      email: json['email'],
      telefone: json['telefone'],
      numeroDocumento: json['numero_documento'] ?? '',
      tipoUtilizador: json['tipo_utilizador'],
    );
  }
}

class Licenca {
  final int id;
  final String numeroLicenca;
  final String dataEmissao;
  final String dataValidade;
  final int anoReferencia;
  final bool activa;
  final String estado;
  final int diasRestantes;
  final String observacoes;

  Licenca({
    required this.id,
    required this.numeroLicenca,
    required this.dataEmissao,
    required this.dataValidade,
    required this.anoReferencia,
    required this.activa,
    required this.estado,
    required this.diasRestantes,
    required this.observacoes,
  });

  factory Licenca.fromJson(Map<String, dynamic> json) {
    return Licenca(
      id: json['id'],
      numeroLicenca: json['numero_licenca'],
      dataEmissao: json['data_emissao'],
      dataValidade: json['data_validade'],
      anoReferencia: json['ano_referencia'],
      activa: json['activa'],
      estado: json['estado'],
      diasRestantes: json['dias_restantes'],
      observacoes: json['observacoes'] ?? '',
    );
  }
}

class Titulo {
  final int id;
  final String numeroTitulo;
  final String dataEmissao;
  final bool activo;
  final String observacoes;

  Titulo({
    required this.id,
    required this.numeroTitulo,
    required this.dataEmissao,
    required this.activo,
    required this.observacoes,
  });

  factory Titulo.fromJson(Map<String, dynamic> json) {
    return Titulo(
      id: json['id'],
      numeroTitulo: json['numero_titulo'],
      dataEmissao: json['data_emissao'],
      activo: json['activo'],
      observacoes: json['observacoes'] ?? '',
    );
  }
}

class Embarcacao {
  final int id;
  final String nome;
  final String numeroMatricula;
  final String tipoEmbarcacao;
  final double comprimento;
  final int potenciaMotor;
  final int anoConstrucao;
  final String material;
  final String estadoRegisto;
  final String observacoes;
  final Licenca? licencaActiva;
  final Titulo? titulo;

  Embarcacao({
    required this.id,
    required this.nome,
    required this.numeroMatricula,
    required this.tipoEmbarcacao,
    required this.comprimento,
    required this.potenciaMotor,
    required this.anoConstrucao,
    required this.material,
    required this.estadoRegisto,
    required this.observacoes,
    this.licencaActiva,
    this.titulo,
  });

  factory Embarcacao.fromJson(Map<String, dynamic> json) {
    return Embarcacao(
      id: json['id'],
      nome: json['nome'],
      numeroMatricula: json['numero_matricula'],
      tipoEmbarcacao: json['tipo_embarcacao'],
      comprimento: (json['comprimento'] as num).toDouble(),
      potenciaMotor: json['potencia_motor'],
      anoConstrucao: json['ano_construcao'],
      material: json['material'],
      estadoRegisto: json['estado_registo'],
      observacoes: json['observacoes'] ?? '',
      licencaActiva: json['licenca_activa'] != null
          ? Licenca.fromJson(json['licenca_activa'])
          : null,
      titulo: json['titulo'] != null
          ? Titulo.fromJson(json['titulo'])
          : null,
    );
  }
}

class AlertaModel {
  final int id;
  final String tipoAlerta;
  final String tipoDisplay;
  final String mensagem;
  final String estado;
  final String dataCriacao;

  AlertaModel({
    required this.id,
    required this.tipoAlerta,
    required this.tipoDisplay,
    required this.mensagem,
    required this.estado,
    required this.dataCriacao,
  });

  factory AlertaModel.fromJson(Map<String, dynamic> json) {
    return AlertaModel(
      id: json['id'],
      tipoAlerta: json['tipo_alerta'],
      tipoDisplay: json['tipo_display'],
      mensagem: json['mensagem'],
      estado: json['estado'],
      dataCriacao: json['data_criacao'],
    );
  }
}

class ConfiguracaoAlertaModel {
  final int id;
  final int diasAntecedencia;
  final String canal;
  final bool activo;
  final String tipoDocumento;

  ConfiguracaoAlertaModel({
    required this.id,
    required this.diasAntecedencia,
    required this.canal,
    required this.activo,
    required this.tipoDocumento,
  });

  factory ConfiguracaoAlertaModel.fromJson(Map<String, dynamic> json) {
    return ConfiguracaoAlertaModel(
      id: json['id'],
      diasAntecedencia: json['dias_antecedencia'],
      canal: json['canal'],
      activo: json['activo'],
      tipoDocumento: json['tipo_documento'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'dias_antecedencia': diasAntecedencia,
      'canal': canal,
      'activo': activo,
      'tipo_documento': tipoDocumento,
    };
  }
}
