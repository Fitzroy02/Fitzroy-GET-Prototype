import 'package:flutter/material.dart';
import 'override_handler.dart';

void main() => runApp(GETSOverrideApp());

class GETSOverrideApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GETS Override',
      home: OverrideHome(),
    );
  }
}

class OverrideHome extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Emergency Override')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => activateOverride(context),
          child: Text('Activate Override'),
        ),
      ),
    );
  }
}
