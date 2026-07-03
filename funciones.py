import random

def RegistrarCorredor(corredores):
    while True:
        try:
            cantidad = int(input("Ingresa la cantidad de corredores a registrar: "))
            if cantidad <= 0:
                print("Ingresa una cantidad mayor a 0")
            else:
                print("Guardados con exito")
                break
        except ValueError:
            print("Ingresa un valor valido")

    for i in range(cantidad):
        while True:
            conductor = input("Ingresa el nombre del conductor: ").strip()

            if conductor:
                break
            print("El nombre no puede estar vacio")

        while True:
            auto = input("Ingresa el modelo del auto: ").strip()

            if auto:
                break

            print("El modelo no puede estar vacio")

        while True:
            try:
                apuesta = float(input("Ingresa la apuesta del conductor: "))

                break

            except ValueError:
                print("Ingresa un monto valido")

        corredor = {
            "conductor": conductor,
            "auto": auto,
            "apuesta": apuesta
        }
        
        corredores.append(corredor)

    return cantidad
  

def VerCorredores(corredores):

    print(f"CORREDORES ({len(corredores)})")

    for c in corredores:

        print(f'{{ {c["conductor"]}, {c["auto"]}, {c["apuesta"]} }}')
    print()


def IniciarCarrera(corredores):
    if not corredores:
        print("No hay corredores registrados")
        return None
    return random.choice(corredores)