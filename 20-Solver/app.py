import streamlit as st
from itertools import permutations, product


# Fungsi untuk menambahkan backslash sebelum tanda * agar tidak dianggap sebagai italic di Markdown
def escape_asterisk(expr):
    return expr.replace("*", "\\*")


# Fungsi Solver tetap sama
def apply_ops(ops, nums):
    expr = str(nums[0])
    for i in range(3):
        expr += ops[i] + str(nums[i + 1])
    return expr


def valid_combinations(nums, ops):
    templates = [
        "({}{}{}){}{}{}{}",  # ((a op b) op c) op d
        "({}{}({}{}{})){}{}",  # (a op (b op c)) op d
        "{}{}({}{}({}{}{}))",  # a op (b op (c op d))
        "{}{}(({}{}{}){}{})",  # a op ((b op c) op d)
        "({}{}{}){}({}{}{})",  # (a op b) op (c op d)
    ]

    results = []
    for template in templates:
        try:
            expr = template.format(
                nums[0], ops[0], nums[1], ops[1], nums[2], ops[2], nums[3]
            )
            if abs(eval(expr) - 20) < 1e-6: 
                # menambahkan backslash sebelum tanda * agar tidak dianggap sebagai italic di Markdown
                results.append(escape_asterisk(expr))
        except ZeroDivisionError:
            continue
    return results


def solve_20(nums):
    operations = ["+", "-", "*", "/"]
    found_solutions = set()

    # Generate semua permutations angka dan operasinya
    for num_perm in permutations(nums):
        for ops in product(operations, repeat=3):
            solutions = valid_combinations(num_perm, ops)
            found_solutions.update(solutions)

    return found_solutions


# Konfigurasi aplikasi Streamlit
st.title("20 Solver")
st.write(
    "Masukkan 4 angka pada kolom di bawah ini, dan lihat apakah mereka bisa menghasilkan angka 20."
)

# Input dari pengguna: 4 baris input untuk masing-masing angka
num1 = st.number_input("Angka 1", value=0, step=1)
num2 = st.number_input("Angka 2", value=0, step=1)
num3 = st.number_input("Angka 3", value=0, step=1)
num4 = st.number_input("Angka 4", value=0, step=1)

# Ketika input diberikan, lakukan proses perhitungan
numbers = [num1, num2, num3, num4]
if all(numbers):  # Pastikan semua input diberikan
    solutions = solve_20(numbers)
    if solutions:
        st.success(f"{len(solutions)} solusi ditemukan:")
        for solution in solutions:
            st.write(solution)
    else:
        st.warning("Tidak ada solusi yang ditemukan untuk menghasilkan 20.")
