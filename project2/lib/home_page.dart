import 'package:flutter/material.dart';
import 'package:mailer/mailer.dart';
import 'package:mailer/smtp_server.dart';
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

  bool get isFormValid =>
      nameSurname != null &&
          birthDate != null &&
          educationLevel != null &&
          city != null &&
          gender != null &&
          selectedModels.isNotEmpty &&
          aiUseCase != null;

  Future<void> _sendEmail() async {
    final smtpServer = gmail('borahaliloglu03@gmail.com', 'igzl qydy zzgn ckei'); // Use App Password

    final message = Message()
      ..from = const Address('borahaliloglu03@yahoo.com', 'cs458') // Change to your email
      ..recipients.add('example@gmail.com') // Recipient email
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
        // Ensuring context is available before showing the Snackbar
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

  // Logout Method
  void _logout() async {
    // Here you can clear the state or perform any necessary cleanup
    // For example, if you're using SharedPreferences to store user data:
    // SharedPreferences.getInstance().then((prefs) {
    //   prefs.remove('user_logged_in');
    // });

    // Delay navigation to ensure the widget is still mounted
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginPage()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Survey Form"),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout, // Logout button action
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
                decoration: const InputDecoration(labelText: "Name-Surname"),
                onChanged: (value) {
                  setState(() {
                    nameSurname = value;
                  });
                },
              ),
              const SizedBox(height: 10),
              ListTile(
                title: Text(birthDate == null
                    ? "Select Birth Date"
                    : "${birthDate!.toLocal()}".split(' ')[0]),
                trailing: const Icon(Icons.calendar_today),
                onTap: _pickDate,
              ),
              const SizedBox(height: 10),
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(labelText: "Education Level"),
                items: ["High School", "Bachelor", "Master", "PhD"]
                    .map((level) => DropdownMenuItem(
                  value: level,
                  child: Text(level),
                ))
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    educationLevel = value;
                  });
                },
              ),
              const SizedBox(height: 10),
              TextFormField(
                decoration: const InputDecoration(labelText: "City"),
                onChanged: (value) {
                  setState(() {
                    city = value;
                  });
                },
              ),
              const SizedBox(height: 10),
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(labelText: "Gender"),
                items: ["Male", "Female", "Other"]
                    .map((gender) => DropdownMenuItem(
                  value: gender,
                  child: Text(gender),
                ))
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    gender = value;
                  });
                },
              ),
              const SizedBox(height: 10),
              const Text("AI Models Tried (Select Multiple)"),
              Column(
                children: aiModels.map((model) {
                  return CheckboxListTile(
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
                  decoration: InputDecoration(labelText: "Cons for $model (if any)"),
                  onChanged: (value) {
                    setState(() {
                      modelCons[model] = value;
                    });
                  },
                );
              }),
              const SizedBox(height: 10),
              TextFormField(
                decoration: const InputDecoration(labelText: "AI Use Case in Daily Life"),
                onChanged: (value) {
                  setState(() {
                    aiUseCase = value;
                  });
                },
                maxLines: 3,
              ),
              const SizedBox(height: 20),
              Visibility(
                visible: isFormValid,
                child: ElevatedButton(
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
