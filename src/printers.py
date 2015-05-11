# -*- coding: utf-8 -*-

# Python import
import sys

# Local import
import settings

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#following from Python cookbook, #475186
def has_colors(stream):
  if not hasattr(stream, "isatty") or not stream.isatty():
    return False
  try:
    import curses
    curses.setupterm()
    return curses.tigetnum("colors") > 2
  except:
    return False

has_colors = has_colors(sys.stdout)

def printout(text, color=WHITE):
  if has_colors:
    seq = "\x1b[1;%dm" % (30+color) + text + "\x1b[0m"
    return seq
  else:
    return text

class LocalPrinter:
  """
  Print all outputs on standard output, with all the colors and stuff
  """
  def __init__(self, verbosity):
    self.verbosity = verbosity

  def printErrorNoSetFound(self):
    """
    Print 'ErrorNoSetFound' error message
    """
    print printout(settings.strings['errorNoSetFound'], settings.colors['errors'])

  def printIntro(self):
    """
    Print the intro sentence, before testing starts
    """
    print printout(settings.strings['intro'], settings.colors['intro'])

  def printSetIntro(self, u):
    """
    Print the set intro sentence, before the beginning of each test set
    """
    if self.verbosity > 0:
      print printout(u.__class__.__name__ + ': ' + u.__doc__, settings.colors['setIntro'])

  def printTestOutput(self, data, doc):
    """
    Print the output of a test
    """
    if data['success']:
      success = printout(settings.strings['testSuccess'], settings.colors['testSuccess'])
    else:
      success = printout(settings.strings['testFailure'], settings.colors['testFailure'])

    output = settings.strings['testOutputFormat'].format(success=success, return_code=data['code'], elapsed=data['elapsed'], doc=doc)

    if self.verbosity > 1:
      print output

  def printTestDirtyFailure(self, data):
    """
    Print the output of a dirty failed test (aka Exception was thrown during test execution)
    """
    output = printout(settings.strings['testDirtyFailure'], settings.colors['testDirtyFailure']) + str(data['exception'])

    if self.verbosity > 1:
      print output

  def printSetResult(self, test_set, nb_tests, nb_ok, total_response_time):
    """
    Print set results, after the end of each test set
    """
    if self.verbosity > 0:
      percent = int(100 * (float(nb_ok) / float(nb_tests)))
      print printout(
        settings.strings['setResult'].format(nb_tests_passed=nb_ok,
                                             nb_tests_total=nb_tests,
                                             percent=percent,
                                             className=test_set.__class__.__name__),
        settings.colors['setResult'])

  def printTotalResult(self, nb_tests, nb_ok, total_response_time):
    """
    Print total results, after the end of all test sets
    """
    percent = int(100 * (float(nb_ok) / float(nb_tests)))
    print printout(
      settings.strings['totalResult'].format(nb_tests_passed=nb_ok,
                                             nb_tests_total=nb_tests,
                                             percent=percent),
      settings.colors['totalResult'])

    if percent == 100:
      print printout(settings.strings['buildOk'], settings.colors['buildOk'])
    else:
      print printout(settings.strings['buildKo'], settings.colors['buildKo'])


class WebPrinter:
  """
  Send all output JSON encoded through websocket, to the client who ordered the test session.
  """
  def __init__(self, verbosity, websocket):
    self.verbosity = verbosity
    self.websocket = websocket

  def encapsulate(self, success, category, message):
    return {'success': success, 'category': category, 'object': message}

  def printErrorNoSetFound(self):
    """
    Print 'ErrorNoSetFound' error message
    """
    self.websocket.write_message(False, 'error', self.encapsulate(settings.strings['errorNoSetFound']))

  def printIntro(self):
    """
    Print the intro sentence, before testing starts
    """
    self.websocket.write_message(self.encapsulate(True, 'intro', settings.strings['intro']))

  def printSetIntro(self, u):
    """
    Print the set intro sentence, before the beginning of each test set
    """
    if self.verbosity > 0:
      self.websocket.write_message(self.encapsulate(True, 'test_set_intro', u.__class__.__name__ + ': ' + u.__doc__))

  def printTestOutput(self, data, doc):
    """
    Print the output of a test
    """
    output = {'code': data['code'], 'response_time': str(data['elapsed']), 'doc': doc}

    if self.verbosity > 1:
      self.websocket.write_message(self.encapsulate(data['success'], 'test_output', output))

  def printTestDirtyFailure(self, data):
    """
    Print the output of a dirty failed test (aka Exception was thrown during test execution)
    """
    output = {'exception': str(data['exception'])}

    if self.verbosity > 1:
      self.websocket.write_message(self.encapsulate(False, 'error', output))

  def printSetResult(self, test_set, nb_tests, nb_ok, total_response_time):
    """
    Print set results, after the end of each test set
    """
    if self.verbosity > 0:
      percent = int(100 * (float(nb_ok) / float(nb_tests)))
      output = {'nb_tests_passed': nb_ok, 'nb_tests_total': nb_tests, 'percentage': percent, 'class_name': test_set.__class__.__name__}
      self.websocket.write_message(self.encapsulate(True, 'test_set_result', output))

  def printTotalResult(self, nb_tests, nb_ok, total_response_time):
    """
    Print total results, after the end of all test sets
    """
    percent = int(100 * (float(nb_ok) / float(nb_tests)))
    output = {'nb_tests_passed': nb_ok, 'nb_tests': nb_tests, 'percentage': percent}
    self.websocket.write_message(self.encapsulate(True, 'total_result', output))

    if percent == 100:
      self.websocket.write_message(self.encapsulate(True, 'build_result', settings.strings['buildOk']))
    else:
      self.websocket.write_message(self.encapsulate(False, 'build_result', settings.strings['buildKo']))
