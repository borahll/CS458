// ✅ Final home_page.dart with added ValueKeys only:
import 'package:flutter/material.dart';
import 'package:mailer/mailer.dart';
import 'package:mailer/smtp_server.dart';
import 'login_page.dart';
import 'package:google_sign_in/google_sign_in.dart';

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

  void _pickDate() async {
    DateTime? pickedDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );

    if (pickedDate != null) {
      setState(() {
        birthDate = pickedDate;
      });
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
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                key: const ValueKey("NameSurnameField"),
                decoration: const InputDecoration(labelText: "Name-Surname"),
                onChanged: (value) => setState(() => nameSurname = value),
              ),
              const SizedBox(height: 10),
              ListTile(
                key: const ValueKey("BirthDateField"),
                title: Text(birthDate == null
                    ? "Select Birth Date"
                    : "${birthDate!.toLocal()}".split(' ')[0]),
                trailing: const Icon(Icons.calendar_today),
                onTap: _pickDate,
              ),
              const SizedBox(height: 10),
              DropdownButtonFormField<String>(
                key: const ValueKey("EducationDropdown"),
                decoration: const InputDecoration(labelText: "Education Level"),
                items: ["High School", "Bachelor", "Master", "PhD"]
                    .map((level) => DropdownMenuItem(
                          value: level,
                          child: Text(level, key: ValueKey("${level}Option")),
                        ))
                    .toList(),
                onChanged: (value) => setState(() => educationLevel = value),
              ),
              const SizedBox(height: 10),
              TextFormField(
                key: const ValueKey("CityField"),
                decoration: const InputDecoration(labelText: "City"),
                onChanged: (value) => setState(() => city = value),
              ),
              const SizedBox(height: 10),
              DropdownButtonFormField<String>(
                key: const ValueKey("GenderDropdown"),
                decoration: const InputDecoration(labelText: "Gender"),
                items: ["Male", "Female", "Other"]
                    .map((gender) => DropdownMenuItem(
                          value: gender,
                          child: Text(gender, key: ValueKey("${gender}Option")),
                        ))
                    .toList(),
                onChanged: (value) => setState(() => gender = value),
              ),
              const SizedBox(height: 10),
              const Text("AI Models Tried (Select Multiple)"),
              Column(
                children: aiModels.map((model) {
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
              ),
              const SizedBox(height: 10),
              ...selectedModels.map((model) {
                return TextFormField(
                  key: ValueKey("${model}ConsField"),
                  decoration:
                      InputDecoration(labelText: "Cons for $model (if any)"),
                  onChanged: (value) =>
                      setState(() => modelCons[model] = value),
                );
              }),
              const SizedBox(height: 10),
              TextFormField(
                key: const ValueKey("AIUseCaseField"),
                decoration: const InputDecoration(
                    labelText: "AI Use Case in Daily Life"),
                onChanged: (value) => setState(() => aiUseCase = value),
                maxLines: 3,
              ),
              const SizedBox(height: 20),
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
}
