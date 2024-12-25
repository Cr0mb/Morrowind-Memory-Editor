import os
import pymem
import pymem.process

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_memory_value(pm, base_address, offsets):
    address = pm.read_int(base_address)
    for offset in offsets[:-1]:
        address = pm.read_int(address + offset)
    return pm.read_float(address + offsets[-1])

def write_memory_value(pm, base_address, offsets, new_value):
    address = pm.read_int(base_address)
    for offset in offsets[:-1]:
        address = pm.read_int(address + offset)
    pm.write_float(address + offsets[-1], new_value)

def display_categories(categories):
    print("\nAvailable categories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

def display_attributes(attributes):
    print("\nAvailable attributes:")
    for i, attribute in enumerate(attributes, start=1):
        print(f"{i}. {attribute}")

def display_all_items(pm, base_address, categories):
    print("\nAll Items and Their Values:\n")
    for category, attributes in categories.items():
        print(f"== {category} ==")
        for attribute, offsets in attributes.items():
            if isinstance(offsets[0], list):
                value_1 = read_memory_value(pm, base_address, offsets[0])
                value_2 = read_memory_value(pm, base_address, offsets[1])
                print(f"{attribute}: {value_1}, {value_2}")
            else:
                value = read_memory_value(pm, base_address, offsets)
                print(f"{attribute}: {value}")
        print()

def main():
    try:
        pm = pymem.Pymem("Morrowind.exe")
        base_address = pymem.process.module_from_name(pm.process_handle, "Morrowind.exe").lpBaseOfDll + 0x003C67DC

        categories = {
            "Core Attributes": {
                "Health_Max": [0x438, 0x2B8],
                "Health": [0x438, 0x2BC],
                "Mana_Max": [0x438, 0x2C4],
                "Mana": [0x438, 0x2C8],
                "Stamina_Max": [0x438, 0x2DC],
                "Stamina": [0x438, 0x2E0],
                "Max_Inventory_Space": [0x438, 0x2D0],
                "Inventory_Space": [0x438, 0x2D4],
            },
            "Player Stats": {
                "Strength": [[0x438, 0x25C], [0x438, 0x258]],
                "Intelligence": [[0x438, 0x264], [0x438, 0x268]],
                "Willpower": [[0x438, 0x270], [0x438, 0x274]],
                "Agility": [[0x438, 0x27C], [0x438, 0x280]],
                "Speed": [[0x438, 0x288], [0x438, 0x28C]],
                "Endurance": [[0x438, 0x294], [0x438, 0x298]],
                "Personality": [[0x438, 0x2A0], [0x438, 0x2A4]],
                "Luck": [[0x438, 0x2AC], [0x438, 0x2B0]],
            },
            "Misc Skills": {
                "Block": [[0x438, 0x3B4], [0x438, 0x3B8]],
                "Armorer": [[0x438, 0x3C4], [0x438, 0x3C8]],
                "Medium_Armor": [[0x438, 0x3D4], [0x438, 0x3D8]],
                "Heavy_Armor": [[0x438, 0x3E4], [0x438, 0x3E8]],
                "Blunt_Weapon": [[0x438, 0x3F4], [0x438, 0x3F8]],
            },
            "Minor Skills": {
                "Athletics": [[0x438, 0x434], [0x438, 0x438]],
                "Mercantile": [[0x438, 0x554], [0x438, 0x558]],
                "Hand_to_Hand": [[0x438, 0x544], [0x438, 0x548]],
                "Speechcraft": [[0x438, 0x534], [0x438, 0x538]],
                "Marksman": [[0x438, 0x524], [0x438, 0x528]],
            },
            "Major Skills": {
                "Short_Blade": [[0x438, 0x514], [0x438, 0x518]],
                "Light_Armor": [[0x438, 0x504], [0x438, 0x508]],
                "Acrobatics": [[0x438, 0x4F4], [0x438, 0x4F8]],
                "Sneak": [[0x438, 0x4E4], [0x438, 0x4E8]],
                "Security": [[0x438, 0x4D4], [0x438, 0x4D8]],
            },
        }
        while True:
            clear_screen()
            print("Morrowind Memory Editor")
            print("[+] Made by Cr0mb [+]\n")
            print("\nMain Menu:")
            print("1. View categories and modify values")
            print("2. Print all items and their values")
            print("3. Exit")
            choice = input("\nEnter your choice: ")

            if choice == "1":
                display_categories(categories)
                category_choice = input("\nSelect a category by number (or type 'back' to return to the main menu): ")
                if category_choice.lower() == 'back':
                    continue

                try:
                    category_choice = int(category_choice) - 1
                    category_keys = list(categories.keys())
                    selected_category = category_keys[category_choice]
                    attributes = categories[selected_category]
                except (ValueError, IndexError):
                    print("Invalid choice. Please try again.")
                    continue

                while True:
                    clear_screen()
                    display_attributes(attributes)
                    attribute_choice = input("\nSelect an attribute by number (or type 'back' to go back): ")
                    if attribute_choice.lower() == 'back':
                        break

                    try:
                        attribute_choice = int(attribute_choice) - 1
                        attribute_keys = list(attributes.keys())
                        selected_attribute = attribute_keys[attribute_choice]
                        offsets = attributes[selected_attribute]
                    except (ValueError, IndexError):
                        print("Invalid choice. Please try again.")
                        continue

                    current_value = read_memory_value(pm, base_address, offsets)
                    print(f"\nCurrent value of {selected_attribute}: {current_value}")

                    new_value = input(f"Enter new value for {selected_attribute} (or type 'cancel' to cancel): ")
                    if new_value.lower() == 'cancel':
                        continue

                    try:
                        new_value = float(new_value)
                        write_memory_value(pm, base_address, offsets, new_value)
                        print(f"Value of {selected_attribute} successfully updated to {new_value}.")
                    except ValueError:
                        print("Invalid value. Please enter a numeric value.")

            elif choice == "2":
                clear_screen()
                display_all_items(pm, base_address, categories)
                input("\nPress Enter to return to the main menu...")

            elif choice == "3":
                break

            else:
                print("Invalid choice. Please try again.")

    except pymem.exception.ProcessNotFound:
        print("Morrowind.exe process not found. Make sure the game is running.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()