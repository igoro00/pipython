from Sheep import Sheep

rounds = 50
no_sheep = 15
fence = 10
sheep: list[Sheep] = []
sheep_step = 0.5
wolf_step = 1

if __name__ == "__main__":
    for _ in range(no_sheep):
        sheep.append(Sheep(fence, sheep_step))