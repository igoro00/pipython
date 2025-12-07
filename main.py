from Sheep import Sheep
from Herd import Herd
from Wolf import Wolf
import json
import csv
import argparse
import configparser
import logging
logger = logging.getLogger(__name__)
def main():
    parser = argparse.ArgumentParser(
        prog="python main.py",
    )
    parser.add_argument("-c", "--config", type=str)
    parser.add_argument("-l", "--log", type=int)
    parser.add_argument("-r", "--rounds", default=50, type=int)
    parser.add_argument("-s", "--sheep", default=15, type=int)
    parser.add_argument("-w", "--wait", action="store_true")

    args = vars(parser.parse_args())

    rounds = args["rounds"]
    n_sheep = args["sheep"]
    wait = args["wait"]
    log = args["log"]

    if log is not None:
        logging.basicConfig(
            filename="chase.log", 
            filemode='w', 
            level=log,
            format='%(asctime)s %(levelname)s %(message)s'
        )

    spawn_limit = 10
    sheep_step = 0.5
    wolf_step = 1

    if args["config"]:
        config = configparser.ConfigParser()
        config.read(args["config"])
        # TODO: error handling
        spawn_limit = float(config["Sheep"]["InitPosLimit"])
        sheep_step = float(config["Sheep"]["MoveDist"])
        wolf_step = float(config["Wolf"]["MoveDist"])
        logger.debug(f"Configuration has been loaded from {args['config']}:\n\tspawn_limit: {spawn_limit}, sheep_step: {sheep_step}, wolf_step: {wolf_step}")

    herd = Herd(n_sheep, sheep_step, spawn_limit)
    logger.info("Initial positions of all sheep were determined")
    logger.debug(f"Sheep positions:\n{"\n".join([f" - [{i}] {x.json_pos()}" for i, x in enumerate(herd.sheep)])}")

    wolf = Wolf(wolf_step, herd)

    json_out = []
    csv_out = []
    def log_round(round:int, herd:Herd, wolf_pos: complex, closest_sheep: Sheep, killed: bool):
        msg = f"[Round {round}] "
        msg += f"No. of sheep: {len(herd.sheep)}; "
        msg += f"Wolf at ({wolf_pos.real:.3f}, {wolf_pos.imag:.3f}) " 
        if killed:
            msg += f"killed sheep {closest_sheep.i}"
        else:
            msg += f"is chasing sheep {closest_sheep.i} at ({closest_sheep.pos.real:.3f}, {closest_sheep.pos.imag:.3f})"
        return msg

    for round in range(rounds):
        round += 1
        logger.info(f"New round started: %d", round)
        herd.update()
        logger.info(f"All sheep moved")
        closest_sheep, killed = wolf.update()
        json_out.append({
            "round_no": round,
            "wolf_pos": [wolf.pos.real, wolf.pos.imag],
            "sheep_pos": [x.json_pos() for x in herd.sheep] # TODO: musi wpisywać none dla martwych owiec a tutaj sa tylko zywe
        })
        csv_out.append({
            "round_no": round,
            "n_sheep": len(herd.sheep)
        })
        print(log_round(round, herd, wolf.pos, closest_sheep, killed))
        logger.info(f"The round ended - {len(herd.sheep)} sheep remaining...")
        if not herd.sheep:
            logger.info("Simulation terminated - all sheep have been eaten")
            break
        if wait:
            input("Press Enter to continue...")
        if round == rounds:
            logger.info("Simulation terminated - reached round limit")

    with open('pos.json', 'w') as fp:
        json.dump(json_out, fp, indent=4)
        logger.debug("Wrote to pos.json")

    with open("alive.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_out[0].keys())
        writer.writeheader()
        writer.writerows(csv_out)
        logger.debug("Wrote to alive.csv")

if __name__ == "__main__":
    main()