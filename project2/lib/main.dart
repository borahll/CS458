import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_driver/driver_extension.dart';

import 'firebase_options.dart';
import 'login_page.dart';

void main() async {
  // Enable Flutter Driver extension for integration testing
  enableFlutterDriverExtension();
  print("✅ Flutter Driver extension enabled");
  // Required to initialize bindings before Firebase
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Run the app
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginPage(),
    );
  }
}
