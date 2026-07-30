import 'package:flutter/material.dart';

class TemaMaritimo {
  // Paleta de cores do plano
  static const Color azulOceano = Color(0xFF0A6B8A);
  static const Color azulProfundo = Color(0xFF063B4F);
  static const Color areiaClara = Color(0xFFF5F0E8);
  static const Color brancoEspuma = Color(0xFFFFFFFF);
  static const Color verdeMar = Color(0xFF2A9D6F);
  static const Color laranjaCoral = Color(0xFFE8834A);
  static const Color vermelhoCoral = Color(0xFFD94F4F);
  static const Color cinzaRede = Color(0xFF4A5568);

  static ThemeData get tema {
    return ThemeData(
      primaryColor: azulOceano,
      scaffoldBackgroundColor: areiaClara,
      colorScheme: const ColorScheme.light(
        primary: azulOceano,
        secondary: laranjaCoral,
        surface: brancoEspuma,
        error: vermelhoCoral,
      ),
      fontFamily: 'Inter',
      appBarTheme: const AppBarTheme(
        backgroundColor: azulProfundo,
        foregroundColor: brancoEspuma,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          fontFamily: 'Outfit',
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: brancoEspuma,
        ),
      ),
      cardTheme: CardTheme(
        color: brancoEspuma,
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: azulOceano,
          foregroundColor: brancoEspuma,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          textStyle: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: brancoEspuma,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFFE2E8F0), width: 2),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Color(0xFFE2E8F0), width: 2),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: azulOceano, width: 2),
        ),
        labelStyle: const TextStyle(color: cinzaRede),
      ),
    );
  }
}
