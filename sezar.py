from manim import *


class Sezar(Scene):
    def construct(self):
        def shift_by_amount(letters_to_shift, amount: int, run_time=2) -> Mobject:
            buff = (letters_to_shift[1].get_left() - letters_to_shift[0].get_right())[0]
            self.play(
                letters_to_shift.animate.shift(
                    ((letters_to_shift[0].width + buff) * amount) * LEFT
                ),
                run_time=run_time,
            )
            return letters_to_shift

        def shift_group_by_amount(letters_to_shift, amount: int, run_time=2):
            self.play(
                *[
                    x.animate.shift(
                        (
                            (
                                (x[0].width + (x[1].get_left() - x[0].get_right())[0])
                                * amount
                            )
                            * LEFT
                        )
                    )
                    for x in letters_to_shift
                ],
                run_time=run_time
            )

        def move_along_axis(mobject, axis, new_value) -> Mobject:
            current_pos = mobject.get_center()
            if axis == "x":
                new_pos = np.array([new_value, current_pos[1], current_pos[2]])
            elif axis == "y":
                new_pos = np.array([current_pos[0], new_value, current_pos[2]])
            elif axis == "z":
                new_pos = np.array([current_pos[0], current_pos[1], new_value])
            else:
                raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

            mobject.move_to(new_pos)
            return mobject

        def find_letter(letters, letter):
            for group in letters:
                if group[0].text == letter:
                    return group[0]

        self.camera.background_color = ManimColor("#260701")

        plain_text = Text("M A T H")
        resulting_text = Text("P D W K")

        top_letters = VGroup()
        first = True
        top_arrow = ArrowTriangleTip(start_angle=-PI / 2, color=ManimColor("#D4A276"))
        bottom_arrow = ArrowTriangleTip(start_angle=PI / 2, color=ManimColor("#D4A276"))
        shift_amount = VGroup(Text("3"), Circle(color=ManimColor("#ADC178"))).scale(0.5)

        for letter_code in range(65, 65 + 26):
            letter = Text(chr(letter_code))
            square = Square()
            combo = VGroup(letter, square).scale(0.5)

            if first:
                combo.move_to(square.get_top() * 1.5)
                first = False
            else:
                combo.next_to(top_letters[-1], RIGHT, buff=0.2)

            top_letters.add(combo)

        bottom_letters = VGroup(*[x.copy() for x in top_letters])
        move_along_axis(top_letters, "y", top_letters.height * 0.5)
        move_along_axis(bottom_letters, "y", -bottom_letters.height * 0.5)

        move_along_axis(top_arrow, "y", top_letters.get_y() + top_letters.height)
        move_along_axis(
            bottom_arrow, "y", bottom_letters.get_y() - bottom_letters.height
        )

        plain_text.next_to(top_arrow, UP)
        resulting_text.next_to(bottom_arrow, DOWN)
        shift_amount.next_to(plain_text, UP)

        self.play(Create(plain_text))
        self.play(
            LaggedStart(
                LaggedStart(*[Create(combo) for combo in top_letters], lag_ratio=0.05),
                LaggedStart(
                    *[Create(combo) for combo in bottom_letters], lag_ratio=0.05
                ),
                lag_ratio=0.2,
            )
        )
        self.play(LaggedStart(Create(top_arrow), Create(bottom_arrow)))
        self.play(Create(shift_amount))

        shift_by_amount(bottom_letters, 3)

        shift_group_by_amount([top_letters, bottom_letters], ord("M") - ord("A"))
        self.play(
            (find_letter(bottom_letters, "P").copy().animate.move_to(resulting_text[0]))
        )

        shift_group_by_amount([top_letters, bottom_letters], ord("A") - ord("M"))
        self.play(
            (find_letter(bottom_letters, "D").copy().animate.move_to(resulting_text[1]))
        )

        shift_group_by_amount([top_letters, bottom_letters], ord("T") - ord("A"))
        self.play(
            (find_letter(bottom_letters, "W").copy().animate.move_to(resulting_text[2]))
        )

        shift_group_by_amount([top_letters, bottom_letters], ord("H") - ord("T"))
        self.play(
            (find_letter(bottom_letters, "K").copy().animate.move_to(resulting_text[3]))
        )

        self.wait(2)
