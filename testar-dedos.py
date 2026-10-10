"""Executa um teste sequencial dos cinco servos, sem usar a camera."""

import servo_braco3d as mao


def main():
    try:
        mao.testeTodos()
        print("Teste dos dedos concluido.")
    finally:
        mao.fechar()


if __name__ == "__main__":
    main()