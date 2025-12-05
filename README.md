# Neuro-Symbolic Math Engine
Project Overview: Guaranteeing Mathematical Accuracy

This project delivers a Tool-Augmented Generation (TAG) system designed to provide 100% mathematically accurate solutions to single-variable algebraic equations. The primary goal was to solve a critical engineering challenge: eliminating calculation errors and hallucinations—the most common failure points for general-purpose Large Language Models (LLMs) in mathematics.

This system runs entirely offline, demonstrating robust deployment capability outside of cloud infrastructure.

# Strategic Scope
The system is strictly scoped to single-variable linear and quadratic equations. This limitation is a deliberate engineering decision made to prioritize reliability and verifiable accuracy over generalized, but unreliable, breadth of knowledge. We ensure the system does a few things perfectly, rather than many things poorly.

# Architecture and Technical Rationale
The core innovation lies in separating the natural language processing (handled by a neural network) from the formal computation (managed by a symbolic solver).

## 1. The Neuro Component (Language Model)
The neural component handles all interaction with the user, ensuring the system can communicate in human language while maintaining mathematical integrity.

(i) Parser/Classifier (src/language_model.py): This module uses a lightweight DistilBERT tokenizer and rule-based logic to perform Natural Language Understanding (NLU). Its job is to classify the user's intent (e.g., "Is this a quadratic equation?") and aggressively strip away all conversational noise and unnecessary words, leaving only a clean, machine-readable algebraic string (e.g., converting "Solve 4x minus 8" to "4*x - 8 == 0").

(ii) Output Formatter (src/chatbot_math.py): After the computation is complete, this module translates the raw, technical output from the solver (e.g., SymPy's list of rational numbers) into a clean, professional $\LaTeX$-formatted response for the user.

## 2. The Symbolic Component (Solver Engine)
This is the core of the Tool-Augmented Generation (TAG) strategy, ensuring verifiable truth.

(i) Computational Core (src/solver_engine.py): This wraps the SymPy library, making it the system's single source of truth for all computation. It guarantees $100\%$ accuracy because it relies on formal mathematical algorithms (like the quadratic formula and algebraic reduction) rather than statistical prediction.

(ii) Role in TAG: The LLM is prohibited from calculating. Computation is offloaded to SymPy, which returns the provably correct result.

## 3. The Orchestrator (MathChatbot)
The MathChatbot class in main.py and src/chatbot_math.py serves as the central agent.

(i) It routes the cleaned query from the Parser to the Solver.

(ii) It implements the Graceful Refusal logic, ensuring that if a query falls outside the scope (e.g., "What is a derivative?"), the system responds politely and professionally with the defined scope message, rather than crashing or guessing.

# Setup and Execution: 

## Prerequisites

(i) Python 3.8+
(ii) A stable internet connection is required for the initial model and dependency downloads.

## 1. Installation

(i) Clone the repository and navigate to the project root.

(ii) Create and activate a virtual environment (venv).

(iii) Install all required dependencies:
  ### pip install sympy transformers torch

## 2. Running the Chatbot

Execute the main entry point file:

### python main.py

# System Verification (Demonstration of Reliability)
The following test cases demonstrate the system's proficiency in handling key algebraic challenges, proving the successful integration of NLU and Symbolic Computation.

## Test 1: Linear Equation and Clean Output

(i) Query: Solve 4x - 8 = 0

(ii) Verification Point: The system correctly parses the implicit multiplication (4x becomes 4*x) and solves the equation.

(iii) Expected Output: The single solution for x is: 2.

## Test 2: Quadratic Equation and Multi-Root Solution

(i) Query: Find roots of x^2 + 2x - 3 = 0

(ii) Verification Point: Proves the parser correctly handles the power syntax (x^2 becomes x**2).

(iii) Expected Output: The solutions for x are: 1 and -3.

## Test 3: Fractional Precision

(i) Query: 2x^2 + 5x - 3 = 0

(ii) Verification Point: Confirms the SymPy solver handles fractional roots exactly, and the formatter cleanly presents the $\LaTeX$ fraction.

(iii) Expected Output: The solutions for x are: $\frac{1}{2}$ and $-3$.

## Test 4: Scope Control (Graceful Refusal)

(i) Query: What is the history of the number pi?

(ii) Verification Point: Proves the orchestrator correctly identifies out-of-scope intent and provides a professional response.

(iii) Expected Output: I am currently a specialized algebraic solver. I can only solve single-variable linear and quadratic equations...
