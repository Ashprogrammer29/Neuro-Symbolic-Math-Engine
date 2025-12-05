from transformers import AutoTokenizer
from src.config import MODEL_NAME, MODEL_LOCAL_PATH
import os
import re

class LanguageModel:
    """
    Handles NLU: Classifying the input query type (Linear, Quadratic, Other)
    and extracting the clean algebraic string.
    """

    # --- THIS IS THE CORRECTED __INIT__ METHOD ---
    def __init__(self):
        # 1. Download and Load Tokenizer (Required for basic text cleanup)
        print(f"Loading tokenizer...")

        # Check if local path exists to enforce local loading attempt first
        is_local_path_ready = os.path.exists(MODEL_LOCAL_PATH)

        if is_local_path_ready:
            print("Attempting to load from local cache...")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(MODEL_LOCAL_PATH, local_files_only=True)
                print("Tokenizer loaded from local cache.")
                # FIX: Use a return statement to exit the function if successful
                return
            except Exception as e:
                # If local load fails (e.g., incomplete files), we fall through to download
                print(f"Error loading local model: {e}. Attempting online download...")

        # Fallback: Initial Online Download (ONLY if local files failed or don't exist)
        print(f"Local files not ready. Downloading {MODEL_NAME} (REQUIRED ONCE)...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.tokenizer.save_pretrained(MODEL_LOCAL_PATH)
            print("Tokenizer downloaded and saved locally.")
        except Exception as e:
            # Fatal Error: If this fails, it's an authentication or connection issue.
            print("\n❌ FATAL ERROR: Failed to download model. You must address the following:")
            print("1. Check internet connection.")
            print("2. Run 'huggingface-cli login' in your terminal.")
            print(f"Original error: {e}")
            raise RuntimeError("Model download/authentication failed. Cannot proceed.")

    # --- THIS IS THE CORRECT classify_and_extract METHOD ---
    def classify_and_extract(self, query: str) -> tuple[str, str | None]:

        clean_query = query.lower().strip()
        classification = "other"  # Initialize outside the checks

        # --- Stage 1: Classification ---
        if '**2' in clean_query or 'x^2' in clean_query:
            classification = "quadratic"
        elif 'x' in clean_query or '=' in clean_query:
            classification = "linear"
        else:
            # If it doesn't match linear or quadratic rules, exit early.
            return ("other", None)

        # --- Stage 2: Aggressive Extraction and Standardization ---
        # NOTE: THIS SECTION MUST BE ALIGNED WITH THE START OF THE FUNCTION BODY

        equation_str = query.lower().strip()

        # 1. Aggressively remove conversational keywords
        for keyword in ['please', 'solve', 'the', 'linear', 'equation', 'find', 'the', 'roots', 'of',
                        'what is the solution to', 'value of x in', 'a', 'an']:
            equation_str = equation_str.replace(keyword, '')

            # 2. Remove all conversational clutter, leaving only numbers, variables, and operators.
        equation_str = re.sub(r'[^\w\=\*\/\+\-\.\^]', '', equation_str)

        # 3. Insert Implicit Multiplication
        equation_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation_str)

        # 4. Final Standardization for SymPy
        equation_str = equation_str.replace('=', '==')
        equation_str = equation_str.replace('^', '**')
        equation_str = equation_str.replace(' ', '')

        # FINAL REPAIR: Handle the x^2 case if it was missed
        if 'x2' in equation_str:
            equation_str = equation_str.replace('x2', 'x**2')

        # Check if the extracted string is still empty or useless
        if not equation_str or equation_str == '==':
            return ("other", None)

        # FINAL SUCCESS RETURN
        return (classification, equation_str)

# --- Day 2 Testing/Verification ---
if __name__ == "__main__":  # <-- THIS IS WHAT TRIGGERS THE TESTS
    lm = LanguageModel()

    # Test 1: Linear
    q1 = "Please solve the linear equation: 4x - 8 = 0"
    print(f"\nQuery 1: {q1}")
    c1, e1 = lm.classify_and_extract(q1)
    print(f"Result: Type={c1}, Extracted={e1}")

    # Test 2: Quadratic
    q2 = "Find the roots of x^2 + 2x - 3 = 0"
    print(f"\nQuery 2: {q2}")
    c2, e2 = lm.classify_and_extract(q2)
    print(f"Result: Type={c2}, Extracted={e2}")

    # Test 3: Unsolvable/Other
    q3 = "What is the history of the number pi?"
    print(f"\nQuery 3: {q3}")
    c3, e3 = lm.classify_and_extract(q3)
    print(f"Result: Type={c3}, Extracted={e3}")