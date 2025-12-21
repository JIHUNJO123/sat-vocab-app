import 'dart:ui' as ui;
import 'package:shared_preferences/shared_preferences.dart';

/// Supported language information
class SupportedLanguage {
  final String code;
  final String name;
  final String nativeName;

  const SupportedLanguage({
    required this.code,
    required this.name,
    required this.nativeName,
  });
}

/// Translation service (embedded translations only, no API calls)
class TranslationService {
  static final TranslationService instance = TranslationService._init();
  TranslationService._init();

  // Supported languages list - English, Korean, Chinese only
  static const List<SupportedLanguage> supportedLanguages = [
    SupportedLanguage(code: 'en', name: 'English', nativeName: 'English'),
    SupportedLanguage(code: 'ko', name: 'Korean', nativeName: 'Korean'),
    SupportedLanguage(code: 'zh', name: 'Chinese', nativeName: 'Chinese'),
  ];

  String _currentLanguage = 'en';

  String get currentLanguage => _currentLanguage;

  /// Get current language info
  SupportedLanguage get currentLanguageInfo {
    return supportedLanguages.firstWhere(
      (lang) => lang.code == _currentLanguage,
      orElse: () => supportedLanguages.first,
    );
  }
