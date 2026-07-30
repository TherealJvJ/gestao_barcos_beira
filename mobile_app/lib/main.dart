import 'package:flutter/material.dart';
import 'theme/tema.dart';
import 'views/login_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'INTRANSMAR Beira',
      theme: TemaMaritimo.tema,
      home: const LoginView(),
      debugShowCheckedModeBanner: false,
    );
  }
}
