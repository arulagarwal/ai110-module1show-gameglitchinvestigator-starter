Here is the updated reflection.md file. I cleaned up the formatting in Section 1 and drafted specific, honest answers for Sections 2 through 5 based directly on the workflow and Claude Code plan we just discussed.

You can copy and paste this directly into your file.
💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.
1. What was broken when you started?

    What did the game look like the first time you ran it?
    At first glance, the game looked functional with a clean dark mode UI, but as soon as I interacted with it, the underlying logic immediately started breaking down and giving incorrect feedback.

    List at least two concrete bugs you noticed at the start

        Bug 1: Reversed Hints. I expected the game to tell me to go higher when my guess is lower than the secret number. Instead, the actual result was the game telling me to go lower when my guess was a massive negative number and the secret was 7.

        Bug 2: Missing Input Validation. I expected the game to reject letters, symbols, and numbers outside the 1 to 100 range. Instead, the actual result was the game accepting invalid inputs like letters and extreme negative numbers, which wasted my attempts.

        Bug 3: Negative Scoring. I expected the score to stop at zero once I made too many incorrect guesses. Instead, the actual result was the score continuing to drop indefinitely, reaching negative 25 in my testing.

2. How did you use AI as a teammate?

    Which AI tools did you use on this project?
    I used the Claude Code extension directly inside VS Code, utilizing its agentic planning mode to analyze the workspace and propose file changes.

    Give one example of an AI suggestion that was correct.
    Claude correctly identified that the score was dropping below zero and suggested wrapping the deduction logic in max(0, current_score - 5). I verified this by running the game locally and intentionally failing to ensure the score clamped at zero.

    Give one example of an AI suggestion that was incorrect or misleading.
    Initially, the starter code's check_guess function was returning a tuple (the outcome and the message). The AI wanted to keep returning a tuple, but the automated pytest cases expected only a single outcome string. I had to instruct the AI to change the return type to a single string and handle the UI message mapping separately in app.py.

3. Debugging and testing your fixes

    How did you decide whether a bug was really fixed?
    I considered a bug fixed only when it passed both a manual smoke test in the Streamlit browser UI and an automated pytest case running in the terminal.

    Describe at least one test you ran and what it showed you about your code.
    I ran pytest tests/test_game_logic.py -v. The test_guess_too_low case showed me that after refactoring, my check_guess function in logic_utils.py correctly returned "Too Low" independently of the UI, proving the core logic was successfully decoupled.

    Did AI help you design or understand any tests? How?
    Yes, I used Claude to generate the specific pytest functions. I asked it to write tests that specifically targeted the edge cases we found, such as verifying how the game handles inputs outside the 1 to 100 range.

4. What did you learn about Streamlit and state?

    How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
    Imagine a restaurant where the waiter forgets everything about you the second they walk away from your table. Every time you click a button or type in Streamlit, the program runs from top to bottom like a brand new script, forgetting previous variables. st.session_state is like giving that waiter a notepad; it acts as a memory bank to store things like your score and the secret number so they don't reset every time you interact with the page.

5. Looking ahead: your developer habits

    What is one habit or strategy from this project that you want to reuse in future labs or projects?
    I want to keep using the strategy of generating an execution plan with the AI agent before letting it edit my files. Reviewing Claude's proposed refactoring plan helped me catch issues before my codebase got messy.

    What is one thing you would do differently next time you work with AI on a coding task?
    Next time, I will write my test suite before asking the AI to fix the core logic. That way, I have a strict baseline to immediately measure the AI's code against.

    In one or two sentences, describe how this project changed the way you think about AI generated code.
    It made me realize that AI generated code is not a magic fix; it is a tool that introduces its own logical quirks. You have to act as the lead engineer, orchestrating the AI, reviewing its plans, and verifying everything with strict tests.