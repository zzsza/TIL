import fire

class Calculator:
  def add(self, x, y):
    return x + y

  def multiply(self, x, y):
    return x * y

if __name__ == '__main__':
  calculator = Calculator()
  fire.Fire(calculator)
