import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_hi.dart';
import 'app_localizations_ko.dart';
import 'app_localizations_zh.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'generated/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale) : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates = <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('hi'),
    Locale('ko'),
    Locale('zh')
  ];

  /// No description provided for @appTitle.
  ///
  /// In en, this message translates to:
  /// **'SAT Vocabulary Master'**
  String get appTitle;

  /// No description provided for @todayWord.
  ///
  /// In en, this message translates to:
  /// **'Today\'s Word'**
  String get todayWord;

  /// No description provided for @learning.
  ///
  /// In en, this message translates to:
  /// **'Learning'**
  String get learning;

  /// No description provided for @levelLearning.
  ///
  /// In en, this message translates to:
  /// **'Difficulty Level'**
  String get levelLearning;

  /// No description provided for @allWords.
  ///
  /// In en, this message translates to:
  /// **'All Words'**
  String get allWords;

  /// No description provided for @viewAllWords.
  ///
  /// In en, this message translates to:
  /// **'View all vocabulary'**
  String get viewAllWords;

  /// No description provided for @favorites.
  ///
  /// In en, this message translates to:
  /// **'Favorites'**
  String get favorites;

  /// No description provided for @savedWords.
  ///
  /// In en, this message translates to:
  /// **'Saved words'**
  String get savedWords;

  /// No description provided for @flashcard.
  ///
  /// In en, this message translates to:
  /// **'Flashcard'**
  String get flashcard;

  /// No description provided for @cardLearning.
  ///
  /// In en, this message translates to:
  /// **'Card learning'**
  String get cardLearning;

  /// No description provided for @quiz.
  ///
  /// In en, this message translates to:
  /// **'Quiz'**
  String get quiz;

  /// No description provided for @testYourself.
  ///
  /// In en, this message translates to:
  /// **'Test yourself'**
  String get testYourself;

  /// No description provided for @settings.
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settings;

  /// No description provided for @language.
  ///
  /// In en, this message translates to:
  /// **'Language'**
  String get language;

  /// No description provided for @displayLanguage.
  ///
  /// In en, this message translates to:
  /// **'Display Language'**
  String get displayLanguage;

  /// No description provided for @selectLanguage.
  ///
  /// In en, this message translates to:
  /// **'Select Language'**
  String get selectLanguage;

  /// No description provided for @display.
  ///
  /// In en, this message translates to:
  /// **'Display'**
  String get display;

  /// No description provided for @darkMode.
  ///
  /// In en, this message translates to:
  /// **'Dark Mode'**
  String get darkMode;

  /// No description provided for @fontSize.
  ///
  /// In en, this message translates to:
  /// **'Font Size'**
  String get fontSize;

  /// No description provided for @notifications.
  ///
  /// In en, this message translates to:
  /// **'Notifications'**
  String get notifications;

  /// No description provided for @dailyReminder.
  ///
  /// In en, this message translates to:
  /// **'Daily Reminder'**
  String get dailyReminder;

  /// No description provided for @dailyReminderDesc.
  ///
  /// In en, this message translates to:
  /// **'Get reminded to study every day'**
  String get dailyReminderDesc;

  /// No description provided for @removeAds.
  ///
  /// In en, this message translates to:
  /// **'Remove Ads'**
  String get removeAds;

  /// No description provided for @adsRemoved.
  ///
  /// In en, this message translates to:
  /// **'Ads Removed'**
  String get adsRemoved;

  /// No description provided for @thankYou.
  ///
  /// In en, this message translates to:
  /// **'Thank you for your support!'**
  String get thankYou;

  /// No description provided for @buy.
  ///
  /// In en, this message translates to:
  /// **'Buy'**
  String get buy;

  /// No description provided for @restorePurchase.
  ///
  /// In en, this message translates to:
  /// **'Restore Purchase'**
  String get restorePurchase;

  /// No description provided for @restoring.
  ///
  /// In en, this message translates to:
  /// **'Restoring...'**
  String get restoring;

  /// No description provided for @purchaseSuccess.
  ///
  /// In en, this message translates to:
  /// **'Purchase successful!'**
  String get purchaseSuccess;

  /// No description provided for @loading.
  ///
  /// In en, this message translates to:
  /// **'Loading...'**
  String get loading;

  /// No description provided for @notAvailable.
  ///
  /// In en, this message translates to:
  /// **'Not available'**
  String get notAvailable;

  /// No description provided for @info.
  ///
  /// In en, this message translates to:
  /// **'Info'**
  String get info;

  /// No description provided for @version.
  ///
  /// In en, this message translates to:
  /// **'Version'**
  String get version;

  /// No description provided for @disclaimer.
  ///
  /// In en, this message translates to:
  /// **'Disclaimer'**
  String get disclaimer;

  /// No description provided for @disclaimerText.
  ///
  /// In en, this message translates to:
  /// **'This app is an independent SAT preparation tool and is not affiliated with, endorsed by, or approved by ETS (Educational Testing Service).'**
  String get disclaimerText;

  /// No description provided for @privacyPolicy.
  ///
  /// In en, this message translates to:
  /// **'Privacy Policy'**
  String get privacyPolicy;

  /// No description provided for @cannotLoadWords.
  ///
  /// In en, this message translates to:
  /// **'Cannot load words'**
  String get cannotLoadWords;

  /// No description provided for @noFavoritesYet.
  ///
  /// In en, this message translates to:
  /// **'No favorites yet'**
  String get noFavoritesYet;

  /// No description provided for @tapHeartToSave.
  ///
  /// In en, this message translates to:
  /// **'Tap the heart icon to save words'**
  String get tapHeartToSave;

  /// No description provided for @addedToFavorites.
  ///
  /// In en, this message translates to:
  /// **'Added to favorites'**
  String get addedToFavorites;

  /// No description provided for @removedFromFavorites.
  ///
  /// In en, this message translates to:
  /// **'Removed from favorites'**
  String get removedFromFavorites;

  /// No description provided for @wordDetail.
  ///
  /// In en, this message translates to:
  /// **'Word Detail'**
  String get wordDetail;

  /// No description provided for @definition.
  ///
  /// In en, this message translates to:
  /// **'Definition'**
  String get definition;

  /// No description provided for @example.
  ///
  /// In en, this message translates to:
  /// **'Example'**
  String get example;

  /// No description provided for @levelWords.
  ///
  /// In en, this message translates to:
  /// **'{level} Words'**
  String levelWords(String level);

  /// No description provided for @basic.
  ///
  /// In en, this message translates to:
  /// **'Basic'**
  String get basic;

  /// No description provided for @basicDesc.
  ///
  /// In en, this message translates to:
  /// **'Foundation words - 500 words'**
  String get basicDesc;

  /// No description provided for @common.
  ///
  /// In en, this message translates to:
  /// **'Common'**
  String get common;

  /// No description provided for @commonDesc.
  ///
  /// In en, this message translates to:
  /// **'Frequently tested - 1,000 words'**
  String get commonDesc;

  /// No description provided for @advanced.
  ///
  /// In en, this message translates to:
  /// **'Advanced'**
  String get advanced;

  /// No description provided for @advancedDesc.
  ///
  /// In en, this message translates to:
  /// **'High-frequency SAT - 800 words'**
  String get advancedDesc;

  /// No description provided for @expert.
  ///
  /// In en, this message translates to:
  /// **'Expert'**
  String get expert;

  /// No description provided for @expertDesc.
  ///
  /// In en, this message translates to:
  /// **'Challenging vocabulary - 500 words'**
  String get expertDesc;

  /// No description provided for @alphabetical.
  ///
  /// In en, this message translates to:
  /// **'Alphabetical'**
  String get alphabetical;

  /// No description provided for @random.
  ///
  /// In en, this message translates to:
  /// **'Random'**
  String get random;

  /// No description provided for @tapToFlip.
  ///
  /// In en, this message translates to:
  /// **'Tap to flip'**
  String get tapToFlip;

  /// No description provided for @previous.
  ///
  /// In en, this message translates to:
  /// **'Previous'**
  String get previous;

  /// No description provided for @next.
  ///
  /// In en, this message translates to:
  /// **'Next'**
  String get next;

  /// No description provided for @question.
  ///
  /// In en, this message translates to:
  /// **'Question'**
  String get question;

  /// No description provided for @score.
  ///
  /// In en, this message translates to:
  /// **'Score'**
  String get score;

  /// No description provided for @quizComplete.
  ///
  /// In en, this message translates to:
  /// **'Quiz Complete!'**
  String get quizComplete;

  /// No description provided for @finish.
  ///
  /// In en, this message translates to:
  /// **'Finish'**
  String get finish;

  /// No description provided for @tryAgain.
  ///
  /// In en, this message translates to:
  /// **'Try Again'**
  String get tryAgain;

  /// No description provided for @showResult.
  ///
  /// In en, this message translates to:
  /// **'Show Result'**
  String get showResult;

  /// No description provided for @wordToMeaning.
  ///
  /// In en, this message translates to:
  /// **'Word to Meaning'**
  String get wordToMeaning;

  /// No description provided for @meaningToWord.
  ///
  /// In en, this message translates to:
  /// **'Meaning to Word'**
  String get meaningToWord;

  /// No description provided for @excellent.
  ///
  /// In en, this message translates to:
  /// **'Excellent! Perfect score!'**
  String get excellent;

  /// No description provided for @great.
  ///
  /// In en, this message translates to:
  /// **'Great job! Keep it up!'**
  String get great;

  /// No description provided for @good.
  ///
  /// In en, this message translates to:
  /// **'Good effort! Keep practicing!'**
  String get good;

  /// No description provided for @keepPracticing.
  ///
  /// In en, this message translates to:
  /// **'Keep practicing! You will improve!'**
  String get keepPracticing;

  /// No description provided for @levelA1.
  ///
  /// In en, this message translates to:
  /// **'Beginner'**
  String get levelA1;

  /// No description provided for @levelA2.
  ///
  /// In en, this message translates to:
  /// **'Elementary'**
  String get levelA2;

  /// No description provided for @levelB1.
  ///
  /// In en, this message translates to:
  /// **'Intermediate'**
  String get levelB1;

  /// No description provided for @levelB2.
  ///
  /// In en, this message translates to:
  /// **'Upper Intermediate'**
  String get levelB2;

  /// No description provided for @levelC1.
  ///
  /// In en, this message translates to:
  /// **'Advanced'**
  String get levelC1;

  /// No description provided for @privacyPolicyContent.
  ///
  /// In en, this message translates to:
  /// **'This app does not collect, store, or share any personal information. Your learning progress and favorites are stored only on your device. No data is transmitted to external servers.'**
  String get privacyPolicyContent;

  /// No description provided for @restorePurchaseDesc.
  ///
  /// In en, this message translates to:
  /// **'If you have previously purchased ad removal on another device or after reinstalling the app, tap here to restore your purchase.'**
  String get restorePurchaseDesc;

  /// No description provided for @restoreComplete.
  ///
  /// In en, this message translates to:
  /// **'Restore complete'**
  String get restoreComplete;

  /// No description provided for @noPurchaseFound.
  ///
  /// In en, this message translates to:
  /// **'No previous purchase found'**
  String get noPurchaseFound;
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) => <String>['en', 'hi', 'ko', 'zh'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {


  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en': return AppLocalizationsEn();
    case 'hi': return AppLocalizationsHi();
    case 'ko': return AppLocalizationsKo();
    case 'zh': return AppLocalizationsZh();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.'
  );
}
