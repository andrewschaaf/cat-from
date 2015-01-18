import subprocess, unittest


class OffsetTests(unittest.TestCase):

  def test_empty_file(self):
    assert_succeeds_with("", ['--offset', '0', '%s/empty-file' % FIXTURES_DIR])

  def test_file_larger_than_buffer(self):
    with open('%s/larger-than-buffer' % FIXTURES_DIR, "wb") as f:
      f.write('0123456789' * 3300)
    expected = '456789' + ('0123456789' * 3299)
    assert_succeeds_with(expected, ['--offset', '4', '%s/larger-than-buffer' % FIXTURES_DIR])

  def test_offset_is_zero(self):
    assert_succeeds_with("Foo\n", ['--offset', '0', '%s/foo.txt' % FIXTURES_DIR])

  def test_offset_is_one(self):
    assert_succeeds_with("oo\n", ['--offset', '1', '%s/foo.txt' % FIXTURES_DIR])

  def test_offset_is_the_size_of_the_file(self):
    assert_succeeds_with("", ['--offset', '4', '%s/foo.txt' % FIXTURES_DIR])

  def test_offset_is_greater_than_the_size_of_the_file(self):
    assert_errors_with('the offset is larger than the file',
                        ['--offset', '5', '%s/foo.txt' % FIXTURES_DIR])


class PathTests(unittest.TestCase):

  def test_path_does_not_exist(self):
    assert_errors_with('we failed to open the file',
                        ['--offset', '0', '%s/does-not-exist' % FIXTURES_DIR])

  def test_path_is_dir(self):
    assert_errors_with('fread failed',
                        ['--offset', '0', FIXTURES_DIR])


class ArgumentValidationTests(unittest.TestCase):

  def test_two_args(self):
    assert_errors_with('exactly three args required',
                        ['arg1', 'arg2'], usage=True)

  def test_four_args(self):
    assert_errors_with('exactly three args required',
                        ['a1', 'a2', 'a3', 'a4'], usage=True)

  def test_wrong_first_arg(self):
    assert_errors_with('the first arg must be "--offset"',
                        ['a1', 'a2', 'a3'], usage=True)

  def test_blank_offset(self):
    assert_errors_with('the offset arg must contain digits',
                        ['--offset', '', 'a3'], usage=True)

  def test_19_digit_offset(self):
    assert_errors_with('the offset arg must contain at most 18 digits',
                        ['--offset', '1234567890123456789', 'file-dne'], usage=True)

  def test_18_digit_offset(self):
    assert_errors_with('we failed to open the file',
                        ['--offset', '123456789012345678', 'file-dne'])

  def test_offset_with_digits_and_nondigits(self):
    assert_errors_with('the offset arg must only contain digits',
                        ['--offset', '123x', 'file-dne'], usage=True)


#### Helpers


FIXTURES_DIR = '/'.join(__file__.split('/')[:-1]) + '/fixtures'
BINARY_PATH = '/'.join(__file__.split('/')[:-2]) + '/build/cat-from'


def assert_equal(got, expected):
  if got != expected:
    print("Expected: %r" % expected)
    print("Got:      %r" % got)
    raise ValueError("values differ")


def assert_succeeds_with(expected_out, args):
  returncode, out, err = run(args)
  assert_equal(returncode, 0)
  assert_equal(out, expected_out)
  assert_equal(err, "")


def assert_errors_with(message, args, usage=False):
  full_message = "Error: %s\n" % message
  if usage is True:
    full_message = "\n" + full_message + "\nUsage:  cat-from --offset N <file>\n\n"
  returncode, out, err = run(args)
  assert_equal(returncode, 1)
  assert_equal(out, "")
  assert_equal(err, full_message)


def run(args):
  command = [BINARY_PATH] + args
  p = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
  (out, err) = p.communicate()
  return (p.returncode, out, err)


if __name__ == '__main__':
  unittest.main()
