from model.model import Model

m = Model()

print("=" * 40)
print("Bienvenido a la oficina del LicencIAdo!")
print("Escribe 'gracias' para salir.")
print("=" * 40)

while True:
    question = input("> ")
    if question.lower().strip() == 'gracias':
        print("\nAdiós")
        break

    res, ctx = m.ask_question(question)
    print()
    print(res)
    print("-" * 80)