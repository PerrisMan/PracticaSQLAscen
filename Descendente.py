        Principal.ejecutarPrompt()
        except IOException as e:
            print("Error al ejecutar el prompt: " + str(e))

    @staticmethod
    def ejecutarPrompt():
        while True:
            linea = input(">>> ")
            if linea is None:
                break  # Presionar Ctrl + D
            Principal.ejecutar(linea)
            Principal.existenErrores = False

    @staticmethod
    def ejecutar(source):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        parser = Parser(tokens)
        parser.parse()

    @staticmethod
    def error(linea, mensaje):
        Principal.reportar(linea, "", mensaje)

    @staticmethod
    def reportar(linea, donde, mensaje):
        print(f"[linea {linea}] Error {donde}: {mensaje}")
        Principal.existenErrores = True
