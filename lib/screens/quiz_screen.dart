import 'dart:math';
import 'package:flutter/material.dart';
import 'package:sat_vocab_app/l10n/generated/app_localizations.dart';
import '../db/database_helper.dart';
import '../models/word.dart';
import '../services/translation_service.dart';
import '../services/ad_service.dart';

enum QuizType { wordToMeaning, meaningToWord }

class QuizScreen extends StatefulWidget {
  final String? level;
  final bool favoritesOnly;

  const QuizScreen({super.key, this.level, this.favoritesOnly = false});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  List<Word> _words = [];
  List<Word> _quizWords = [];
  bool _isLoading = true;
  int _currentIndex = 0;
  int _score = 0;
  int _totalQuestions = 20;
  List<String> _options = [];
  String? _selectedOption;
  bool _answered = false;
  QuizType _quizType = QuizType.wordToMeaning;
  Map<int, String> _translatedDefinitions = {};

  @override
  void initState() {
    super.initState();
    _loadWords();
  }

  Future<void> _loadWords() async {
    // JSON에서 단어 로드 (내장 번역 포함)
    final jsonWords = await DatabaseHelper.instance.getWordsWithTranslations();

    List<Word> words;
    if (widget.favoritesOnly) {
      final favorites = await DatabaseHelper.instance.getFavorites();
      final favoriteIds = favorites.map((f) => f.id).toSet();
      words = jsonWords.where((w) => favoriteIds.contains(w.id)).toList();
    } else if (widget.level != null) {
      words = jsonWords.where((w) => w.level == widget.level).toList();
    } else {
      words = jsonWords;
    }

    words.shuffle();

    // Take quiz words first
    final quizWords = words.take(_totalQuestions).toList();

    final translationService = TranslationService.instance;
    await translationService.init();
    final langCode = translationService.currentLanguage;

    // 모든 ?�어???�???�장 번역 로드 (?�답 ?�택지??번역?�어????
    if (translationService.needsTranslation) {
      for (var word in words) {
        // ?�장 번역�??�인 (API ?�출 ?�음)
        final embeddedTranslation = word.getEmbeddedTranslation(
          langCode,
          'definition',
        );
        if (embeddedTranslation != null && embeddedTranslation.isNotEmpty) {
          _translatedDefinitions[word.id] = embeddedTranslation;
        }
        // ?�장 번역 ?�으�??�어 ?�본 ?�용 (API ?�출 ?�함 - ?�즈 ?�도 ?�선)
      }
    }

    if (mounted) {
      setState(() {
        _words = words;
        _quizWords = quizWords;
        _isLoading = false;
        _generateOptions();
      });
    }
  }

  void _generateOptions() {
    if (_quizWords.isEmpty) return;

    final currentWord = _quizWords[_currentIndex];
    final correctAnswer =
        _quizType == QuizType.wordToMeaning
            ? (_translatedDefinitions[currentWord.id] ?? currentWord.definition)
            : currentWord.word;

    final wrongAnswers = <String>[];
    final usedIndices = <int>{_words.indexOf(currentWord)};

    while (wrongAnswers.length < 3 && usedIndices.length < _words.length) {
      final randomIndex = Random().nextInt(_words.length);
      if (!usedIndices.contains(randomIndex)) {
        usedIndices.add(randomIndex);
        final wrongWord = _words[randomIndex];
        final wrongAnswer =
            _quizType == QuizType.wordToMeaning
                ? (_translatedDefinitions[wrongWord.id] ?? wrongWord.definition)
                : wrongWord.word;
        if (wrongAnswer != correctAnswer) {
          wrongAnswers.add(wrongAnswer);
        }
      }
    }

    _options = [correctAnswer, ...wrongAnswers]..shuffle();
  }

  void _checkAnswer(String selectedOption) {
    if (_answered) return;

    final currentWord = _quizWords[_currentIndex];
    final correctAnswer =
        _quizType == QuizType.wordToMeaning
            ? (_translatedDefinitions[currentWord.id] ?? currentWord.definition)
            : currentWord.word;

    setState(() {
      _answered = true;
      _selectedOption = selectedOption;
      if (selectedOption == correctAnswer) {
        _score++;
      }
    });
  }

  void _nextQuestion() {
    if (_currentIndex < _quizWords.length - 1) {
      setState(() {
        _currentIndex++;
        _answered = false;
        _selectedOption = null;
        _generateOptions();
      });
    } else {
      _showResultDialog();
    }
  }

  void _showResultDialog() async {
    final adService = AdService.instance;
    if (!adService.adsRemoved) {
      await adService.showInterstitialAd();
    }

    if (!mounted) return;

    final l10n = AppLocalizations.of(context)!;
    final percentage = (_score / _quizWords.length * 100).round();

    showDialog(
      context: context,
      barrierDismissible: false,
      builder:
          (context) => AlertDialog(
            title: Text(l10n.quizComplete),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  percentage >= 80
                      ? Icons.emoji_events
                      : percentage >= 60
                      ? Icons.thumb_up
                      : Icons.refresh,
                  size: 60,
                  color:
                      percentage >= 80
                          ? Colors.amber
                          : percentage >= 60
                          ? Colors.green
                          : Colors.orange,
                ),
                const SizedBox(height: 16),
                Text(
                  '$_score / ${_quizWords.length}',
                  style: const TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  '$percentage%',
                  style: TextStyle(fontSize: 20, color: Colors.grey[600]),
                ),
                const SizedBox(height: 8),
                Text(
                  _getResultMessage(percentage),
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 16),
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                },
                child: Text(l10n.finish),
              ),
              ElevatedButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  _restartQuiz();
                },
                child: Text(l10n.tryAgain),
              ),
            ],
          ),
    );
  }

  String _getResultMessage(int percentage) {
    final l10n = AppLocalizations.of(context)!;
    if (percentage >= 90) return l10n.excellent;
    if (percentage >= 80) return l10n.great;
    if (percentage >= 60) return l10n.good;
    return l10n.keepPracticing;
  }

  void _restartQuiz() {
    setState(() {
      _words.shuffle();
      _quizWords = _words.take(_totalQuestions).toList();
      _currentIndex = 0;
      _score = 0;
      _answered = false;
      _selectedOption = null;
      _generateOptions();
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.quiz)),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_quizWords.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.quiz)),
        body: Center(child: Text(l10n.cannotLoadWords)),
      );
    }

    final currentWord = _quizWords[_currentIndex];
    final correctAnswer =
        _quizType == QuizType.wordToMeaning
            ? (_translatedDefinitions[currentWord.id] ?? currentWord.definition)
            : currentWord.word;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.quiz),
        actions: [
          PopupMenuButton<QuizType>(
            icon: const Icon(Icons.swap_horiz),
            onSelected: (type) {
              setState(() {
                _quizType = type;
                _restartQuiz();
              });
            },
            itemBuilder:
                (context) => [
                  PopupMenuItem(
                    value: QuizType.wordToMeaning,
                    child: Text(l10n.wordToMeaning),
                  ),
                  PopupMenuItem(
                    value: QuizType.meaningToWord,
                    child: Text(l10n.meaningToWord),
                  ),
                ],
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Progress
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '${l10n.question} ${_currentIndex + 1}/${_quizWords.length}',
                  style: const TextStyle(fontSize: 16),
                ),
                Text(
                  '${l10n.score}: $_score',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(
              value: (_currentIndex + 1) / _quizWords.length,
              backgroundColor: Colors.grey[300],
            ),
            const SizedBox(height: 24),

            // Question Card
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: Theme.of(
                          context,
                        ).primaryColor.withAlpha((0.1 * 255).toInt()),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        currentWord.level,
                        style: TextStyle(
                          color: Theme.of(context).primaryColor,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      _quizType == QuizType.wordToMeaning
                          ? currentWord.word
                          : (_translatedDefinitions[currentWord.id] ??
                              currentWord.definition),
                      style: TextStyle(
                        fontSize: _quizType == QuizType.wordToMeaning ? 28 : 18,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Options
            Expanded(
              child: ListView.builder(
                itemCount: _options.length,
                itemBuilder: (context, index) {
                  final option = _options[index];
                  final isCorrect = option == correctAnswer;
                  final isSelected = option == _selectedOption;

                  Color? backgroundColor;
                  Color? borderColor;
                  if (_answered) {
                    if (isCorrect) {
                      backgroundColor = Colors.green.withAlpha(
                        (0.2 * 255).toInt(),
                      );
                      borderColor = Colors.green;
                    } else if (isSelected) {
                      backgroundColor = Colors.red.withAlpha(
                        (0.2 * 255).toInt(),
                      );
                      borderColor = Colors.red;
                    }
                  }

                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: BorderSide(
                        color: borderColor ?? Colors.transparent,
                        width: 2,
                      ),
                    ),
                    color: backgroundColor,
                    child: ListTile(
                      onTap: _answered ? null : () => _checkAnswer(option),
                      title: Text(
                        option,
                        style: TextStyle(
                          fontSize:
                              _quizType == QuizType.meaningToWord ? 18 : 14,
                        ),
                      ),
                      trailing:
                          _answered
                              ? Icon(
                                isCorrect
                                    ? Icons.check_circle
                                    : (isSelected ? Icons.cancel : null),
                                color: isCorrect ? Colors.green : Colors.red,
                              )
                              : null,
                    ),
                  );
                },
              ),
            ),

            // Next Button
            if (_answered)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _nextQuestion,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: Text(
                    _currentIndex < _quizWords.length - 1
                        ? l10n.next
                        : l10n.showResult,
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
