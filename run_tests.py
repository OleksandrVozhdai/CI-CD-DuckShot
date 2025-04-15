import unittest
import sys
import os.path

# Додаємо корінь проєкту до sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Знаходимо всі тести в директорії tests
test_loader = unittest.TestLoader()
test_suite = test_loader.discover('tests', pattern='test_*.py')

# Запускаємо тести
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(test_suite)

# Перевіряємо, чи були помилки
if not result.wasSuccessful():
    sys.exit(1)
