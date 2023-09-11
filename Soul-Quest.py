from dataclasses import dataclass
import random
import time
import os
import ast


# add change inventory function and print inventory function
@dataclass
class Player:
    name: str
    race: str
    attributes: dict
    skillpoints: int
    xp: list
    level: int
    inventory: dict

    def print_inventory(user):
        print("Inventory:")
        for key, value in user.inventory.items():
            for k, v in value.items():
                print(f"{key}. {k}:{v}")

    def edit_inventory(user):
        while True:
            print("Inventory:")
            for key, value in user.inventory.items():
                for k, v in value.items():
                    print(f"{key}. {k}:{v}")
            try:
                slot = input("Enter the slot number you want to change? or [quit]\n> ")
                if slot == "quit":
                    return
                elif int(slot) in user.inventory:
                    slot = int(slot)
                else:
                    raise ValueError
                while True:
                    try:
                        newslot = int(
                            input(
                                f"Enter slot of item you want in place of slot {slot}:\n>"
                            )
                        )
                        if slot in user.inventory:
                            slot_item = user.inventory[slot]
                            newslot_item = user.inventory[newslot]
                            user.inventory[slot] = newslot_item
                            user.inventory[newslot] = slot_item
                            print("\033c", end="")
                            break
                    except (ValueError, KeyError):
                        print("Please enter a valid slot")
            except ValueError:
                print("\033c", end="")
                print("Cannot change that slot")

    def print_attributes(user):
        for i, (k, v) in enumerate(user.attributes.items()):
            print(f"{i + 1}. {k}:{v}")

    def update_attributes(user):
        while True:
            print(f"LVL {user.level}: {user.xp[0]:,.3f}/{user.xp[1]:,.3f}")
            print(
                f"""You have {user.skillpoints} {'point' if user.skillpoints  == 1 else 'points'} left."""
            )
            user.print_attributes()
            attributes = {
                1: "Health",
                2: "Stamina",
                3: "Mana",
                4: "Intelligence",
                5: "Grit",
                6: "Damage",
            }
            try:
                userinput = input(
                    "Enter the number next to the attribute you would like to change or [quit].\n> "
                )
                if userinput == "quit":
                    return
                elif userinput.isdigit():
                    if int(userinput) in attributes:
                        userinput = int(userinput)
                        userchoice = attributes[userinput]
                        while True:
                            try:
                                points = int(input("Amt of points: "))
                                if points > user.skillpoints:
                                    print("\033c", end="")
                                    print(
                                        f"Amount cannot exceed current number of skillpoints, you have {user.skillpoints}"
                                    )
                                    break
                                else:
                                    user.attributes[userchoice] += points * 10
                                    user.skillpoints -= points
                                    print("\033c", end="")
                                    break
                            except ValueError:
                                print("Use yo common sense cuh")
                else:
                    print("\033c", end="")
                    raise ValueError
            except:
                print("Invalid Choice")


def use_inventory_item(user, item, health, mana):
    item_type = {
        "Weapon": ["Wooden Sword", "Steel Sword"],
        "Healing": ["Health Potion", "Mana Potion"],
        "Currency": ["Gold"],
    }
    weapons = {"Wooden Sword": 25, "Steel Sword": 45}
    healing = {"Health Potion": 50, "Mana Potion": 50}
    item_name = ""
    type = ""
    for k, v in item.items():
        item_name = k

    for k, v in item_type.items():
        if item_name in v:
            type = k
    if type == "Healing":
        amt = healing[item_name]
        return ("health", amt)

    elif type == "Weapon":
        amt = weapons[item_name]
        return ("damage", amt)

    else:
        print("item not in game yet")
        return ("nothing", 0)


@dataclass
class Environment:
    name: str
    monsters: list
    xp_boost: float
    areas: list


@dataclass
class Monster:
    name: str
    health: int
    damage: int
    drops: list
    xp: int


races = {
    "Orc": {
        "Health": 150,
        "Stamina": 110,
        "Mana": 100,
        "Intelligence": 100,
        "Grit": 120,
        "Damage": 120,
    },
    "Human": {
        "Health": 100,
        "Stamina": 120,
        "Mana": 120,
        "Intelligence": 150,
        "Grit": 120,
        "Damage": 100,
    },
    "Khajit": {
        "Health": 110,
        "Stamina": 150,
        "Mana": 100,
        "Intelligence": 120,
        "Grit": 120,
        "Damage": 100,
    },
    "Reptile": {
        "Health": 110,
        "Stamina": 110,
        "Mana": 150,
        "Intelligence": 110,
        "Grit": 120,
        "Damage": 100,
    },
}


# starts the game
def get_saved_characters():
    saved_characters = []
    for file in os.listdir():
        if ".txt" in file:
            saved_characters.append(file.split("-")[0])
    return saved_characters


def choose_character(characters):
    while True:
        print("You have these saved characters: ")
        for i, char in enumerate(characters):
            print(f"{i+1}. {char}")
        choice = input("Enter character name or [quit]: ")
        if choice in characters:
            return choice
        elif choice == "quit":
            return
        print("\033c", end="")
        print(f"{choice} does not exist")


def init_game(environments):
    print("Welcome to Soul quest.\nAre you ready to play?")
    file = ""
    while True:
        user_input = input("> ")
        if user_input[0] in ["y", "Y"]:
            characters = get_saved_characters()
            break
        elif user_input == "no":
            return
        else:
            print("invalid input")

    while True:
        user_input = input("Would you like to load a character?[yes/no]\n> ")
        if user_input == "yes":
            file = f"{choose_character(characters)}-file.txt"
            if file != "None-file.txt":
                return load_file(file)
            pass
        elif user_input == "no":
            return init_player(races), Environment(
                name="Town",
                monsters=None,
                xp_boost=1,
                areas=["Home", "Merchant", "Forest"],
            )
        elif user_input == "quit":
            return
        else:
            print("\033c", end="")
            print("Alright say yes or no")


# initializes the player
def init_player(races):
    for i, key in enumerate(races):
        print(f"{i+1}. {key}")
    while True:
        race = input("Enter the name of your desired race:\n>")
        if race in races:
            name = input(f"Enter the name of your {race}:\n>")
            player = Player(name, race, races[race], 5, [0, 50], 0, {})
            player.inventory = {
                1: {"Wooden Sword": 1},
                2: {"Wooden Shield": 1},
                3: {"Spell Staff": 1},
                4: {"Health Potion": 5},
                5: {"Mana Potion": 5},
                6: {"Gold": 100},
            }
            return player
        else:
            print(f"{race} does not exist.")


def init_environments() -> list:
    Tundra = Environment(
        "Tundra", [], 1.25, ["Cave", "Ice Forest", "Icy Mountains", "Merchant", "Camp"]
    )
    Town = Environment("Town", [], 1, ["Home", "Merchant", "Forest"])
    Volcanic = Environment(
        "Volcanic",
        [],
        1.5,
        ["Eruptive Fissure", "Fissure Cave", "Magma Chamber", "Cave"],
    )
    return [Tundra, Town, Volcanic]


def valid_area_transition(userinput, environment):
    ...


def transition_area(userinput, environment):
    ...


def init_monsters(environment):
    print(environment)
    if environment.name == "Tundra":
        return [
            Monster(
                "Ice Dragon",
                500,
                50,
                [{"Dragon heart": 1}, {"Ice Dragon Scales": 5}, {"Ice Dragon Soul": 1}],
                200,
            ),
            Monster(
                "Yeti",
                150,
                25,
                [{"Yeti Head": 1}, {"Yeti Soul": 1}, {"Steel Sword": 1}],
                65,
            ),
        ]

    elif environment.name == "Town":
        return [
            Monster("Bandit", 50, 10, [{"Gold": 10}, {"Iron Dagger": 1}], 15),
            Monster("Rat", 10, 5, [{"Rat Head": 1}, {"Rat Fur": 1}, {"Gold": 1}], 5),
        ]

    elif environment.name == "Volcanic":
        return [
            Monster("Barlog", 300, 35, [{"Gold": 100}, {"Iron Dagger": 1}], 300),
            Monster(
                "Fire Serpent",
                200,
                40,
                [{"Fire Scales": 1}, {"Fire Essence": 1}, {"Gold": 50}],
                150,
            ),
        ]


def get_rand_monster(monsters):
    num = random.randint(0, len(monsters))
    return monsters[num - 1]


def get_rand_area(environment, area):
    while True:
        num = random.randint(0, len(environment.areas))

        if environment.areas[num - 1] not in [area, "Home"]:
            return environment.areas[num - 1]


def fight_choice(player):
    while True:
        try:
            user_input = input("> ")
            if user_input == "run away":
                return "run away"
            elif int(user_input) in player.inventory:
                dict = player.inventory[int(user_input)]
                return dict
            else:
                raise ValueError
        except ValueError:
            print("Dam cuh")


def fight(player, monster):
    player_health = player.attributes["Health"]
    player_mana = player.attributes["Mana"]
    monster_health = monster.health
    print("\033c", end="")
    while player_health > 0 and monster_health > 0:
        print(
            f"""Your Health: {player_health:,.2f}
{monster.name} Health: {monster_health:,.2f}
Your inventory[enter number to select item and use or 'run away']:
"""
        )
        player.print_inventory()
        combat_choice = fight_choice(player)
        if combat_choice == "run away":
            return "run away"
        item_type, damage = use_inventory_item(
            player, combat_choice, player_health, player_mana
        )
        if item_type == "insufficient":
            pass
        elif item_type == "health":
            player_health += damage
            print("\033c", end="")
        elif item_type == "damage":
            crit = 0
            if player.attributes["Intelligence"] <= 100:
                crit = random.randint(1, 10)
            elif player.attributes["Intelligence"] <= 150:
                crit = random.randint(1, 8)
            elif player.attributes["Intelligence"] <= 200:
                crit = random.randint(1, 6)
            elif player.attributes["Intelligence"] <= 250:
                crit = random.randint(1, 4)
            elif player.attributes["Intelligence"] <= 300:
                crit = random.randint(1, 2)
            else:
                crit = 1
            if crit == 1:
                monster_health -= 2 * (damage * (player.attributes["Damage"] / 100))
                print("\033c", end="")
                print(
                    f"Critical hit! You did {2*(damage * (player.attributes['Damage'] / 100)):,.2f} damage to the {monster.name}"
                )

            else:
                monster_health -= damage * (player.attributes["Damage"] / 100)
                player_health -= monster.damage - (player.attributes["Grit"] / 20)
                print("\033c", end="")
                print(
                    f"You did {damage*(player.attributes['Damage'] / 100)} damage to the {monster.name}"
                )
                print(
                    f"You took {(monster.damage - (player.attributes['Grit'] / 20)):,.2f} damage"
                )
        else:
            pass
        if monster_health < 1:
            return True
        elif player_health < 1:
            return False
        else:
            pass


def sleep(player):
    print("Sleeping.................")
    time.sleep(10)


def give_xp(player, entity):
    player.xp[0] += entity.xp
    while player.xp[0] > player.xp[1]:
        player.level += 1
        player.skillpoints += 1
        player.xp[0] -= player.xp[1]
        player.xp[1] *= 1.15
    return


def give_loot(player, entity):
    drops = entity.drops
    for drop in drops:
        for k, v in drop.items():
            for slot, item in player.inventory.items():
                if k in item.keys():
                    player.inventory[slot][k] += v
                    drops.remove(drop)
    for drop in drops:
        for k, v in drop.items():
            i = max(player.inventory.keys())
            player.inventory[i + 1] = {k: v}

    return


def interact_area(area, player, monster, environment):
    while True:
        print(f"You have found a(n) {area}")
        if area in ["Merchant", "Home", "Camp"]:
            if area == "Merchant":
                print("Would you like to shop?[yes/no]")  # Shop
                user_input = input("> ")
                if user_input == "yes":
                    # shop function
                    print("\033c", end="")
                    print("Not available right now")
                    return area
                elif user_input == "no":
                    print("\033c", end="")
                    return get_rand_area(environment, area)
                else:
                    print("\033c", end="")
                    print("invalid action")
            elif area in ["Home", "Camp"]:
                print("Sleep?[yes/no]")
                user_input = input("> ")
                if user_input in ["y", "yes", "yea", "ye"]:
                    print("\033c", end="")
                    sleep(player)
                elif user_input == "no":
                    print("\033c", end="")
                    return get_rand_area(environment, area)
                    pass
                else:
                    print("\033c", end="")
                    print("Invalid response")
        else:
            user_input = input(
                "Would you like to continue down this path?[yes/no/return] \n> "
            ).lower()
            if user_input in ["yes", "y", "yea", "ye"]:
                won = fight(player, monster)
                if won == "run away":
                    print("\033c", end="")
                    print("You ran away, luckily the monster stopped following")
                elif won == True:
                    print(f"You defeated the {monster.name}")
                    give_loot(player, monster)
                    give_xp(player, monster)
                else:
                    print("You died.")

            elif user_input == "return":
                print("\033c", end="")
                return "leave"
            elif user_input == "no":
                print("\033c", end="")
                return get_rand_area(environment, area)
            else:
                print("\033c", end="")
                print("Invalid action")


def explore(player, area, environment, monsters):
    area = get_rand_area(environment, None)
    while True:
        monster = get_rand_monster(monsters)
        area = interact_area(area, player, monster, environment)
        if area == "leave":
            return


# dont forget to ask for loaded data or create new data or overwrite data
def change_environment(environments):
    print("Where would you like to go?")
    for i, loco in enumerate(environments):
        print(f"{i+1}. {loco.name}")
    while True:
        try:
            user_input = int(input("[Enter number]: "))
            return environments[user_input - 1]
        except (IndexError, ValueError):
            print("Invalid Choice")


def save_game(player, environment, area):
    with open(f"{player.name}-file.txt", "w") as file:
        file.write(
            f"""{player.name}
{player.race}
{player.attributes}
{player.skillpoints}
{player.xp}
{player.level}
{player.inventory}
"""
        )

        file.write(
            f"""{environment.name}
{environment.monsters}
{environment.xp_boost}
{environment.areas}
"""
        )
        file.write(f"{area}")


def load_file(file):
    with open(f"{file}", "r") as file:
        contents = file.read().split("\n")
        player = Player(
            contents[0],
            contents[1],
            ast.literal_eval(contents[2]),
            int(contents[3]),
            ast.literal_eval(contents[4]),
            int(contents[5]),
            ast.literal_eval(contents[6]),
        )
        environment = Environment(
            contents[7], contents[8], float(contents[9]), ast.literal_eval(contents[10])
        )

        return player, environment


def main():
    environments = init_environments()
    try:
        player, player_environment = init_game(environments)
    except TypeError:
        print("Have a good day then")
        return
    if not player:
        return
    player_area = get_rand_area(player_environment, None)
    while True:
        monsters = init_monsters(player_environment)
        print("\033c", end="")
        print(
            f"You are in the {player_area} area, located in the {player_environment.name} region. \n"
        )
        print(
            """Here are your options:
    1. Explore
    2. Change Environment
    3. Update Attributes
    4. Edit Inventory
    5. Quit
    [Enter Number:]
    """
        )
        try:
            user = int(input("> "))
            if user == 1:
                explore(player, player_area, player_environment, monsters)
            elif user == 2:
                player_environment = change_environment(environments)
                player_area = get_rand_area(player_environment, None)
            elif user == 3:
                player.update_attributes()
            elif user == 4:
                player.edit_inventory()
            elif user == 5:
                save_game(player, player_environment, player_area)
                break
            else:
                print("\033c", end="")
                print("Invalid Action")
        except ValueError:
            print("\033c", end="")
            print("Invalid Action")


if __name__ == "__main__":
    main()
