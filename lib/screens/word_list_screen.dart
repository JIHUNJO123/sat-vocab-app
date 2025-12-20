import 'package:flutter/material.dart';
import 'package:flip_card/flip_card.dart';
import 'package:jlpt_vocab_app/l10n/generated/app_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';
import '../db/database_helper.dart';
import '../models/word.dart';
import '../services/translation_service.dart';
import '../services/ad_service.dart';
import '../services/display_service.dart';
import 'word_detail_screen.dart';

class WordListScreen extends StatefulWidget {
  final String? level;
  final bool isFlashcardMode;

  const WordListScreen({super.key, this.level, this.isFlashcardMode = false});

  @override
  State<WordListScreen> createState() => _WordListScreenState();
}

class _WordListScreenState extends State<WordListScreen> {
  List<Word> _words = [];
  List<Word> _allWords = []; // Keep all words for filtering
  bool _isLoading = true;
  int _currentFlashcardIndex = 0;
  late PageController _pageController;
  String _sortOrder = 'alphabetical';
  String? _selectedBandFilter; // Band filter for All Words view
  bool _isBannerAdLoaded = false;
  double _wordFontSize = 1.0;
  bool _showNativeLanguage = true;
  bool _showBandBadge = true; // Band 諛곗? ?쒖떆 ?щ?

  final ScrollController _listScrollController = ScrollController();

  Map<int, String> _translatedDefinitions = {};
  Map<int, String> _translatedExamples = {};

  String get _positionKey =>
      'word_list_position_${widget.level ?? 'all'}_${widget.isFlashcardMode ? 'flashcard' : 'list'}';

  String get _scrollOffsetKey =>
      'word_list_scroll_offset_${widget.level ?? 'all'}';

  Future<void> _restoreScrollPosition() async {
    if (widget.isFlashcardMode) return;
    final prefs = await SharedPreferences.getInstance();
    final offset = prefs.getDouble(_scrollOffsetKey) ?? 0.0;
    if (offset > 0) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_listScrollController.hasClients && mounted) {
          _listScrollController.jumpTo(offset);
        }
      });
    }
  }

  Future<void> _saveScrollPosition() async {
    if (_listScrollController.hasClients) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setDouble(_scrollOffsetKey, _listScrollController.offset);
    }
  }

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _loadWords();
    _loadBannerAd();
    _loadInterstitialAd();
    _loadFontSize();
  }

  Future<void> _loadInterstitialAd() async {
    final adService = AdService.instance;
    await adService.initialize();
    if (!adService.adsRemoved) {
      await adService.loadInterstitialAd();
    }
  }

  Future<void> _loadFontSize() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _wordFontSize = prefs.getDouble('wordFontSize') ?? 1.0;
    });
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

  Future<void> _loadWords() async {
    List<Word> words;
    if (widget.level != null) {
      words = await DatabaseHelper.instance.getWordsByLevel(widget.level!);
    } else {
      words = await DatabaseHelper.instance.getAllWords();
    }

    final prefs = await SharedPreferences.getInstance();
    final savedPosition = prefs.getInt(_positionKey) ?? 0;

    setState(() {
      _allWords = words; // Keep original list
      _words = words;
      _isLoading = false;
    });

    if (words.isNotEmpty) {
      final position = savedPosition.clamp(0, words.length - 1);
      if (widget.isFlashcardMode) {
        _currentFlashcardIndex = position;
        _pageController = PageController(initialPage: position);
        setState(() {});
      } else {
        _restoreScrollPosition();
      }
    }
  }

  void _filterByBand(String? band) {
    setState(() {
      _selectedBandFilter = band;
      if (band == null) {
        _words = List.from(_allWords);
      } else {
        _words = _allWords.where((w) => w.level == band).toList();
      }
      _currentFlashcardIndex = 0;
      if (_pageController.hasClients) {
        _pageController.jumpToPage(0);
      }
    });
  }

  Future<void> _savePosition(int position) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_positionKey, position);
  }

  Future<void> _loadTranslationForWord(Word word) async {
    if (_translatedDefinitions.containsKey(word.id)) return;

    final translationService = TranslationService.instance;
    await translationService.init();

    if (!translationService.needsTranslation) return;
    if (!mounted) return;

    // ?댁옣 踰덉뿭留??ъ슜 (API ?몄텧 ?놁쓬)
    final langCode = translationService.currentLanguage;
    final embeddedDef = word.getEmbeddedTranslation(langCode, 'definition');
    final embeddedEx = word.getEmbeddedTranslation(langCode, 'example');

    if (!mounted) return;
    if (embeddedDef != null && embeddedDef.isNotEmpty) {
      setState(() {
        _translatedDefinitions[word.id] = embeddedDef;
        if (embeddedEx != null && embeddedEx.isNotEmpty) {
          _translatedExamples[word.id] = embeddedEx;
        }
      });
    }
  }

  void _sortWords(String order) {
    final currentWord =
        _words.isNotEmpty ? _words[_currentFlashcardIndex] : null;

    setState(() {
      _sortOrder = order;
      if (order == 'alphabetical') {
        _words.sort(
          (a, b) => a.word.toLowerCase().compareTo(b.word.toLowerCase()),
        );
      } else if (order == 'random') {
        _words.shuffle();
      }

      if (currentWord != null) {
        final newIndex = _words.indexWhere((w) => w.id == currentWord.id);
        _currentFlashcardIndex = newIndex >= 0 ? newIndex : 0;
      } else {
        _currentFlashcardIndex = 0;
      }

      if (_pageController.hasClients) {
        _pageController.jumpToPage(_currentFlashcardIndex);
      }
    });
  }

  Future<void> _toggleFavorite(Word word) async {
    await DatabaseHelper.instance.toggleFavorite(word.id, !word.isFavorite);
    setState(() {
      word.isFavorite = !word.isFavorite;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          word.isFavorite
              ? AppLocalizations.of(context)!.addedToFavorites
              : AppLocalizations.of(context)!.removedFromFavorites,
        ),
        duration: const Duration(seconds: 1),
      ),
    );
  }

  Color _getLevelColor(String level) {
    switch (level) {
      case 'N5':
        return Colors.green;
      case 'N4':
        return Colors.blue;
      case 'N3':
        return Colors.orange;
      case 'N2':
        return Colors.purple;
      case 'N1':
        return Colors.red;
      default:
        return Colors.blue;
    }
  }

  void _showBandFilterDialog() {
    final l10n = AppLocalizations.of(context)!;
    final bands = [
      {'level': null, 'name': l10n.allWords, 'color': Colors.grey},
      {'level': 'N5', 'name': 'N5', 'color': Colors.green},
      {'level': 'N4', 'name': 'N4', 'color': Colors.blue},
      {'level': 'N3', 'name': 'N3', 'color': Colors.orange},
      {'level': 'N2', 'name': 'N2', 'color': Colors.purple},
      {'level': 'N1', 'name': 'N1', 'color': Colors.red},
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
              children: [
                Text(
                  l10n.levelLearning,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                ...bands.map(
                  (band) => ListTile(
                    leading: CircleAvatar(
                      backgroundColor: band['color'] as Color,
                      radius: 12,
                    ),
                    title: Text(band['name'] as String),
                    trailing:
                        _selectedBandFilter == band['level']
                            ? Icon(
                              Icons.check,
                              color: Theme.of(context).primaryColor,
                            )
                            : null,
                    onTap: () {
                      Navigator.pop(context);
                      _filterByBand(band['level'] as String?);
                    },
                  ),
                ),
                const SizedBox(height: 16),
              ],
            ),
          ),
    );
  }

  Future<bool> _handleBackPress() async {
    if (widget.isFlashcardMode) {
      final adService = AdService.instance;
      if (!adService.adsRemoved && adService.isInterstitialAdLoaded) {
        await adService.showInterstitialAd();
      }
    }
    return true;
  }

  @override
  void dispose() {
    if (!widget.isFlashcardMode) {
      _saveScrollPosition();
    }
    _pageController.dispose();
    _listScrollController.dispose();
    AdService.instance.disposeBannerAd();
    if (widget.isFlashcardMode) {
      _savePosition(_currentFlashcardIndex);
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    String title = l10n.allWords;
    if (widget.level != null) {
      title = l10n.levelWords(widget.level!);
    }
    if (widget.isFlashcardMode) {
      title = l10n.flashcard;
    }

    return Scaffold(
      appBar: AppBar(
        leading: widget.isFlashcardMode
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: () async {
                  if (await _handleBackPress()) {
                    if (context.mounted) Navigator.of(context).pop();
                  }
                },
              )
            : null,
        title: Column(
          children: [
            Text(title),
            if (_selectedBandFilter != null)
              Text(
                _selectedBandFilter!,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.normal,
                ),
              ),
          ],
        ),
        centerTitle: true,
        actions: [
          // Band 諛곗? ?쒖떆 ?좉? 踰꾪듉 (All Words 由ъ뒪?몄뿉?쒕쭔)
          if (widget.level == null &&
              !widget.isFlashcardMode &&
              _words.isNotEmpty)
            IconButton(
              icon: Icon(
                _showBandBadge ? Icons.label : Icons.label_off,
                color: _showBandBadge ? Theme.of(context).primaryColor : null,
              ),
              tooltip: 'Toggle Band Badge',
              onPressed: () {
                setState(() {
                  _showBandBadge = !_showBandBadge;
                });
              },
            ),
          // Band filter button (All Words? Flashcard 紐⑤뱶 紐⑤몢?먯꽌 ?ъ슜 媛??
          if (widget.level == null && _words.isNotEmpty)
            IconButton(
              icon: Icon(
                Icons.filter_list,
                color:
                    _selectedBandFilter != null
                        ? Theme.of(context).primaryColor
                        : null,
              ),
              onPressed: _showBandFilterDialog,
            ),
          if (_words.isNotEmpty && TranslationService.instance.needsTranslation)
            IconButton(
              icon: Icon(
                _showNativeLanguage ? Icons.translate : Icons.language,
                color:
                    _showNativeLanguage ? Theme.of(context).primaryColor : null,
              ),
              onPressed: () {
                setState(() {
                  _showNativeLanguage = !_showNativeLanguage;
                });
              },
            ),
          if (_words.isNotEmpty)
            PopupMenuButton<String>(
              icon: const Icon(Icons.sort),
              onSelected: _sortWords,
              itemBuilder:
                  (context) => [
                    PopupMenuItem(
                      value: 'alphabetical',
                      child: Row(
                        children: [
                          Icon(
                            Icons.sort_by_alpha,
                            color:
                                _sortOrder == 'alphabetical'
                                    ? Theme.of(context).primaryColor
                                    : null,
                          ),
                          const SizedBox(width: 8),
                          Text(l10n.alphabetical),
                        ],
                      ),
                    ),
                    PopupMenuItem(
                      value: 'random',
                      child: Row(
                        children: [
                          Icon(
                            Icons.shuffle,
                            color:
                                _sortOrder == 'random'
                                    ? Theme.of(context).primaryColor
                                    : null,
                          ),
                          const SizedBox(width: 8),
                          Text(l10n.random),
                        ],
                      ),
                    ),
                  ],
            ),
        ],
      ),
      body:
          _isLoading
              ? const Center(child: CircularProgressIndicator())
              : _words.isEmpty
              ? Center(child: Text(l10n.cannotLoadWords))
              : Column(
                children: [
                  Expanded(
                    child:
                        widget.isFlashcardMode
                            ? _buildFlashcardView()
                            : _buildListView(),
                  ),
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

  Widget _buildListView() {
    return ListView.builder(
      controller: _listScrollController,
      padding: const EdgeInsets.all(16),
      itemCount: _words.length,
      itemBuilder: (context, index) {
        final word = _words[index];
        _loadTranslationForWord(word);

        final definition =
            _showNativeLanguage && _translatedDefinitions.containsKey(word.id)
                ? _translatedDefinitions[word.id]!
                : word.definition;

        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => WordDetailScreen(word: word),
                ),
              );
            },
            title: Row(
              children: [
                Expanded(
                  child: Text(
                    word.getDisplayWord(displayMode: DisplayService.instance.displayMode),
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16 * _wordFontSize,
                    ),
                  ),
                ),
                // Band 諛곗?: All Words?먯꽌 ?좉? 媛??
                if (widget.level == null && _showBandBadge)
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: _getLevelColor(word.level),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      word.level,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
              ],
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 4),
                Row(
                  children: [
                    Text(
                      word.partOfSpeech,
                      style: TextStyle(color: Colors.grey[600], fontSize: 12),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  definition,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(fontSize: 14 * _wordFontSize),
                ),
              ],
            ),
            trailing: IconButton(
              icon: Icon(
                word.isFavorite ? Icons.favorite : Icons.favorite_border,
                color: word.isFavorite ? Colors.red : null,
              ),
              onPressed: () => _toggleFavorite(word),
            ),
          ),
        );
      },
    );
  }

  Widget _buildFlashcardView() {
    final l10n = AppLocalizations.of(context)!;

    return Column(
      children: [
        // Progress indicator
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                '${_currentFlashcardIndex + 1} / ${_words.length}',
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
        ),
        // Flashcard
        Expanded(
          child: PageView.builder(
            controller: _pageController,
            itemCount: _words.length,
            onPageChanged: (index) {
              setState(() {
                _currentFlashcardIndex = index;
              });
              _savePosition(index);
              _loadTranslationForWord(_words[index]);
            },
            itemBuilder: (context, index) {
              final word = _words[index];
              _loadTranslationForWord(word);

              final definition =
                  _showNativeLanguage &&
                          _translatedDefinitions.containsKey(word.id)
                      ? _translatedDefinitions[word.id]!
                      : word.definition;
              final example =
                  _showNativeLanguage &&
                          _translatedExamples.containsKey(word.id)
                      ? _translatedExamples[word.id]!
                      : word.example;

              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24.0),
                child: FlipCard(
                  direction: FlipDirection.HORIZONTAL,
                  front: Card(
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(20),
                        gradient: LinearGradient(
                          colors: [
                            _getLevelColor(word.level),
                            _getLevelColor(
                              word.level,
                            ).withAlpha((0.7 * 255).toInt()),
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(24.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
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
                                    color: Colors.white.withAlpha(
                                      (0.2 * 255).toInt(),
                                    ),
                                    borderRadius: BorderRadius.circular(20),
                                  ),
                                  child: Text(
                                    word.partOfSpeech,
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                                IconButton(
                                  icon: Icon(
                                    word.isFavorite
                                        ? Icons.favorite
                                        : Icons.favorite_border,
                                    color:
                                        word.isFavorite
                                            ? Colors.red
                                            : Colors.white,
                                  ),
                                  onPressed: () => _toggleFavorite(word),
                                ),
                              ],
                            ),
                            const Spacer(),
                            Text(
                              word.getDisplayWord(displayMode: DisplayService.instance.displayMode),
                              style: TextStyle(
                                fontSize: 28 * _wordFontSize,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 16),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 12,
                                vertical: 6,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.white.withAlpha(
                                  (0.2 * 255).toInt(),
                                ),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                word.level,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 14,
                                ),
                              ),
                            ),
                            const Spacer(),
                            Text(
                              l10n.tapToFlip,
                              style: TextStyle(
                                color: Colors.white.withAlpha(
                                  (0.8 * 255).toInt(),
                                ),
                                fontSize: 14,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                  back: Card(
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.lightbulb_outline,
                            size: 40,
                            color: Theme.of(context).primaryColor,
                          ),
                          const SizedBox(height: 16),
                          Text(
                            l10n.definition,
                            style: TextStyle(
                              fontSize: 14,
                              color: Theme.of(context).primaryColor,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            definition,
                            style: TextStyle(
                              fontSize: 18 * _wordFontSize,
                              height: 1.5,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 24),
                          Text(
                            l10n.example,
                            style: TextStyle(
                              fontSize: 14,
                              color: Theme.of(context).primaryColor,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            word.example, // Always show example in English
                            style: TextStyle(
                              fontSize: 16 * _wordFontSize,
                              fontStyle: FontStyle.italic,
                              color: Colors.grey[700],
                              height: 1.5,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
        // Navigation buttons
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              ElevatedButton.icon(
                onPressed:
                    _currentFlashcardIndex > 0
                        ? () {
                          _pageController.previousPage(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        }
                        : null,
                icon: const Icon(Icons.chevron_left),
                label: Text(l10n.previous),
              ),
              ElevatedButton.icon(
                onPressed:
                    _currentFlashcardIndex < _words.length - 1
                        ? () {
                          _pageController.nextPage(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                          );
                        }
                        : null,
                icon: const Icon(Icons.chevron_right),
                label: Text(l10n.next),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

