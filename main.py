from Sheep import Sheep
from Herd import Herd
from Wolf import Wolf
import json
import csv

rounds = 50
n_sheep = 15
spawn_limit = 10
sheep_step = 0.5
wolf_step = 1

herd = Herd(n_sheep, sheep_step, spawn_limit)

wolf = Wolf(wolf_step, herd)

json_out = []
csv_out = []
def log_round(round:int, herd:Herd, wolf_pos: complex, closest_sheep: Sheep, killed: bool):
    closest_sheep_idx = herd.sheep.index(closest_sheep)
    msg = f"[Round {round}] "
    msg += f"No. of sheep: {len(herd.alive_sheep)}; "
    msg += f"Wolf at ({wolf_pos.real:.3f}, {wolf_pos.imag:.3f}) " 
    if killed:
        msg += f"killed sheep {closest_sheep_idx}"
    else:
        msg += f"is running after sheep {closest_sheep_idx} at ({closest_sheep.pos.real:.3f}, {closest_sheep.pos.imag:.3f})"
    return msg

for round in range(rounds):
    for s in herd.alive_sheep:
        s.update()
    closest_sheep, killed = wolf.update()
    json_out.append({
        "round_no": round,
        "wolf_pos": [wolf.pos.real, wolf.pos.imag],
        "sheep_pos": [x.json_pos() for x in herd.sheep]
    })
    csv_out.append({
        "round_no": round,
        "n_sheep": len(herd.alive_sheep)
    })
    print(log_round(round, herd, wolf.pos, closest_sheep, killed))
    if not herd.alive_sheep:
        break

with open('pos.json', 'w') as fp:
    json.dump(json_out, fp, indent=4)

with open("alive.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_out[0].keys())
    writer.writeheader()
    writer.writerows(csv_out)