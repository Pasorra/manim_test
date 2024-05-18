from manim import *


class PlayfairCipher(Scene):
    def construct(self):
        def find_letter(keysquare, letter):
            for i, l in enumerate(keysquare):
                if l == letter:
                    return i

        def dim(grid, exclude):
            things_to_dim = []
            for var in grid:
                if var[0].text not in exclude:
                    things_to_dim.append(var)
            return things_to_dim

        def index_to_grid_pos(i):
            row = i // 5
            column = i % 5
            return (row, column)

        def grid_pos_to_index(row, col):
            return row * 5 + col

        def animate_cipher_step(letters_to_find):
            global result_next_to
            letters_places = [
                find_letter(keysquare, letters_to_find[0]),
                find_letter(keysquare, letters_to_find[1]),
            ]
            surrounding_rect = SurroundingRectangle(
                VGroup(
                    grid[letters_places[0]],
                    grid[letters_places[1]],
                ),
                color=ManimColor("#4cc9f0"),
            )

            self.play(Create(surrounding_rect))
            things_to_dim = dim(grid, letters_to_find)
            self.play(
                LaggedStart(
                    *[
                        ApplyMethod(entry[0].set_opacity, 0.5)
                        for entry in things_to_dim
                    ],
                    lag_ratio=0.2,
                    run_time=0.5,
                )
            )

            row1, col1 = index_to_grid_pos(letters_places[0])
            row2, col2 = index_to_grid_pos(letters_places[1])

            if row1 == row2:
                col1 = (col1 + 1) % 5
                col2 = (col2 + 1) % 5
            elif col1 == col2:
                row1 = (row1 + 1) % 5
                row2 = (row2 + 1) % 5
            else:
                col1, col2 = col2, col1

            new_idx1 = grid_pos_to_index(row1, col1)
            new_idx2 = grid_pos_to_index(row2, col2)
            encrypted_letters = keysquare[new_idx1] + keysquare[new_idx2]
            print(encrypted_letters)

            self.play(Circumscribe(grid[new_idx1], color=ManimColor("#4cc9f0")))
            self.play(ApplyMethod(grid[new_idx1][0].set_opacity, 1))
            new_next_to = grid[new_idx1][0].copy()
            self.play(new_next_to.animate.next_to(result_next_to, RIGHT))
            result_next_to = new_next_to

            self.play(Circumscribe(grid[new_idx2], color=ManimColor("#4cc9f0")))
            self.play(ApplyMethod(grid[new_idx2][0].set_opacity, 1))
            new_next_to = grid[new_idx2][0].copy()
            self.play(new_next_to.animate.next_to(result_next_to, RIGHT))
            result_next_to = new_next_to

            self.play(
                LaggedStart(
                    *[ApplyMethod(entry[0].set_opacity, 1) for entry in things_to_dim],
                    lag_ratio=0.2,
                    run_time=0.5,
                )
            )
            self.play(FadeOut(surrounding_rect))

        self.camera.background_color = ManimColor("#432818")

        plain = "CODE"
        plain_text = Text(plain)
        keysquare = "PLAYFIR" + "".join(
            [chr(x) for x in range(65, 65 + 26) if chr(x) not in "PLAYFIRJ"]
        )
        grid = (
            VGroup(
                *[
                    VGroup(Text(x), Circle(color=ManimColor("#FFE6A7")))
                    for x in keysquare
                ]
            )
            .arrange_in_grid(5, 5)
            .scale(0.5)
        )
        plain_text.next_to(grid, LEFT)
        global result_next_to
        result_next_to = grid
        self.play(Create(plain_text))
        self.play(LaggedStart(*[Create(combo) for combo in grid]))

        animate_cipher_step("CO")
        animate_cipher_step("DE")
