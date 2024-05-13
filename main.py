import math
import re
import streamlit as st

# Compile the regular expressions
pattern_expr = re.compile(r"\(([^+-]+)([+-])([^)]+)\)\^([^+-]+)")
pattern_number = re.compile(r"-?\d+\.\d+|-?\d+")

st.title("Binomial Expansion Calculator")


def extract_expression_components(expr):
    match = pattern_expr.search(expr)
    if match:
        return (
            match.group(1).strip(),
            match.group(2),
            match.group(3).strip(),
            match.group(4),
        )
    return None, None, None, None


def extract_numbers(s):
    numbers = [
        float(num) if "." in num else int(num) for num in pattern_number.findall(s)
    ]
    return numbers[0] if numbers else 1


def strip_numbers(s):
    return re.sub(r"\d+", "", s)


user_expr = st.text_input(
    "Expression", placeholder="Enter the expression (e.g., (x-2y)^7)"
)
btn = st.button("Calculate")

if btn:
    a, sign, b, n = extract_expression_components(user_expr)
    if None in (a, sign, b, n) or not n.isdigit():
        st.error("Invalid expression. Please enter in the form (a+b)^n.")
    else:
        n = int(n)
        b_num = extract_numbers(sign + b)
        output = []
        for i in range(n + 1):
            c = math.comb(n, i)
            term_a = extract_numbers(a) ** (n - i)
            term_b = b_num**i
            coefficient = c * term_a * term_b

            # Create the term parts for x and y
            term_parts = []
            a = strip_numbers(a)
            b = strip_numbers(b)
            if n - i > 0:
                term_parts.append(f"{a}^{n-i}" if n - i > 1 else f"{a}")
            if i > 0:
                term_parts.append(f"{b}^{i}" if i > 1 else f"{b}")

            # Determine the sign of the term based on the index and the initial sign of b
            term_sign = "+" if (sign == "+" or i % 2 == 0) else "-"
            if coefficient:
                # Handle the coefficient for the last term or if it's 1
                if (i == n and coefficient == 1) or (
                    i != 0
                    and coefficient == 1
                    and not term_parts[-1].startswith(f"{b}")
                ):
                    term = f"{''.join(term_parts)}"
                else:
                    term = f"{'' if coefficient == 1 else coefficient}{''.join(term_parts)}"
                output.append(
                    f"{term_sign}{term}" if not term.startswith("-") else term
                )

        # Correct initial sign and remove the first '+' if it exists
        formatted_output = "".join(output)
        if formatted_output.startswith("+"):
            formatted_output = formatted_output[1:]

        st.latex(formatted_output)
