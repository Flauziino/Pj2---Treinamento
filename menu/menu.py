def linhas(tam=60):
    print('-'*tam)


def titulos(txt):
    linhas()
    print(f'{txt.center(60)}')
    linhas()


def menu(lst):
    for i in lst:
        print(f'   {i}')


def ler_inteiro(txt):
    while True:
        try:
            n = input(txt)
            if n.isdigit():
                num = int(n)
                return num

        except ValueError as error:
            print(error)

        else:
            print('Por favor digite um numero inteiro!')


if __name__ == '__main__':
    titulos('ola')
