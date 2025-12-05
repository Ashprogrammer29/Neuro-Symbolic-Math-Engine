from src.language_model import LanguageModel
from src.solver_engine import SolverEngine
from sympy import latex  # Used for clean mathematical formatting


class MathChatbot:
    """
    The Orchestrator: Combines NLU (LanguageModel) and Computation (SolverEngine)
    into a single, robust, tool-augmented system.
    """

    def __init__(self):
        # Initialize the two core components
        print("\n--- Initializing Chatbot Components ---")
        self.parser = LanguageModel()
        self.solver = SolverEngine()
        print("--- Chatbot Ready ---")

        # Define the acceptable scope for error messages
        self.SCOPE_MESSAGE = (
            "I am currently a specialized algebraic solver. "
            "I can only solve single-variable linear and quadratic equations. "
            "Please phrase your question as a clear equation (e.g., 'x^2 + 5x = 6')."
        )

    def format_solutions(self, solutions: list) -> str:
        """
        [Output Formatting] Converts raw SymPy results into clean, readable LaTeX text.
        This is necessary for a professional presentation.
        """
        if not solutions:
            return "This equation has no solution."

        # Use latex() for presentation

        if len(solutions) == 1:
            solution_str = f"The single solution for $x$ is: ${latex(solutions[0])}$."
        else:
            # Format multiple solutions
            solution_parts = [f"${latex(sol)}$" for sol in solutions]

            # Use 'and' for two solutions, or commas for more
            if len(solutions) == 2:
                solution_str = f"The solutions for $x$ are: {solution_parts[0]} and {solution_parts[1]}."
            else:
                solution_str = f"The solutions for $x$ are: {', '.join(solution_parts)}."

        return solution_str

    def ask(self, query: str) -> str:
        """
        The main query processing loop (The Agent Logic).
        """
        try:
            # 1. Classification & Extraction (NLU/Parser)
            classification, equation_str = self.parser.classify_and_extract(query)

            # 2. Scope Check (Triage)
            if classification == "other":
                return self.SCOPE_MESSAGE

            # 3. Solve (Offloading to Tool)
            # The SolverEngine handles the core math for both 'linear' and 'quadratic' types.
            solutions = self.solver.solve_algebraic(equation_str)

            # 4. Formatting (Generation)
            return self.format_solutions(solutions)

        except ValueError as e:
            # Handles parsing errors from the LanguageModel or SymPy
            # Example: User inputting gibberish math that SymPy can't read
            print(f"\n[DEBUG: Parsing Error] {e}")
            return (
                f"I encountered a syntax error while trying to parse your equation. "
                f"Ensure your input is correctly formatted (e.g., 4*x**2 + 2*x == 0). {self.SCOPE_MESSAGE}"
            )
        except RuntimeError as e:
            # Handles fundamental SymPy solving failures
            print(f"\n[DEBUG: Solver Error] {e}")
            return (
                "An internal computation error occurred. The problem is likely ill-posed or outside the precise scope."
            )
        except Exception as e:
            # Catch all other unexpected errors
            print(f"\n[DEBUG: Unexpected Error] {e}")
            return "An unexpected error occurred. Please simplify your query."