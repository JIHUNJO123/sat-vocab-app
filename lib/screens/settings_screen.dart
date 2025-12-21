import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../main.dart';
import '../services/translation_service.dart';
import '../services/purchase_service.dart';
import '../services/ad_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _darkMode = false;
  bool _dailyReminder = false;
  double _fontSize = 1.0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadSettings();
    _setupPurchaseCallbacks();
  }

  void _setupPurchaseCallbacks() {
    PurchaseService.instance.onPurchaseSuccess = () {
      if (mounted) {
        setState(() {});
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(AppLocalizations.of(context)!.purchaseSuccess),
            backgroundColor: Colors.green,
          ),
        );
      }
    };

    PurchaseService.instance.onPurchaseError = (error) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(error), backgroundColor: Colors.red),
        );
      }
    };
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _darkMode = prefs.getBool('darkMode') ?? false;
      _dailyReminder = prefs.getBool('dailyReminder') ?? false;
      _fontSize = prefs.getDouble('wordFontSize') ?? 1.0;
      _isLoading = false;
    });
  }

  Future<void> _saveSetting(String key, dynamic value) async {
    final prefs = await SharedPreferences.getInstance();
    if (value is bool) {
      await prefs.setBool(key, value);
    } else if (value is double) {
      await prefs.setDouble(key, value);
    } else if (value is String) {
      await prefs.setString(key, value);
    }
  }

  void _showLanguageSelector() {
    final l10n = AppLocalizations.of(context)!;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder:
          (context) => DraggableScrollableSheet(
            initialChildSize: 0.7,
            maxChildSize: 0.9,
            minChildSize: 0.5,
            expand: false,
            builder:
                (context, scrollController) => Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Text(
                        l10n.selectLanguage,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const Divider(),
                    Expanded(
                      child: ListView.builder(
                        controller: scrollController,
                        itemCount: TranslationService.supportedLanguages.length,
                        itemBuilder: (context, index) {
                          final lang =
                              TranslationService.supportedLanguages[index];
                          final isSelected =
                              TranslationService.instance.currentLanguage ==
                              lang.code;

                          return ListTile(
                            leading:
                                isSelected
                                    ? Icon(
                                      Icons.check,
                                      color: Theme.of(context).primaryColor,
                                    )
                                    : const SizedBox(width: 24),
                            title: Text(lang.nativeName),
                            subtitle: Text(lang.name),
                            onTap: () {
                              // TranslationService???¸ì–´ ì½”ë“œ ?€??
                              TranslationService.instance.setLanguage(
                                lang.code,
                              );

                              Provider.of<LocaleProvider>(
                                context,
                                listen: false,
                              ).setLocaleDirectly(Locale(lang.code));
                              Navigator.pop(context);
                              setState(() {});
                            },
                          );
                        },
                      ),
                    ),
                  ],
                ),
          ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final localeProvider = Provider.of<LocaleProvider>(context);

    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.settings)),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(title: Text(l10n.settings)),
      body: ListView(
        children: [
          // Language Section
          _buildSectionHeader(l10n.language),
          ListTile(
            leading: const Icon(Icons.language),
            title: Text(l10n.displayLanguage),
            subtitle: Text(
              TranslationService.instance.currentLanguageInfo.nativeName,
            ),
            trailing: const Icon(Icons.chevron_right),
            onTap: _showLanguageSelector,
          ),
          const Divider(),

          // Display Section
          _buildSectionHeader(l10n.display),
          SwitchListTile(
            secondary: const Icon(Icons.dark_mode),
            title: Text(l10n.darkMode),
            value: _darkMode,
            onChanged: (value) {
              setState(() => _darkMode = value);
              _saveSetting('darkMode', value);
              localeProvider.toggleDarkMode(value);
            },
          ),
          ListTile(
            leading: const Icon(Icons.text_fields),
            title: Text(l10n.fontSize),
            subtitle: Slider(
              value: _fontSize,
              min: 0.8,
              max: 1.4,
              divisions: 6,
              label: '${(_fontSize * 100).round()}%',
              onChanged: (value) {
                setState(() => _fontSize = value);
                _saveSetting('wordFontSize', value);
              },
            ),
          ),
          const Divider(),

          // Notification Section
          _buildSectionHeader(l10n.notifications),
          SwitchListTile(
            secondary: const Icon(Icons.notifications),
            title: Text(l10n.dailyReminder),
            subtitle: Text(l10n.dailyReminderDesc),
            value: _dailyReminder,
            onChanged: (value) {
              setState(() => _dailyReminder = value);
              _saveSetting('dailyReminder', value);
            },
          ),
          const Divider(),

          // Remove Ads Section
          _buildRemoveAdsSection(),
          const Divider(),

          // Info Section
          _buildSectionHeader(l10n.info),
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: Text(l10n.version),
            subtitle: const Text('1.0.0'),
          ),
          ListTile(
            leading: const Icon(Icons.copyright),
            title: Text(l10n.disclaimer),
            subtitle: Text(l10n.disclaimerText),
            isThreeLine: true,
          ),
          ListTile(
            leading: const Icon(Icons.privacy_tip),
            title: Text(l10n.privacyPolicy),
            onTap: () {
              showDialog(
                context: context,
                builder:
                    (context) => AlertDialog(
                      title: Text(l10n.privacyPolicy),
                      content: Text(l10n.privacyPolicyContent),
                      actions: [
                        TextButton(
                          onPressed: () => Navigator.pop(context),
                          child: const Text('OK'),
                        ),
                      ],
                    ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.bold,
          color: Theme.of(context).primaryColor,
        ),
      ),
    );
  }

  Widget _buildRemoveAdsSection() {
    final l10n = AppLocalizations.of(context)!;
    final adsRemoved = AdService.instance.adsRemoved;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionHeader(l10n.removeAds),
        if (adsRemoved)
          ListTile(
            leading: const Icon(Icons.check_circle, color: Colors.green),
            title: Text(l10n.adsRemoved),
            subtitle: Text(l10n.thankYou),
          )
        else ...[
          ListTile(
            leading: const Icon(Icons.remove_circle_outline),
            title: Text(l10n.removeAds),
            subtitle: Text(
              PurchaseService.instance.getRemoveAdsPrice() ??
                  (PurchaseService.instance.isAvailable
                      ? '${l10n.loading} (Products: ${PurchaseService.instance.products.length})'
                      : '${l10n.notAvailable} - Store not available'),
            ),
            trailing: ElevatedButton(
              onPressed: () async {
                debugPrint('=== Buy button pressed ===');
                debugPrint(
                  'isAvailable: ${PurchaseService.instance.isAvailable}',
                );
                debugPrint(
                  'products: ${PurchaseService.instance.products.length}',
                );
                debugPrint(
                  'errorMessage: ${PurchaseService.instance.errorMessage}',
                );
                final result = await PurchaseService.instance.buyRemoveAds();
                debugPrint('buyRemoveAds result: $result');
              },
              child: Text(l10n.buy),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.restore),
            title: Text(l10n.restorePurchase),
            subtitle: Text(l10n.restorePurchaseDesc),
            isThreeLine: true,
            onTap: () async {
              await PurchaseService.instance.restorePurchases();
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(SnackBar(content: Text(l10n.restoring)));
            },
          ),
        ],
      ],
    );
  }
}
