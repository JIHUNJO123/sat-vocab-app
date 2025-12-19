import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:jlpt_vocab_app/l10n/generated/app_localizations.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:sqflite_common_ffi_web/sqflite_ffi_web.dart';
import 'screens/home_screen.dart';
import 'services/translation_service.dart';
import 'services/ad_service.dart';
import 'services/purchase_service.dart';
import 'services/display_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // ?뚮옯?쇰퀎 sqflite 珥덇린??
  if (kIsWeb) {
    // ?뱀뿉??sqflite 珥덇린??
    databaseFactory = databaseFactoryFfiWeb;
  } else if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    // Windows, Linux, macOS?먯꽌 sqflite 珥덇린??
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
  }

  // 踰덉뿭 ?쒕퉬??珥덇린??
  await TranslationService.instance.init();

  // 표시 서비스 초기화
  await DisplayService.instance.init();

  // 광고 서비스 초기화
  await AdService.instance.initialize();

  // 인앱 구매 서비스 초기화
  await PurchaseService.instance.initialize();

  runApp(
    ChangeNotifierProvider(
      create: (_) => LocaleProvider(),
      child: const JLPTVocabApp(),
    ),
  );
}

/// ?몄뼱 諛??뚮쭏 蹂寃쎌쓣 ?꾪븳 Provider
class LocaleProvider extends ChangeNotifier {
  Locale _locale = const Locale('en');
  ThemeMode _themeMode = ThemeMode.light;

  Locale get locale => _locale;
  ThemeMode get themeMode => _themeMode;

  LocaleProvider() {
    _loadSavedSettings();
  }

  Future<void> _loadSavedSettings() async {
    final prefs = await SharedPreferences.getInstance();

    // ?몄뼱 濡쒕뱶
    await TranslationService.instance.init();
    final langCode = TranslationService.instance.currentLanguage;
    _locale = _createLocale(langCode);

    // ?ㅽ겕紐⑤뱶 濡쒕뱶
    final isDarkMode = prefs.getBool('darkMode') ?? false;
    _themeMode = isDarkMode ? ThemeMode.dark : ThemeMode.light;

    notifyListeners();
  }

  Locale _createLocale(String langCode) {
    return Locale(langCode);
  }

  void setLocale(Locale locale) {
    _locale = locale;
    TranslationService.instance.setLanguage(locale.languageCode);
    notifyListeners();
  }

  void setLocaleDirectly(Locale locale) {
    _locale = locale;
    notifyListeners();
  }

  void toggleDarkMode(bool isDark) {
    _themeMode = isDark ? ThemeMode.dark : ThemeMode.light;
    notifyListeners();
  }
}

class JLPTVocabApp extends StatelessWidget {
  const JLPTVocabApp({super.key});

  @override
  Widget build(BuildContext context) {
    final localeProvider = Provider.of<LocaleProvider>(context);

    return MaterialApp(
      title: 'JLPT Step N5–N3',
      debugShowCheckedModeBanner: false,

      // Localization ?ㅼ젙
      locale: localeProvider.locale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en'),
        Locale('ko'),
        Locale('zh'),
      ],

      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE53E3E), // JLPT Red
          brightness: Brightness.light,
        ),
        useMaterial3: false,
        appBarTheme: const AppBarTheme(centerTitle: true, elevation: 0),
        cardTheme: CardThemeData(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
        ),
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE53E3E), // JLPT Red
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(centerTitle: true, elevation: 0),
        cardTheme: CardThemeData(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          filled: true,
        ),
      ),
      themeMode: localeProvider.themeMode,
      home: const HomeScreen(),
    );
  }
}

