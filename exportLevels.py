import os
import random

import matplotlib.pyplot as plt
from PIL import Image
# Import your existing logic from your main file
from levelGenWeb import find_paths, draw_paths_streamlit, get_random_edge_point, levels


def export_level_images():
    # 1. Configuration for the export
    levels_to_export = levels

    # 2. Create export directory if it doesn't exist
    if not os.path.exists("exports"):
        os.makedirs("exports")
        print("Created /exports directory.")

    for name, config in levels_to_export.items():
        print(f"Generating {name}...")

        # 3. Get a random start point on the edge
        start_pt = get_random_edge_point(config["A"])

        # 4. Find paths using your algorithm
        paths = find_paths(
            A=config["A"],
            start=get_random_edge_point(config["A"]),
            required_turns=config["turns"],
            min_length=config["min_len"],
            max_length=config["max_len"],
            allow_crossing=False,
            min_straight_length=config["min_straight_length"]
        )

        if paths:
            # 5. Draw the path using your existing image logic
            fig = draw_paths_streamlit(
                A=config["A"],
                paths=paths,
                level_folder=config["level"],
                max_allowed_images=config["max_images"]
            )

            # 6. Save the figure as a high-quality PNG
            file_path = f"exports/{name}_map.png"
            fig.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close(fig)  # Close to free up memory
            print(f"✅ Saved to {file_path}")
        else:
            print(f"❌ Could not generate a valid path for {name}")

def mass_export():
    base_export_dir = "all_exported_levels"

    for folder_name, config in levels.items():
        print(folder_name)
        if folder_name != "Level 3":
            continue
        # 1. Create a specific folder for this level (e.g., all_exported_levels/level1)
        level_dir = os.path.join(base_export_dir, folder_name)
        if not os.path.exists(level_dir):
            os.makedirs(level_dir)
            print(f"Created directory: {level_dir}")

        # 2. Since find_paths needs a starting point, we loop through all possible edge starts
        # to find EVERY possible path for the grid size.
        all_possible_paths = []

        # Checking every perimeter cell as a potential starting point
        edge_points = []
        for i in range(config["A"]):
            edge_points.extend([(0, i), (config["A"] - 1, i), (i, 0), (i, config["A"] - 1)])
        edge_points = list(set(edge_points))  # Remove corner duplicates

        print(f"Searching for all paths for {folder_name}...")
        for start_node in edge_points:
            paths = find_paths(
                A=config["A"],
                start=start_node,
                required_turns=config["turns"],
                min_length=config["min_len"],
                max_length=config["max_len"],
                allow_crossing=True,
                min_straight_length=config["min_straight_length"]
            )
            if paths:
                all_possible_paths.extend(paths)

        print(f"Found {len(all_possible_paths)} total paths for {folder_name}. Exporting images...")

        # 3. Export each path as its own image
        for idx, path in enumerate(all_possible_paths):
            if random.randint(0, 200000) > 1:
                continue
            # We wrap the single path in a list because draw_paths_streamlit expects a list of paths
            fig = draw_paths_streamlit(
                A=config["A"],
                paths=[path],
                level_folder=config['level'],
                max_allowed_images=config["max_images"]
            )

            file_name = f"path_{idx:03d}.png"  # Saves as path_001.png, path_002.png
            file_path = os.path.join(level_dir, file_name)

            fig.savefig(file_path, dpi=150, bbox_inches='tight')
            plt.close(fig)  # Critical to prevent memory crashes

          #  if idx % 10 == 0:
            print(f"Progress: {idx}/{len(all_possible_paths)} images saved...")

    print("\n✅ All levels exported successfully to the /all_exported_levels folder!")


if __name__ == "__main__":
    mass_export()


# if __name__ == "__main__":
#     export_level_images()