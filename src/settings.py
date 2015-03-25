# -*- coding: utf-8 -*-

sets = [
  'usecase1',
]

strings = {
  'intro': 'Launching tests\n',
  'setResult': 'Total for {className} : {nb_tests_passed} / {nb_tests_total} successful tests ({percent}%)\n---\n',
  'totalResult': 'Total : {nb_tests_passed} / {nb_tests_total} successful tests ({percent}%)',
  'buildOk': '\n\n  [BUILD: OK]\n\n',
  'buildKo': '\n\n  [BUILD: KO]\n\n',
  'testOutputFormat': '[{success}] [code : {return_code}] [{elapsed}ms] {doc}',
  'testSuccess': 'OK',
  'testFailure': 'KO',
  'testDirtyFailure': '[KO] [DIRTY]',

  'errorNoSetFound': 'No tests found. Exiting.',

}

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

colors = {
  'intro': MAGENTA,
  'setIntro': CYAN,
  'setResult': CYAN,
  'totalResult': MAGENTA,
  'buildOk': GREEN,
  'buildKo': RED,
  'testSuccess': GREEN,
  'testFailure': RED,
  'testDirtyFailure': RED,
  'errors': RED,
}