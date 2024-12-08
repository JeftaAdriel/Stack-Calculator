from api.routers.stack import SLStack

import re

Operators = {"+", "-", "*", "/", "^", "(", ")"}


def level(char):
    if char == "^":
        return 3
    elif char == "/" or char == "*":
        return 2
    elif char == "+" or char == "-":
        return 1
    else:
        return 0


def infix_to_prefix(expression):

    characters = re.findall(r"\d+\.\d+|\d+|[^\d\w\s]", expression)[
        ::-1
    ]  ## tokenisasi (list() jadi ngebikin semua elemen "kepecah") dan langsung direverse. serta handle float biar jadi satu kesatuan
    print(f"Langkah Pertama, reverse infix yang telah ditokenisasi: {characters}\n")
    stack = SLStack()  # bikin linked listnya
    prefix = []  # untuk store hasilnya
    step_count = 2  # untuk labelin setiap step

    for char in characters:
        print(f"Elemen dari ekspresi Infix: {char}")
        if char == ")":  # kalo input ) push ke stack
            stack.push(char)
            print(f"Langkah {step_count}: Push {char} ke Stack")
            print(f"Prefix: {prefix}\n")
            stack.print_stack()
            step_count += 1

        elif char == "(":  # kalo input "(" pop sampe ketemu input ")"
            print(f"Langkah {step_count}: Pop sampai ditemukan ')'")
            while stack.is_empty() != True and stack.peek() != ")":
                prefix.append(stack.pop())
                print(f"Prefix: {prefix}\n")
                stack.print_stack()
                step_count += 1
            stack.pop()  # tutup kurungnya "()" ga dimasukkin ke hasil akhir
            print(f"Langkah {step_count}: Pop ')'")
            print(f"Prefix: {prefix}\n")
            stack.print_stack()
            step_count += 1

        elif char not in Operators:  # kalo input operands langsung dimasukkin ke hasil akhir
            try:
                float(char)  # memastikan input operands benar angka
                prefix.append(char)
                print(f"Langkah {step_count}: Masukkan {char} ke Prefix: {prefix}")
                print(f"Prefix: {prefix}\n")
                stack.print_stack()
                step_count += 1
            except ValueError:  # program dihentikan ketika ada operator yang tidak valid
                print(f"Langkah {step_count}: Error: '{char}' bukanlah suatu operator yang valid.")
                return

        else:  # kalo input operator dan levelnya lebih rendah dari elemen TOP yang ada di stack, pop, sampe ketemu elemen TOP yang levelnya sama atau lebih rendah
            while stack.is_empty() != True and (level(char) < level(stack.peek())):  # peek ngecek elemen TOP di stack
                print(
                    f"Langkah {step_count}: Karena level {char} lebih rendah dari {stack.peek()}, pop operator dari stack dan masukkan ke Prefix: {prefix}"
                )
                prefix.append(stack.pop())
                print(f"Prefix: {prefix}\n")
                stack.print_stack()
            stack.push(char)  # masukin inputnya ke stack
            print(f"Langkah {step_count}: Push {char} ke Stack")
            print(f"Prefix: {prefix}\n")
            stack.print_stack()
            step_count += 1

    while stack.is_empty() != True:  # terakhir, pop sisa operator yang ada distack
        prefix.append(stack.peek())
        stack.pop()
        print(f"Langkah {step_count}: Karena elemen sudah habis, pop sisa operator dari stack dan masukkan ke Prefix: {prefix}")
        print(f"Prefix: {prefix}\n")
        stack.print_stack()
        step_count += 1

    prefix = prefix[::-1]  # reverse lagi hasil akhir
    print(f"Langkah terakhir, reverse kembali hasil Prefix: {prefix}\n")
    print(f"Hasil Akhir: {''.join(prefix)}\n")
