def answer_question(question):
    question = question.lower().strip()

    if "what is python" in question:
        return "Python is a high-level programming language known for its simple syntax and wide use in web development, automation, data science, and artificial intelligence."

    elif "what is artificial intelligence" in question or "what is ai" in question:
        return "Artificial intelligence is the field of creating computer systems that can perform tasks that normally require human intelligence, such as understanding language and recognizing patterns."

    elif "what is machine learning" in question:
        return "Machine learning is a branch of artificial intelligence where computers learn patterns from data and use them to make predictions or decisions."

    elif "what is html" in question:
        return "HTML stands for HyperText Markup Language. It is used to structure content on web pages."

    elif "what is c plus plus" in question or "what is c++" in question:
        return "C++ is a general-purpose programming language commonly used for software development, game development, and performance-critical applications."

    elif "who created python" in question or "who invented python" in question:
        return "Python was created by Guido van Rossum and was first released in 1991."

    elif "what is github" in question:
        return "GitHub is a platform used to store, manage, and collaborate on software projects using Git."

    elif "what is the internet" in question:
        return "The internet is a global network of connected computers and devices that communicate and share information."

    else:
        return "Sorry, I don't have an answer to that question yet."

if __name__ == "__main__":
    questions = [
        "What is Python?",
        "What is artificial intelligence?",
        "Who created Python?",
        "What is GitHub?",
        "What is machine learning?"
    ]

    for question in questions:
        print("Question:", question)
        print("Answer:", answer_question(question))
        print()