from backend.stack import SLStack
from backend.utils import level
import re

stack = SLStack()  # bikin linked listnya
Operators = {"+", "-", "*", "/", "^", "(", ")"}


def infix_to_postfix(expression):
    conversion_steps = []
    characters = re.findall(r"(?:(?<!\d)-\d+\.\d+|(?<!\d)-\d+|\d+\.\d+|\d+|[^\d\w\s])", expression)  # Tokenisasi ekspresi infix
    conversion_steps.append(f"Langkah 1: Tokenisasi ekspresi infix: {characters}")
    postfix = []  # untuk store hasilnya
    step_count = 2  # untuk labelin setiap step

    for char in characters:
        print(f"Elemen dari ekspresi Infix: {char}")
        if char == "(":  # kalo input ( push ke stack
            stack.push(char)
            conversion_steps.append(f"Langkah {step_count}: Push {char} ke Stack")
            step_count += 1

        elif char == ")":  # kalo input ")", pop sampe ketemu input "("
            while stack.is_empty() != True and stack.peek() != "(":
                postfix.append(stack.pop())
                step_count += 1
            stack.pop()  # pop tanda "("
            conversion_steps.append(f"Langkah {step_count}: Pop '('")
            step_count += 1

        elif char not in Operators:  # kalo input operands langsung dimasukkin ke hasil akhir
            try:
                float(char)  # memastikan input operands benar angka
                postfix.append(char)
                conversion_steps.append(f"Langkah {step_count}: Masukkan {char} ke Postfix")
                step_count += 1
            except ValueError:  # program dihentikan ketika ada operator yang tidak valid
                conversion_steps.append(f"Langkah {step_count}: Error: '{char}' bukanlah operand yang valid.")
                return

        else:  # kalo input operator
            while not stack.is_empty() and level(char) <= level(stack.peek()) and stack.peek() != "(":  # peek ngecek elemen TOP di stack
                conversion_steps.append(
                    f"Langkah {step_count}: Karena level {char} lebih rendah dari {stack.peek()}, pop operator dari stack dan masukkan ke Postfix"
                )
                postfix.append(stack.pop())
                step_count += 1
            stack.push(char)  # masukin inputnya ke stack
            conversion_steps.append(f"Langkah {step_count}: Push {char} ke Stack")
            step_count += 1

    while stack.is_empty() != True:  # terakhir, pop sisa operator yang ada distack
        postfix.append(stack.peek())
        stack.pop()
        conversion_steps.append(f"Langkah {step_count}: Karena elemen sudah habis, pop sisa operator dari stack dan masukkan ke Postfix")
        step_count += 1

    step_count += 1
    conversion_steps.append("")
    conversion_steps.append(f"Hasil Postfix: {''.join(postfix)}")

    return postfix, conversion_steps


def calculate_postfix(postfix: list):
    calculate_steps = []
    step_count = 1

    # Traverse dari kiri ke kanan pada ekspresi postfix
    for char in postfix:
        result = None
        if char not in Operators:  # Jika operand, push ke stack
            stack.push(float(char))
            calculate_steps.append(f"Langkah {step_count}: Masukkan operand {char} ke stack.")
            step_count += 1
        else:  # Jika operator, lakukan operasi
            op2 = stack.pop()
            op1 = stack.pop()
            if char == "+":
                result = op1 + op2
            elif char == "-":
                result = op1 - op2
            elif char == "*":
                result = op1 * op2
            elif char == "/":
                result = op1 / op2
            elif char == "^":
                result = op1**op2

            calculate_steps.append(
                f"Langkah {step_count}: Pop {op1} dan {op2}, lalu hitung {op1} {char} {op2} = {result}. Kemudian masukkan {result} ke stack."
            )
            step_count += 1
            stack.push(result)

    # Hasil akhir
    final_result = stack.pop()
    calculate_steps.append("")
    calculate_steps.append(f"Hasil akhir: {final_result}")

    return final_result, calculate_steps
