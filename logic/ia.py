import g4f

if __name__ == '__main__':
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                "role": "user",
                "content": "Bonjour",
            },
            {
                "role": "assistant",
                "content": "Bonjour je suis ton psy et je vais aider à comprendre et résoudre tes problèmes. Comment "
                           "puis-je t'aider aujourd'hui ?",
            },
            {
                "role": "user",
                "content": "Bonjour, jai des problemes avec ma femme comment faire ?",
            }
        ],
        provider=g4f.Provider.DeepAi,
    )

    print(response)
