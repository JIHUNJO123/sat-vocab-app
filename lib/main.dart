import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:sqflite_common_ffi_web/sqflite_ffi_web.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import 'screens/home_screen.dart';
import 'services/translation_service.dart';
import 'services/ad_service.dart';
import 'services/purchase_service.dart';

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

  // 번역 서비스 초기화
  await TranslationService.instance.init();

  // AdMob SDK 초기화 (모바일 플랫폼에서만)
  if (!kIsWeb && (Platform.isAndroid || Platform.isIOS)) {
    try {
      await MobileAds.instance.initialize();
      debugPrint('AdMob SDK initialized successfully');
    } catch (e) {
      debugPrint('AdMob init error: $e');
    }
  }

  // 광고 서비스 초기화 (잠금 해제 상태 로드 + 보상형 광고 로드)
  await AdService.instance.loadUnlockStatus();
  AdService.instance.loadRewardedAd();

  // 인앱 구매 서비스 초기화
  await PurchaseService.instance.initialize();

  runApp(
    ChangeNotifierProvider(
      create: (_) => LocaleProvider(),
      child: const SATVocabApp(),
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

class SATVocabApp extends StatelessWidget {
  const SATVocabApp({super.key});

  @override
  Widget build(BuildContext context) {
    final localeProvider = Provider.of<LocaleProvider>(context);

    return MaterialApp(
      title: 'SAT Vocabulary Master',
      debugShowCheckedModeBanner: false,

      // Localization settings
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
        Locale('ja'),
        Locale('zh'),
        Locale('es'),
        Locale('pt'),
        Locale('de'),
        Locale('fr'),
        Locale('vi'),
        Locale('ar'),
        Locale('id'),
        Locale('hi'),
      ],

      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E86AB), // SAT Blue
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
          seedColor: const Color(0xFF6B4EAB),
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
