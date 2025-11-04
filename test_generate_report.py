"""
Тестовый скрипт для проверки генерации отчета
"""
import requests
import sys


def test_generate_report(report_id: int, output_file: str = "report.pdf"):
    """
    Тестировать генерацию отчета

    Args:
        report_id: ID отчета для генерации
        output_file: Путь для сохранения PDF
    """
    url = "http://localhost:8000/api/v1/reports/generate"

    print(f"Отправка запроса на генерацию отчета {report_id}...")

    try:
        response = requests.post(
            url,
            json={"report_id": report_id},
            timeout=30
        )

        if response.status_code == 200:
            # Сохраняем PDF
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"✅ Отчет успешно сгенерирован и сохранен в {output_file}")
            print(f"   Размер файла: {len(response.content)} байт")
            return True
        elif response.status_code == 404:
            print(f"❌ Ошибка 404: Отчет с ID {report_id} не найден")
            try:
                error_data = response.json()
                print(f"   Детали: {error_data.get('detail', 'Нет дополнительной информации')}")
            except:
                pass
            return False
        elif response.status_code == 500:
            print(f"❌ Ошибка 500: Внутренняя ошибка сервера")
            try:
                error_data = response.json()
                print(f"   Детали: {error_data.get('detail', 'Нет дополнительной информации')}")
            except:
                pass
            return False
        else:
            print(f"❌ Неожиданная ошибка: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения: Сервер не доступен")
        print("   Убедитесь что сервер запущен на http://localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Ошибка: Превышено время ожидания (30 секунд)")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        return False


def test_health_check():
    """Проверить доступность сервера"""
    url = "http://localhost:8000/health"

    print("Проверка доступности сервера...")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сервер доступен")
            print(f"   Статус: {data.get('status', 'unknown')}")
            print(f"   Сервис: {data.get('service', 'unknown')}")
            return True
        else:
            print(f"⚠️  Сервер ответил с кодом {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не доступен")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  Тестирование Report Generation Microservice")
    print("=" * 60)
    print()

    # Проверка доступности сервера
    if not test_health_check():
        print()
        print("Запустите сервер командой: python -m app.main")
        sys.exit(1)

    print()
    print("-" * 60)
    print()

    # Получаем report_id из аргументов командной строки
    if len(sys.argv) > 1:
        try:
            report_id = int(sys.argv[1])
        except ValueError:
            print("❌ Ошибка: report_id должен быть числом")
            print()
            print("Использование: python test_generate_report.py <report_id>")
            print("Пример: python test_generate_report.py 1")
            sys.exit(1)
    else:
        report_id = 1
        print(f"ℹ️  report_id не указан, используется значение по умолчанию: {report_id}")
        print()

    # Тестируем генерацию отчета
    output_file = f"report_{report_id}.pdf"
    success = test_generate_report(report_id, output_file)

    print()
    print("=" * 60)

    if success:
        print("✅ Тест пройден успешно!")
        sys.exit(0)
    else:
        print("❌ Тест провален")
        sys.exit(1)
