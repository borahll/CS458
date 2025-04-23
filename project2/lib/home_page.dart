import 'package:flutter/material.dart';
import 'package:mailer/mailer.dart';
import 'package:mailer/smtp_server.dart';
import 'package:intl/intl.dart';
import 'package:google_sign_in/google_sign_in.dart';

import 'login_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  _HomePage createState() => _HomePage();
}

class _HomePage extends State<HomePage> {
  final _formKey = GlobalKey<FormState>();

  String? nameSurname;
  DateTime? birthDate;
  String? educationLevel;
  String? city;
  String? gender;
  List<String> selectedModels = [];
  Map<String, String> modelCons = {};
  String? aiUseCase;

  final List<String> aiModels = ["ChatGPT", "Bard", "Claude", "Copilot"];

  // We'll store the typed date in this controller
  final TextEditingController _birthDateController = TextEditingController();

  bool get isFormValid =>
      nameSurname != null &&
      birthDate != null &&
      educationLevel != null &&
      city != null &&
      gender != null &&
      selectedModels.isNotEmpty &&
      aiUseCase != null;

  Future<void> _sendEmail() async {
    final smtpServer =
        gmail('borahaliloglu03@gmail.com', 'igzl qydy zzgn ckei');

    final message = Message()
      ..from = const Address('borahaliloglu03@yahoo.com', 'cs458')
      ..recipients.add('example@gmail.com')
      ..subject = 'AI Survey Response'
      ..text = """
      Name-Surname: $nameSurname
      Birth Date: ${birthDate?.toLocal()}
      Education Level: $educationLevel
      City: $city
      Gender: $gender
      AI Models Tried: ${selectedModels.join(', ')}
      Model Cons: ${modelCons.entries.map((e) => '${e.key}: ${e.value}').join('; ')}
      AI Use Case: $aiUseCase
      """;

    try {
      await send(message, smtpServer);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Survey sent successfully!")),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed to send survey: $e")),
        );
      }
    }
  }

  void _logout() async {
    try {
      await GoogleSignIn().signOut();
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const LoginPage()),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed to log out from Google: $e")),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        key: const ValueKey("Survey Form"),
        title: const Text("Survey Form"),
        actions: [
          IconButton(
            key: const ValueKey("LogoutButton"),
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Name-Surname
              TextFormField(
                key: const ValueKey("NameSurnameField"),
                decoration: const InputDecoration(labelText: "Name-Surname"),
                onChanged: (value) {
                  setState(() {
                    nameSurname = value.trim().isEmpty ? null : value.trim();
                  });
                },
              ),
              const SizedBox(height: 10),

              // Birth Date with manual . insertion
              TextFormField(
                key: const ValueKey("BirthDateField"),
                controller: _birthDateController,
                decoration: const InputDecoration(
                  labelText: "Birth Date (DD.MM.YYYY)",
                  hintText: "e.g. 01.01.2007",
                ),
                // The onChanged automatically inserts dots
                onChanged: (value) {
                  _formatBirthDate(value);
                },
              ),

              const SizedBox(height: 10),

              DropdownButtonFormField<String>(
                key: const ValueKey("EducationDropdown"),
                decoration: const InputDecoration(labelText: "Education Level"),
                items: ["High School", "Bachelor", "Master", "PhD"]
                    .map(
                      (level) => DropdownMenuItem(
                        value: level,
                        child: Text(
                          level,
                          key: ValueKey("${level}Option"),
                        ),
                      ),
                    )
                    .toList(),
                onChanged: (value) {
                  setState(() => educationLevel = value);
                },
              ),
              const SizedBox(height: 10),

              // City
              TextFormField(
                key: const ValueKey("CityField"),
                decoration: const InputDecoration(labelText: "City"),
                onChanged: (value) {
                  setState(() => city = value.trim().isEmpty ? null : value);
                },
              ),
              const SizedBox(height: 10),

              // Gender
              DropdownButtonFormField<String>(
                key: const ValueKey("GenderDropdown"),
                decoration: const InputDecoration(labelText: "Gender"),
                items: ["Male", "Female", "Other"]
                    .map((gender) => DropdownMenuItem(
                          value: gender,
                          child: Text(
                            gender,
                            key: ValueKey("${gender}Option"),
                          ),
                        ))
                    .toList(),
                onChanged: (value) {
                  setState(() => this.gender = value);
                },
              ),
              const SizedBox(height: 10),

              // AI Models
              const Text("AI Models Tried (Select Multiple)"),
              ...aiModels.map((model) {
                return CheckboxListTile(
                  key: ValueKey("${model}Checkbox"),
                  title: Text(model),
                  value: selectedModels.contains(model),
                  onChanged: (isChecked) {
                    setState(() {
                      if (isChecked == true) {
                        selectedModels.add(model);
                        modelCons[model] = "";
                      } else {
                        selectedModels.remove(model);
                        modelCons.remove(model);
                      }
                    });
                  },
                );
              }).toList(),
              const SizedBox(height: 10),

              // For each selected model, a "Cons" field
              ...selectedModels.map((model) {
                return TextFormField(
                  key: ValueKey("${model}ConsField"),
                  decoration: InputDecoration(
                    labelText: "Cons for $model (if any)",
                  ),
                  onChanged: (value) {
                    setState(() => modelCons[model] = value);
                  },
                );
              }),
              const SizedBox(height: 10),

              // AI Use Case
              TextFormField(
                key: const ValueKey("AIUseCaseField"),
                decoration: const InputDecoration(
                  labelText: "AI Use Case in Daily Life",
                ),
                onChanged: (value) {
                  setState(
                      () => aiUseCase = value.trim().isEmpty ? null : value);
                },
                maxLines: 3,
              ),
              const SizedBox(height: 20),

              // Send button
              Visibility(
                visible: isFormValid,
                child: ElevatedButton(
                  key: const ValueKey("SendSurveyButton"),
                  onPressed: isFormValid ? _sendEmail : null,
                  style: ButtonStyle(
                    backgroundColor: MaterialStateProperty.resolveWith<Color>(
                      (states) => isFormValid ? Colors.blue : Colors.grey,
                    ),
                  ),
                  child: const Text("Send"),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Reformat the user-typed string to "DD.MM.YYYY" with auto dots.
  /// Then parse for validity (not future).
  void _formatBirthDate(String rawInput) {
    // 1) Remove all non-digit chars
    final digits = rawInput.replaceAll(RegExp(r'\D'), '');
    // 2) Build a new string with dots after 2 and 4 digits
    String formatted = '';
    for (int i = 0; i < digits.length; i++) {
      formatted += digits[i];
      if ((i == 1 || i == 3) && i < digits.length - 1) {
        // Insert a '.' after 2 digits (DD.) and then after 2 more digits (MM.)
        formatted += '.';
      }
    }

    // 3) Update the TextEditingController text (keeping the cursor at end)
    _birthDateController.value = TextEditingValue(
      text: formatted,
      selection: TextSelection.collapsed(offset: formatted.length),
    );

    // 4) Parse the result if it has length 10 => "DD.MM.YYYY"
    if (formatted.length == 10) {
      final parsed = _parseAndValidateDate(formatted);
      setState(() {
        birthDate = parsed; // if invalid/future, parsed is null
      });
    } else {
      // Not enough digits => not a valid date yet
      setState(() {
        birthDate = null;
      });
    }
  }

  /// Attempt to parse "DD.MM.YYYY" and ensure not after today
  DateTime? _parseAndValidateDate(String input) {
    try {
      final formatter = DateFormat("dd.MM.yyyy");
      final parsed = formatter.parseStrict(input);
      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);

      // If parsed date is after today's date, treat as invalid
      if (parsed.isAfter(today)) {
        return null;
      }
      return parsed;
    } catch (_) {
      return null;
    }
  }
}
