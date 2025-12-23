import 'package:flutter/material.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import '../db/database_helper.dart';
import '../models/word.dart';
import '../services/translation_service.dart';
import '../services/ad_service.dart';
import 'word_list_screen.dart';
import 'word_detail_screen.dart';
import 'favorites_screen.dart';
import 'quiz_screen.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Word? _todayWord;
  String? _translatedDefinition;
  bool _isLoading = true;
  bool _isBannerAdLoaded = false;
  String? _lastLanguage;

  @override
  void initState() {
    super.initState();
    _loadTodayWord();
    _loadBannerAd();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final currentLanguage = TranslationService.instance.currentLanguage;
    if (_lastLanguage != null && _lastLanguage != currentLanguage) {
      _loadTodayWord();
    }
    _lastLanguage = currentLanguage;
  }

  Future<void> _loadBannerAd() async {
    final adService = AdService.instance;
    await adService.initialize();

    if (!adService.adsRemoved) {
      await adService.loadBannerAd(
        onLoaded: () {
          if (mounted) {
            setState(() {
              _isBannerAdLoaded = true;
            });
          }
        },
      );
    }
  }

  Future<void> _loadTodayWord() async {
    try {
      final word = await DatabaseHelper.instance.getTodayWord();
      if (word != null) {
        final translationService = TranslationService.instance;
        await translationService.init();

        if (translationService.needsTranslation) {
          // ?댁옣 踰덉뿭留??ъ슜 (API ?몄텧 ?놁쓬)
          final embeddedTranslation = word.getEmbeddedTranslation(
            translationService.currentLanguage,
            'definition',
          );

          if (mounted) {
            setState(() {
              _todayWord = word;
              _translatedDefinition = embeddedTranslation;
              _isLoading = false;
            });
          }
        } else {
          if (mounted) {
            setState(() {
              _todayWord = word;
              _translatedDefinition = null;
              _isLoading = false;
            });
          }
        }
      } else {
        if (mounted) {
          setState(() {
            _todayWord = null;
            _isLoading = false;
          });
        }
      }
    } catch (e) {
      print('Error loading today word: $e');
      if (mounted) {
        setState(() {
          _todayWord = null;
          _isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    AdService.instance.disposeBannerAd();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          l10n.appTitle,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Today's Word Card
                  _buildTodayWordCard(),
                  const SizedBox(height: 24),

                  // Quick Actions
                  Text(
                    l10n.learning,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  _buildMenuGrid(),

                  const SizedBox(height: 24),

                  // Difficulty Level
                  Text(
                    l10n.levelLearning,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  _buildLevelCards(),
                ],
              ),
            ),
          ),
          // 諛곕꼫 愿묎퀬
          _buildBannerAd(),
        ],
      ),
    );
  }

  Widget _buildBannerAd() {
    final adService = AdService.instance;

    if (adService.adsRemoved ||
        !_isBannerAdLoaded ||
        adService.bannerAd == null) {
      return const SizedBox.shrink();
    }

    return Container(
      width: adService.bannerAd!.size.width.toDouble(),
      height: adService.bannerAd!.size.height.toDouble(),
      alignment: Alignment.center,
      child: AdWidget(ad: adService.bannerAd!),
    );
  }

  Widget _buildTodayWordCard() {
    final l10n = AppLocalizations.of(context)!;

    if (_isLoading) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(24.0),
          child: Center(child: CircularProgressIndicator()),
        ),
      );
    }

    if (_todayWord == null) {
      return Card(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Center(child: Text(l10n.cannotLoadWords)),
        ),
      );
    }

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => WordDetailScreen(word: _todayWord!),
            ),
          );
        },
        borderRadius: BorderRadius.circular(16),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(24.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            gradient: LinearGradient(
              colors: [
                Theme.of(context).primaryColor,
                Theme.of(context).primaryColor.withAlpha((0.7 * 255).toInt()),
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white.withAlpha((0.2 * 255).toInt()),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      "\u{1F4C5} ${l10n.todayWord}",
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white.withAlpha((0.2 * 255).toInt()),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      _todayWord!.level,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  Expanded(
                    child: Text(
                      _todayWord!.word,
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                _translatedDefinition ?? _todayWord!.definition,
                style: const TextStyle(fontSize: 16, color: Colors.white),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMenuGrid() {
    final l10n = AppLocalizations.of(context)!;

    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: 1.3,
      children: [
        _buildMenuCard(
          icon: Icons.list_alt,
          title: l10n.allWords,
          subtitle: l10n.viewAllWords,
          color: Colors.blue,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const WordListScreen()),
            );
          },
        ),
        _buildMenuCard(
          icon: Icons.favorite,
          title: l10n.favorites,
          subtitle: l10n.savedWords,
          color: Colors.red,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const FavoritesScreen()),
            );
          },
        ),
        _buildMenuCard(
          icon: Icons.style,
          title: l10n.flashcard,
          subtitle: l10n.cardLearning,
          color: Colors.orange,
          onTap: () => _showLevelSelectionDialog(isQuiz: false),
        ),
        _buildMenuCard(
          icon: Icons.quiz,
          title: l10n.quiz,
          subtitle: l10n.testYourself,
          color: Colors.green,
          onTap: () => _showLevelSelectionDialog(isQuiz: true),
        ),
      ],
    );
  }

  Widget _buildMenuCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 10.0),
          child: Row(
            children: [
              Icon(icon, size: 36, color: color),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 2),
                    Text(
                      subtitle,
                      style: TextStyle(color: Colors.grey[600], fontSize: 11),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLevelCards() {
    final l10n = AppLocalizations.of(context)!;

    // SAT Level 湲곗? ?덈꺼 (??泥닿퀎)
    final levels = [
      {
        'level': 'Basic',
        'name': l10n.basic,
        'desc': l10n.basicDesc,
        'color': Colors.green,
      },
      {
        'level': 'Common',
        'name': l10n.common,
        'desc': l10n.commonDesc,
        'color': Colors.blue,
      },
      {
        'level': 'Advanced',
        'name': l10n.advanced,
        'desc': l10n.advancedDesc,
        'color': Colors.orange,
      },
      {
        'level': 'Expert',
        'name': l10n.expert,
        'desc': l10n.expertDesc,
        'color': Colors.red,
      },
    ];

    return SizedBox(
      height: 120,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: levels.length,
        itemBuilder: (context, index) {
          final level = levels[index];
          return Container(
            width: 140,
            margin: const EdgeInsets.only(right: 10),
            child: Card(
              elevation: 2,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: InkWell(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder:
                          (context) =>
                              WordListScreen(level: level['level'] as String),
                    ),
                  );
                },
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    gradient: LinearGradient(
                      colors: [
                        (level['color'] as Color).withAlpha(
                          (0.8 * 255).toInt(),
                        ),
                        (level['color'] as Color),
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8.0,
                      vertical: 10.0,
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          level['level'] as String,
                          style: const TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          level['desc'] as String,
                          style: const TextStyle(
                            fontSize: 9,
                            color: Colors.white70,
                          ),
                          textAlign: TextAlign.center,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  void _showLevelSelectionDialog({required bool isQuiz}) {
    final l10n = AppLocalizations.of(context)!;
    final levels = [
      {
        'level': null,
        'name': l10n.allWords,
        'color': Colors.grey,
        'icon': Icons.all_inclusive,
      },
      {
        'level': 'favorites',
        'name': l10n.favorites,
        'color': Colors.red,
        'icon': Icons.favorite,
      },
      {
        'level': 'Basic',
        'name': 'Basic',
        'color': Colors.green,
        'icon': Icons.looks_one,
      },
      {
        'level': 'Common',
        'name': 'Common',
        'color': Colors.blue,
        'icon': Icons.looks_two,
      },
      {
        'level': 'Advanced',
        'name': 'Advanced',
        'color': Colors.orange,
        'icon': Icons.looks_3,
      },
      {
        'level': 'Expert',
        'name': 'Expert',
        'color': Colors.red,
        'icon': Icons.looks_4,
      },
    ];

    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder:
          (context) => Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  isQuiz ? l10n.quiz : l10n.flashcard,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                ...levels.map(
                  (level) => ListTile(
                    leading: Icon(
                      level['icon'] as IconData,
                      color: level['color'] as Color,
                    ),
                    title: Text(level['name'] as String),
                    onTap: () {
                      Navigator.pop(context);
                      final selectedLevel = level['level'] as String?;
                      if (isQuiz) {
                        if (selectedLevel == 'favorites') {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder:
                                  (context) =>
                                      const QuizScreen(favoritesOnly: true),
                            ),
                          );
                        } else {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder:
                                  (context) => QuizScreen(level: selectedLevel),
                            ),
                          );
                        }
                      } else {
                        if (selectedLevel == 'favorites') {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder:
                                  (context) => const WordListScreen(
                                    isFlashcardMode: true,
                                    favoritesOnly: true,
                                  ),
                            ),
                          );
                        } else {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder:
                                  (context) => WordListScreen(
                                    level: selectedLevel,
                                    isFlashcardMode: true,
                                  ),
                            ),
                          );
                        }
                      }
                    },
                  ),
                ),
                const SizedBox(height: 8),
                SizedBox(
                  width: double.infinity,
                  child: TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: Text(l10n.cancel),
                  ),
                ),
              ],
            ),
          ),
    );
  }
}
