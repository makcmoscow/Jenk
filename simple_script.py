def check_digit(variable):
  if variable.isdigit():
    return True
  else:
    return False

def test_check_digit():
  assert check_digit(123) == True, 'It\'s digit'
  assert check_digit('asd') == False, 'It\'s not a digit'

if __name__ == '__main__':
  result = check_digit(345)
  print('result of function: ', result)
