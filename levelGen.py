import numpy as np
from PIL import Image
from numpy.f2py.auxfuncs import throw_error


def find_paths(
        A,
        start,
        required_turns,
        min_length,
        max_length,
        allow_crossing,
        min_straight_length=1
):

    minimum_required_length = (required_turns + 1) * min_straight_length
    print(str(minimum_required_length) +", " + str(min_length))
    if minimum_required_length > max_length or min_straight_length > A:
        raise ValueError('Minimum required length ' + str(minimum_required_length) + ' is more than than max length ' + str(max_length))


    directions = [
        (-1, 0),  # up
        (1, 0),  # down
        (0, -1),  # left
        (0, 1)  # right
    ]

    paths = []
    visited = [[False] * A for _ in range(A)] if not allow_crossing else None

    def dfs(r, c, prev_dir, turns, length, current_path, segment_length):

        # Global pruning
        if length > max_length or turns > required_turns:
            return

        # If valid path length & exact turns
        if min_length <= length <= max_length and turns == required_turns:
            if segment_length >= min_straight_length:
                paths.append(current_path.copy())

        # Stop at max length
        if length == max_length:
            return

        for i, (dr, dc) in enumerate(directions):
            nr, nc = r + dr, c + dc

            if not (0 <= nr < A and 0 <= nc < A):
                continue

            if not allow_crossing and visited[nr][nc]:
                continue

            new_turns = turns

            # First move
            if prev_dir is None:
                new_segment_length = 1

            # Continue straight
            elif prev_dir == i:
                new_segment_length = segment_length + 1

            # Turning
            else:
                # Cannot turn if last segment too short
                if segment_length < min_straight_length:
                    continue

                # Cannot exceed required turns
                if turns + 1 > required_turns:
                    continue

                new_turns = turns + 1
                new_segment_length = 1

            if not allow_crossing:
                visited[nr][nc] = True

            current_path.append([nr, nc])

            dfs(
                nr,
                nc,
                i,
                new_turns,
                length + 1,
                current_path,
                new_segment_length
            )

            current_path.pop()

            if not allow_crossing:
                visited[nr][nc] = False

    sr, sc = start

    if not allow_crossing:
        visited[sr][sc] = True

    dfs(sr, sc, None, 0, 0, [[sr, sc]], 0)

    return paths


import matplotlib.pyplot as plt
import numpy as np
import random


def draw_paths(A, paths, show_grid=False, save_path=None):
    """
    A: grid size (A x A)
    paths: array of paths (each path is [[r,c], ...])
    show_grid: draw grid lines
    save_path: filename to save image (optional)
    """

    fig, ax = plt.subplots(figsize=(6, 6))

    # Load square texture
    square_img = Image.open('images/Vex123Sqaure.png').convert('RGB')
    square_img = np.array(square_img)

    # Draw grid background
    grid = np.zeros((A, A))
    # Draw textured grid
    for r in range(A):
        for c in range(A):
            ax.imshow(
                square_img,
                extent=(c - 0.5, c + 0.5, r + 0.5, r - 0.5)
            )

    #ax.imshow(grid, cmap="Greys", origin="upper")

    # Draw grid lines
    if show_grid:
        ax.set_xticks(np.arange(-0.5, A, 1))
        ax.set_yticks(np.arange(-0.5, A, 1))
        ax.grid(color='black', linestyle='-', linewidth=1)

    # Hide tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Draw each path
    for path in paths:
        color = (random.random(), random.random(), random.random())

        xs = [coord[1] for coord in path]  # col
        ys = [coord[0] for coord in path]  # row

        ax.plot(xs, ys, marker='o', linewidth=2, color=color)

    ax.set_xlim(-0.5, A - 0.5)
    ax.set_ylim(A - 0.5, -0.5)

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    plt.show()

if __name__ == '__main__':
    paths = find_paths(6, (0,0), 1, 3,3, allow_crossing=False, min_straight_length=1)
    draw_paths(6, [paths[random.randint(0,len(paths)-1)]])
    print(paths)