from sympy import symbols, Eq, solve, SympifyError, sympify # ADDED 'sympify'
import re

# Define the symbolic variable we will use for all algebra
# By default, SymPy treats 'x' as complex unless specified otherwise,
# but for most algebraic problems, the real domain is often expected.
x = symbols('x')


class SolverEngine:
    """
    Handles symbolic computation for specific, scoped algebraic problems.
    This class ensures mathematical accuracy.
    """

    @staticmethod
    def _parse_equation(equation_str: str):
        """
        Translates a string equation into a SymPy Eq object, assuming '=='
        for equality or expression=0 otherwise.
        """
        from sympy import sympify, Eq, SympifyError  # Local imports for clarity

        # Check for the standardized equality marker: '=='
        if '==' in equation_str:
            try:
                # SPLIT ON THE DOUBLE EQUALS SIGN!
                lhs_str, rhs_str = equation_str.split('==', 1)

                # Sympy can handle sympifying expressions that are just fragments
                lhs = sympify(lhs_str.strip())
                rhs = sympify(rhs_str.strip())
                return Eq(lhs, rhs)
            except SympifyError as e:
                # Catch if LHS or RHS is still gibberish
                raise ValueError(f"Could not parse equation components: {e}")
            except Exception:
                # Catches non-SymPy errors during the split/parse
                raise ValueError("Could not separate equation into two valid sides.")

        # Handle expression (assume finding roots: EXP = 0)
        else:
            try:
                # If no '==' is found, assume the user provided an expression to be set to zero
                expr = sympify(equation_str)
                return Eq(expr, 0)
            except SympifyError as e:
                raise ValueError(f"Could not parse expression: {e}")

    @staticmethod
    def solve_algebraic(equation_str: str) -> list:
        """
        Solves a single-variable algebraic equation (linear or quadratic).
        Returns a list of solutions.
        """
        try:
            # 1. Parse the string into a SymPy Equation object
            equation = SolverEngine._parse_equation(equation_str)

            # 2. Solve the equation for the symbol 'x'
            solutions = solve(equation, x)

            # 3. Handle specific output cases (e.g., no solution)
            if not solutions:
                # SymPy returns an empty list for equations with no solution (e.g., x^2 = -1 in Reals, but we assume Complex by default)
                # Since SymPy defaults to the complex domain, we return the result directly.
                # Note: In a real app, you'd add domain checking here.
                return []

            return solutions

        except ValueError as e:
            # Re-raise parsing error for the chatbot to handle gracefully
            raise e
        except Exception as e:
            # Catch all other SymPy solving errors
            raise RuntimeError(f"SymPy failed to solve the equation: {e}")



# --- Day 1 Testing/Verification ---
if __name__ == "__main__":
    print("--- Solver Engine Unit Test ---")

    # Test 1: Linear Equation
    linear_eq = "2*x + 5 == 15"
    print(f"\nSolving Linear: {linear_eq}")
    sol1 = SolverEngine.solve_algebraic(linear_eq)
    print(f"Solutions: {sol1}")
    # Expected: [5]

    # Test 2: Quadratic Equation (Two Real Roots)
    quadratic_eq = "x**2 - 5*x + 6"  # Assumes expression = 0
    print(f"\nSolving Quadratic: {quadratic_eq} = 0")
    sol2 = SolverEngine.solve_algebraic(quadratic_eq)
    print(f"Solutions: {sol2}")
    # Expected: [2, 3]

    # Test 3: Quadratic Equation (Complex Roots - SymPy will find them)
    complex_eq = "x**2 + 1 == 0"
    print(f"\nSolving Complex: {complex_eq}")
    sol3 = SolverEngine.solve_algebraic(complex_eq)
    print(f"Solutions: {sol3}")
    # Expected: [-I, I] where I is the imaginary unit

    # Test 4: Quadratic with fractional output
    frac_eq = "2*x**2 + 5*x - 3 == 0"
    print(f"\nSolving Fractional: {frac_eq}")
    sol4 = SolverEngine.solve_algebraic(frac_eq)
    print(f"Solutions: {sol4}")
    # Expected: [-3, 1/2]