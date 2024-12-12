from backend.stack import SLStack
from backend.utils import level
import re

stack = SLStack()  # bikin linked listnya
Operators = {"+", "-", "*", "/", "^", "(", ")"}


def infix_to_prefix(expression):
    conversion_steps = []
    characters = re.findall(r"(?:(?<!\d)-\d+\.\d+|(?<!\d)-\d+|\d+\.\d+|\d+|[^\d\w\s])", expression)[
        ::-1
    ]  ## tokenisasi (list() jadi ngebikin semua elemen "kepecah") dan langsung direverse. serta handle float biar jadi satu kesatuan
    conversion_steps.append(f"Langkah 1: Reverse infix yang telah ditokenisasi: {characters}")
    prefix = []  # untuk store hasilnya
    step_count = 2  # untuk labelin setiap step

    for char in characters:
        if char == ")":  # kalo input ) push ke stack
            stack.push(char)
            conversion_steps.append(f"Langkah {step_count}: Push {char} ke Stack")
            step_count += 1

        elif char == "(":  # kalo input "(" pop sampe ketemu input ")"
            while stack.is_empty() != True and stack.peek() != ")":
                prefix.append(stack.pop())
                step_count += 1
            stack.pop()  # tutup kurungnya "()" ga dimasukkin ke hasil akhir
            conversion_steps.append(f"Langkah {step_count}: Pop ')'")
            step_count += 1

        elif char not in Operators:  # kalo input operands langsung dimasukkin ke hasil akhir
            try:
                float(char)  # memastikan input operands benar angka
                prefix.append(char)
                conversion_steps.append(f"Langkah {step_count}: Masukkan {char} ke Prefix")
                step_count += 1
            except ValueError:  # program dihentikan ketika ada operator yang tidak valid
                conversion_steps.append(f"Langkah {step_count}: Error: '{char}' bukanlah suatu operator yang valid.")
                return None, conversion_steps

        else:  # kalo input operator dan levelnya lebih rendah dari elemen TOP yang ada di stack, pop, sampe ketemu elemen TOP yang levelnya sama atau lebih rendah
            while not stack.is_empty() and level(char) < level(stack.peek()) and stack.peek() != ")":  # peek ngecek elemen TOP di stack
                conversion_steps.append(
                    f"Langkah {step_count}: Karena level {char} lebih rendah dari {stack.peek()}, pop operator dari stack dan masukkan ke Prefix"
                )
                prefix.append(stack.pop())
                step_count += 1
            stack.push(char)  # masukin inputnya ke stack
            conversion_steps.append(f"Langkah {step_count}: Push {char} ke Stack")
            step_count += 1

    while stack.is_empty() != True:  # terakhir, pop sisa operator yang ada distack
        prefix.append(stack.peek())
        stack.pop()
        conversion_steps.append(f"Langkah {step_count}: Karena elemen sudah habis, pop sisa operator dari stack dan masukkan ke Prefix")
        step_count += 1

    prefix = prefix[::-1]  # reverse lagi hasil akhir
    conversion_steps.append(f"Langkah {step_count}: Reverse kembali hasil Prefix: {prefix}")
    step_count += 1
    conversion_steps.append("")
    conversion_steps.append(f"Hasil Prefix: {''.join(prefix)}")

    return prefix, conversion_steps


def calculate_prefix(prefix: list):
    calculate_steps = []
    step_count = 1

    # Traverse dari kanan ke kiri pada ekspresi prefix
    for char in reversed(prefix):
        result = None
        if char not in Operators:  # Jika operand, push ke stack
            stack.push(float(char))
            calculate_steps.append(f"Langkah {step_count}: Masukkan operand {char} ke stack.")
            step_count += 1
        else:  # Jika operator, lakukan operasi
            op1 = stack.pop()
            op2 = stack.pop()
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
