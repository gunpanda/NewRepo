import sys
import os

# Настраиваем кодировку для Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')  # Для вывода ошибок

def calculate_tax(income):
    """Рассчитывает общий НДФЛ по прогрессивной шкале для заданного дохода."""
    if income <= 0:
        return 0
    thresholds = [0, 2_400_000, 5_000_000, 20_000_000, 50_000_000]
    rates = [0.13, 0.15, 0.18, 0.20, 0.22]
    tax = 0
    for i in range(len(thresholds) - 1):
        if income > thresholds[i]:
            tax += (min(income, thresholds[i + 1]) - thresholds[i]) * rates[i]
    if income > thresholds[-1]:
        tax += (income - thresholds[-1]) * rates[-1]
    return round(tax)

def calculate_additional_tax(total_income, tax_withheld):
    """Рассчитывает сумму налога, которую нужно доплатить самостоятельно."""
    total_tax = calculate_tax(total_income)
    additional_tax = total_tax - tax_withheld
    return round(max(additional_tax, 0))

if __name__ == "__main__":
    print("Программа запущена. Введите данные ниже:")
    while True:
        try:
            print("Ожидается ввод дохода...")
            total_income = float(input("Введите общий годовой доход: "))
            print(f"Доход введен: {total_income}")
            print("Ожидается ввод удержанного налога...")
            tax_withheld = float(input("Введите сумму налога, удержанного работодателем: "))
            print(f"Удержанный налог введен: {tax_withheld}")
            if total_income < 0 or tax_withheld < 0:
                print("Доход и налог не могут быть отрицательными. Попробуйте снова.")
                continue
            break
        except ValueError:
            print("Ошибка: введите числовое значение. Попробуйте снова.")
        except Exception as e:
            print(f"Произошла неизвестная ошибка: {e}. Попробуйте снова.")
    
    additional_tax = calculate_additional_tax(total_income, tax_withheld)
    print(f"Сумма налога, которую потребуется доплатить самостоятельно: {additional_tax} рублей")