// ✅ Final login_page.dart with added ValueKeys only:
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'home_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  String message = '';

  Future<void> signInWithGoogle() async {
    try {
      final GoogleSignInAccount? googleUser = await GoogleSignIn().signIn();
      if (googleUser == null) return; // User canceled sign-in

      final GoogleSignInAuthentication googleAuth =
          await googleUser.authentication;
      final OAuthCredential credential = GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );

      await FirebaseAuth.instance.signInWithCredential(credential);

      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const HomePage()),
        );
      }
    } catch (e) {
      print("Error during Google Sign-In: $e"); // Add error logging
      if (mounted) {
        setState(() {
          message = "Google Sign-In failed. Try again.";
        });
      }
    }
  }

  /// **Mock Facebook Login**
  void mockFacebookLogin() {
    setState(() {
      message = "Facebook login (mock) successful!";
    });

    // Navigate to HomePage after successful login
    if (mounted) {
      Navigator.pushReplacement(
          context, MaterialPageRoute(builder: (_) => const HomePage()));
    }
  }

  /// **Mock Email/Password Login**
  void handleMockLogin() {
    String email = emailController.text.trim();
    String password = passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      setState(() => message = "Email/Password required!");
    } else if (email == "test@example.com" && password == "12345") {
      if (mounted) {
        Navigator.pushReplacement(
            context, MaterialPageRoute(builder: (_) => const HomePage()));
      }
    } else {
      setState(() => message = "Invalid credentials!");
    }
  }

  @override
  Widget build(BuildContext context) {
    final double screenWidth = MediaQuery.of(context).size.width;
    final double screenHeight = MediaQuery.of(context).size.height;
    const double containerWidth = 350; // Fixed width for container
    final double buttonHeight = screenHeight * 0.06;

    return Scaffold(
      body: Container(
        // Gradient background
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF3498db),
              Color(0xFF8e44ad)
            ], // Your gradient colors
            stops: [0.0, 1.0], // To control the gradient transition
          ),
        ),
        child: Center(
          child: Container(
            padding: const EdgeInsets.all(20), // Padding inside container
            width: containerWidth,
            decoration: BoxDecoration(
              color: Colors.white
                  .withOpacity(0.8), // Semi-transparent white background
              borderRadius: BorderRadius.circular(8), // Rounded corners
              boxShadow: const [
                BoxShadow(color: Colors.black26, blurRadius: 20)
              ], // Box shadow
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Sign In Header
                Text(
                  "Sign In",
                  style: TextStyle(
                    fontSize: screenWidth * 0.07,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                SizedBox(height: screenHeight * 0.02),

                // Email Input
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: TextField(
                    key: const ValueKey("EmailField"),
                    controller: emailController,
                    decoration: const InputDecoration(
                      labelText: "Email or Phone",
                      border: OutlineInputBorder(),
                      contentPadding:
                          EdgeInsets.symmetric(vertical: 12, horizontal: 15),
                    ),
                  ),
                ),

                // Password Input
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: TextField(
                    key: const ValueKey("PasswordField"),
                    controller: passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: "Password",
                      border: OutlineInputBorder(),
                      contentPadding:
                          EdgeInsets.symmetric(vertical: 12, horizontal: 15),
                    ),
                  ),
                ),

                // Error Message
                if (message.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 10),
                    child: Text(
                      message,
                      style: const TextStyle(
                          color: Colors.red, fontWeight: FontWeight.bold),
                    ),
                  ),

                const SizedBox(height: 20),

                // Login Button
                SizedBox(
                  key: const ValueKey("EmailLoginButton"),
                  width: 300, // Fixed button width
                  height: buttonHeight,
                  child: ElevatedButton(
                    onPressed: handleMockLogin,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                      shape: RoundedRectangleBorder(
                        borderRadius:
                            BorderRadius.circular(4), // Rounded button corners
                      ),
                      padding: const EdgeInsets.symmetric(vertical: 15),
                    ),
                    child: const Text("Login",
                        style: TextStyle(
                            color: Colors.white, fontWeight: FontWeight.bold)),
                  ),
                ),

                const SizedBox(height: 20),

                // Social Login Row
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Google Login Button (Image Asset)
                    GestureDetector(
                      key: const ValueKey("GoogleLoginButton"),
                      onTap: signInWithGoogle,
                      child: SizedBox(
                        width: 180, // Fixed width for Google button
                        height: buttonHeight,
                        child: Image.asset(
                          'assets/signin-assets/iOS/png@1x/dark/ios_dark_rd_ctn@1x.png',
                          fit: BoxFit.contain, // Adjust to fit the container
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),

                    // Facebook Login Button
                    GestureDetector(
                      key: const ValueKey("FacebookLoginButton"),
                      onTap: mockFacebookLogin,
                      child: Container(
                        width: 120, // Fixed width for Facebook button
                        height: buttonHeight,
                        decoration: BoxDecoration(
                          color: Colors.blue[800], // Facebook blue
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: const Center(
                          child: Text("Facebook",
                              style: TextStyle(color: Colors.white)),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
