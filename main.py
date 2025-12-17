##cookbook


def read_cookbook(filename):

    cook_book = {}

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            while True:
                # Читаем название блюда
                dish_name = file.readline().strip()
                if not dish_name:  # Конец файла
                    break

                # Читаем количество ингредиентов
                try:
                    ingredients_count = int(file.readline().strip())
                except ValueError as e:
                    print(f"Ошибка: неверный формат количества ингредиентов для '{dish_name}': {e}")
                    break

                # Читаем сами ингредиенты
                ingredients = []
                for _ in range(ingredients_count):
                    line = file.readline().strip()

                    # Проверяем формат строки
                    if '|' not in line:
                        print(f"Ошибка: неверный формат строки ингредиента: '{line}'")
                        continue

                    parts = line.split('|')
                    if len(parts) != 3:
                        print(f"Ошибка: неверный формат строки ингредиента: '{line}'")
                        continue

                    ingredient_name = parts[0].strip()

                    try:
                        quantity = int(parts[1].strip())
                    except ValueError as e:
                        print(f"Ошибка: количество должно быть числом в '{ingredient_name}': {e}")
                        continue

                    measure = parts[2].strip()

                    # Корректируем единицы измерения согласно примеру из задания
                    if measure == 'шт':
                        measure = 'шт.'

                    ingredients.append({
                        'ingredient_name': ingredient_name,
                        'quantity': quantity,
                        'measure': measure
                    })

                # Добавляем блюдо в кулинарную книгу
                cook_book[dish_name] = ingredients

                # Пропускаем пустую строку между рецептами
                file.readline()

    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        return {}
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return {}

    return cook_book


def print_cookbook(cook_book):
    ""
    if not cook_book:
        print("Кулинарная книга пуста!")
        return

    print("cook_book = {")

    dishes = list(cook_book.keys())
    for dish_idx, dish_name in enumerate(dishes):
        ingredients = cook_book[dish_name]

        print(f"  '{dish_name}': [")

        for ing_idx, ingredient in enumerate(ingredients):
            # Определяем, нужна ли запятая после ингредиента
            comma = ',' if ing_idx < len(ingredients) - 1 else ''

            print(f"    {{'ingredient_name': '{ingredient['ingredient_name']}', "
                  f"'quantity': {ingredient['quantity']}, "
                  f"'measure': '{ingredient['measure']}'}}{comma}")

        # Определяем, нужна ли запятая после блюда
        dish_comma = ',' if dish_idx < len(dishes) - 1 else ''
        print(f"    ]{dish_comma}")

    print("}")


def get_shop_list_by_dishes(dishes, person_count, cook_book):

    shop_list = {}

    for dish in dishes:
        if dish not in cook_book:
            print(f"Внимание: блюдо '{dish}' не найдено в кулинарной книге!")
            continue

        for ingredient in cook_book[dish]:
            name = ingredient['ingredient_name']
            quantity = ingredient['quantity'] * person_count

            if name in shop_list:
                # Если ингредиент уже есть, суммируем количество
                shop_list[name]['quantity'] += quantity
            else:
                # Добавляем новый ингредиент
                shop_list[name] = {
                    'measure': ingredient['measure'],
                    'quantity': quantity
                }

    return shop_list


def main():
    """Основная функция для демонстрации работы программы"""
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ КУЛИНАРНОЙ КНИГИ")
    print("=" * 60)

    # 1. Чтение рецептов из файла
    print("\n1. Чтение рецептов из файла 'recipes.txt'...")
    cook_book = read_cookbook('recipes.txt')

    if not cook_book:
        print("Не удалось прочитать рецепты. Завершение программы.")
        return

    print(f"Успешно прочитано рецептов: {len(cook_book)}")

    # 2. Вывод кулинарной книги
    print("\n2. Кулинарная книга:")
    print_cookbook(cook_book)

    # 3. Пример использования: расчет покупок
    print("\n" + "=" * 60)
    print("3. ПРИМЕР: РАСЧЕТ ПОКУПОК ДЛЯ БЛЮД")
    print("=" * 60)

    # Готовим Омлет и Запеченный картофель на 2 персоны
    dishes_to_cook = ['Омлет', 'Запеченный картофель']
    persons = 2

    print(f"\nБлюда для готовки: {', '.join(dishes_to_cook)}")
    print(f"Количество персон: {persons}")

    shop_list = get_shop_list_by_dishes(dishes_to_cook, persons, cook_book)

    print("\nСписок покупок:")
    print("-" * 30)
    for ingredient, details in sorted(shop_list.items()):
        print(f"{ingredient}: {details['quantity']} {details['measure']}")

    # 4. Тестирование соответствия заданию
    print("\n" + "=" * 60)
    print("4. ПРОВЕРКА СООТВЕТСТВИЯ ЗАДАНИЮ")
    print("=" * 60)

    # Проверяем наличие ключевых блюд из задания
    required_dishes = ['Омлет', 'Утка по-пекински', 'Запеченный картофель']

    print("\nПроверка наличия блюд из задания:")
    for dish in required_dishes:
        if dish in cook_book:
            print(f"  ✓ '{dish}' - найдено ({len(cook_book[dish])} ингредиентов)")
        else:
            print(f"  ✗ '{dish}' - НЕ найдено!")

    # Проверяем формат ингредиентов
    print("\nПроверка формата ингредиентов:")
    if cook_book.get('Омлет'):
        first_ingredient = cook_book['Омлет'][0]
        required_keys = ['ingredient_name', 'quantity', 'measure']

        if all(key in first_ingredient for key in required_keys):
            print("  ✓ Формат ингредиентов соответствует заданию")
        else:
            print("  ✗ Формат ингредиентов НЕ соответствует заданию")

    print("\n" + "=" * 60)
    print("ПРОГРАММА УСПЕШНО ЗАВЕРШЕНА!")
    print("=" * 60)


if __name__ == "__main__":
    main()



#HOMEWORK 2 COOKBOOK
#get_shop_list_by_dishes

def read_cookbook(filename):
    cook_book = {}

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        while i < len(lines) and lines[i].strip() == '':
            i += 1

        if i >= len(lines):
            break

        dish_name = lines[i].strip()
        i += 1

        ingredients_count = int(lines[i].strip())
        i += 1

        ingredients = []
        for _ in range(ingredients_count):
            line = lines[i].strip()
            parts = line.split('|')

            ingredient_name = parts[0].strip()
            quantity = int(parts[1].strip())
            measure = parts[2].strip()

            if measure == 'шт':
                measure = 'шт.'

            ingredients.append({
                'ingredient_name': ingredient_name,
                'quantity': quantity,
                'measure': measure
            })

            i += 1

        cook_book[dish_name] = ingredients

    return cook_book


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}

    for dish in dishes:
        if dish in cook_book:
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                quantity = ingredient['quantity'] * person_count
                measure = ingredient['measure']

                if name in shop_list:
                    shop_list[name]['quantity'] += quantity
                else:
                    shop_list[name] = {
                        'measure': measure,
                        'quantity': quantity
                    }

    return shop_list


cook_book = read_cookbook('recipes.txt')
result = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)
print(result)


##homework 3

def merge_files(input_files, output_file='result.txt'):
    """
    Объединение файлов с сортировкой по количеству строк
    """
    # Собираем информацию о файлах
    files_data = []

    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
                files_data.append({
                    'name': os.path.basename(file_path),
                    'lines': len(content),
                    'content': ''.join(content).strip()
                })
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден!")
            continue
        except Exception as e:
            print(f"Ошибка при чтении '{file_path}': {e}")
            continue

    # Сортируем по количеству строк
    files_data.sort(key=lambda x: x['lines'])

    # Записываем в итоговый файл
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            for file_info in files_data:
                output.write(f"{file_info['name']}\n")
                output.write(f"{file_info['lines']}\n")
                if file_info['content']:
                    output.write(f"{file_info['content']}\n")

        print(f"✓ Файлы объединены в '{output_file}'")
        return True

    except Exception as e:
        print(f"Ошибка при записи в '{output_file}': {e}")
        return False


# ========== ТЕСТИРОВАНИЕ ВСЕХ ЗАДАЧ ==========

def test_task_1():
    """Тест задачи №1"""
    print("\n" + "=" * 60)
    print("ТЕСТ ЗАДАЧИ №1: Чтение кулинарной книги")
    print("=" * 60)

    cook_book = read_cookbook('recipes.txt')

    if not cook_book:
        print("❌ Не удалось прочитать файл 'recipes.txt'")
        print("   Создайте файл recipes.txt с рецептами")
        return None

    print(f"✅ Прочитано {len(cook_book)} блюд:")
    for dish, ingredients in cook_book.items():
        print(f"   • {dish}: {len(ingredients)} ингредиентов")

    return cook_book


def test_task_2(cook_book):
    """Тест задачи №2"""
    print("\n" + "=" * 60)
    print("ТЕСТ ЗАДАЧИ №2: Расчет списка покупок")
    print("=" * 60)

    if not cook_book:
        print("❌ Кулинарная книга пуста")
        return

    print("Тест: get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)")

    result = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)

    print("\nРезультат:")
    print("{")
    for ingredient, details in sorted(result.items()):
        print(f"  '{ingredient}': {{'measure': '{details['measure']}', 'quantity': {details['quantity']}}},")
    print("}")

    # Проверяем правильность
    expected = {
        'Картофель': {'measure': 'кг', 'quantity': 2},
        'Молоко': {'measure': 'мл', 'quantity': 200},
        'Помидор': {'measure': 'шт', 'quantity': 4},
        'Сыр гауда': {'measure': 'г', 'quantity': 200},
        'Яйцо': {'measure': 'шт', 'quantity': 4},
        'Чеснок': {'measure': 'зубч', 'quantity': 6}
    }

    if result == expected:
        print("\n✅ Результат совпадает с заданием!")
    else:
        print("\n❌ Результат не совпадает!")


def test_task_3():
    """Тест задачи №3"""
    print("\n" + "=" * 60)
    print("ТЕСТ ЗАДАЧИ №3: Объединение файлов")
    print("=" * 60)

    # Создаем тестовые файлы как в задании
    print("Создаем тестовые файлы...")

    # Файл 1.txt
    with open('1.txt', 'w', encoding='utf-8') as f:
        f.write("Строка номер 1 файла номер 1\n")
        f.write("Строка номер 2 файла номер 1")

    # Файл 2.txt
    with open('2.txt', 'w', encoding='utf-8') as f:
        f.write("Строка номер 1 файла номер 2")

    # Файл 3.txt (дополнительный для примера)
    with open('3.txt', 'w', encoding='utf-8') as f:
        f.write("Первая строка\n")
        f.write("Вторая строка\n")
        f.write("Третья строка")

    print("Файлы созданы:")
    print("  1.txt - 2 строки")
    print("  2.txt - 1 строка")
    print("  3.txt - 3 строки")

    # Объединяем файлы
    print("\nОбъединяем файлы...")
    merge_files(['1.txt', '2.txt', '3.txt'], 'test_result.txt')

    # Показываем результат
    print("\nСодержимое test_result.txt:")
    print("-" * 40)
    if os.path.exists('test_result.txt'):
        with open('test_result.txt', 'r', encoding='utf-8') as f:
            print(f.read())

    # Убираем тестовые файлы
    for file in ['1.txt', '2.txt', '3.txt', 'test_result.txt']:
        if os.path.exists(file):
            os.remove(file)


def main():
    """Главная функция - тестирует все задачи"""
    print("=" * 60)
    print("ДОМАШНЕЕ ЗАДАНИЕ: ОБРАБОТКА ФАЙЛОВ")
    print("Все 3 задачи в одном файле")
    print("=" * 60)

    # Тест задачи №1
    cook_book = test_task_1()

    # Тест задачи №2 (если есть кулинарная книга)
    if cook_book:
        test_task_2(cook_book)

    # Тест задачи №3
    test_task_3()

    print("\n" + "=" * 60)
    print("ИНФОРМАЦИЯ О ФУНКЦИЯХ:")
    print("=" * 60)
    print("""

    print("\n✅ Все функции готовы к использованию!")