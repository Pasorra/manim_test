from manim import *

SHORT = 0.25
MEDIUM = 0.5
LONG = 2


def colorIJK(ijk: MathTex, ijk_tex_strings: [str], ijk_colors: [color]) -> None:
    for v in zip(ijk_tex_strings, ijk_colors):
        ijk.set_color_by_tex(v[0], v[1])


class VektorelCarpim(Scene):
    def construct(self):
        # helper functions
        def dim_rows_cols(
            entries_to_dim: VGroup, entries_to_highlight: VGroup, col_to_exclude: int
        ) -> None:
            for y in range(len(m1.get_mob_matrix())):
                for x in range(len(m1.get_mob_matrix()[y])):
                    entry = m1.get_mob_matrix()[y][x]
                    if x == col_to_exclude and y == 0:
                        continue
                    if x == col_to_exclude or y == 0:
                        entries_to_dim.add(entry)
                    else:
                        entries_to_highlight.add(entry)
            self.play(
                LaggedStart(
                    *[ApplyMethod(entry.set_opacity, 0.5) for entry in entries_to_dim],
                    lag_ratio=0.2,
                    run_time=0.5,
                )
            )

        def play_multiplications(
            letter: MathTex,
            letter_next_to: MathTex,
            up_left: MathTex,
            up_right: MathTex,
            down_left: MathTex,
            down_right: MathTex,
            sign: MathTex,
        ) -> MathTex:
            "returns the letter"
            ul_int = int(up_left.tex_string)
            ur_int = int(up_right.tex_string)
            dl_int = int(down_left.tex_string)
            dr_int = int(down_right.tex_string)
            sign_copy = sign.copy().next_to(letter_next_to)
            self.play(TransformMatchingShapes(sign, sign_copy), run_time=MEDIUM)
            letter_mult = letter.copy().next_to(sign_copy)
            self.play(TransformMatchingShapes(letter, letter_mult), run_time=MEDIUM)
            ul_dr_mult = MathTex(f"({ul_int} * {dr_int} ").next_to(letter_mult)
            ur_dl_mult = MathTex(f"- {ur_int} * {dl_int})").next_to(ul_dr_mult)
            self.play(
                TransformMatchingShapes(VGroup(up_left, down_right), ul_dr_mult),
                run_time=MEDIUM,
            )
            self.play(
                TransformMatchingShapes(VGroup(up_right, down_left), ur_dl_mult),
                run_time=MEDIUM,
            )
            letter_val = MathTex(f"{ul_int*dr_int - ur_int * dl_int}").next_to(
                letter_mult
            )
            self.play(
                Transform(
                    VGroup(ul_dr_mult, ur_dl_mult),
                    letter_val,
                    run_time=MEDIUM,
                    replace_mobject_with_target_in_scene=True,
                )
            )
            self.play(Swap(letter_mult, letter_val), run_time=SHORT)
            return letter_mult

        # global variables
        isolated_subs = [r"\hat{\textbf{\i}}", r"\hat{\textbf{\j}}", r"\hat{k}"]
        ijk_colors = [RED, GREEN, BLUE]

        # initializing equations
        vecA = MathTex(r"\vec{A}=")
        vecB = MathTex(r"\vec{B}=")
        eqA = MathTex(
            r"4\hat{\textbf{\i}}+5\hat{\textbf{\j}}+3\hat{k}",
            substrings_to_isolate=isolated_subs,
        )
        eqB = MathTex(
            r"2\hat{\textbf{\i}}+\hat{\textbf{\j}}+2\hat{k}",
            substrings_to_isolate=isolated_subs,
        )
        g = VGroup(vecA, eqA, vecB, eqB).arrange_in_grid(cols=2, rows=2)

        for eq in range(1, len(g), 2):
            colorIJK(g[eq], g[eq].tex_strings[1::2], ijk_colors)
        self.play(
            LaggedStart(
                Create(g[:2]),
                Create(g[2:]),
                lag_ratio=0.4,
            ),
            run_time=MEDIUM,
        )

        # removing A = and B =
        self.play(ShrinkToCenter(vecA), ShrinkToCenter(vecB))
        self.play(g.remove(vecA, vecB).animate.center())

        # Separating out IJK
        ijk = MathTex(
            r"".join(isolated_subs),
            substrings_to_isolate=isolated_subs,
        )
        colorIJK(ijk, ijk.tex_strings, ijk_colors)
        newEqA = MathTex(r"4+5+3")
        newEqB = MathTex(r"2+1+2")
        newG = VGroup(ijk, newEqA, newEqB).arrange_in_grid(cols=1)
        self.play(
            TransformMatchingShapes(eqA.copy(), ijk),
            TransformMatchingShapes(eqA, newEqA),
            TransformMatchingShapes(eqB, newEqB),
        )

        # Create matrix
        m0 = Matrix(
            [ijk.tex_strings, [4, 5, 3], [2, 1, 2]],
            left_bracket="|",
            right_bracket="|",
        )
        for i in range(3):
            m0[0][i].color = ijk_colors[i]
        self.play(TransformMatchingShapes(newG, m0), run_time=2)

        # Write out AxB next to matrix
        axb = MathTex(r"A{\times}B=")
        m1 = m0.copy()
        multEq = VGroup(axb, m1).arrange()
        self.play(TransformMatchingShapes(m0, m1))
        self.wait()
        self.play(Write(axb))

        # Write signs above matrix columns
        signs = VGroup()
        for col_index in range(len(m1.get_columns()[0])):
            text = MathTex("+" if col_index % 2 == 0 else "-").set_color(
                GREEN if col_index % 2 == 0 else RED
            )
            text.add_updater(
                lambda x, col_index=col_index: x.next_to(
                    [m1.get_columns()[col_index].get_x(), m1.get_rows()[0].get_y(), 0],
                    UP * (1.4 if col_index % 2 == 0 else 2),
                )
            )
            signs.add(text)
            self.play(Write(text), run_time=SHORT)

        # Dim rows-cols
        entries_to_dim = VGroup()
        entries_to_highlight = VGroup()
        dim_rows_cols(entries_to_dim, entries_to_highlight, 0)

        # highlight bottom right of the matrix
        self.play(multEq.animate.to_corner(LEFT, buff=0.5))
        self.play(Circumscribe(entries_to_highlight), run_time=1.5)

        eq_sign = MathTex("=").next_to(m1)
        self.play(Write(eq_sign), run_time=SHORT)

        # i multiplication
        i = m1.get_mob_matrix()[0][0].copy()
        up_left = m1.get_mob_matrix()[1][1].copy()
        up_right = m1.get_mob_matrix()[1][2].copy()
        down_left = m1.get_mob_matrix()[2][1].copy()
        down_right = m1.get_mob_matrix()[2][2].copy()
        sign = signs[0].copy()
        sign.clear_updaters()

        i = play_multiplications(
            i, eq_sign, up_left, up_right, down_left, down_right, sign
        )

        # return back to color
        self.play(
            LaggedStart(
                *[ApplyMethod(entry.set_opacity, 1) for entry in entries_to_dim],
                lag_ratio=0.2,
                run_time=0.5,
            )
        )

        # Dim rows-cols
        entries_to_dim = VGroup()
        entries_to_highlight = VGroup()
        dim_rows_cols(entries_to_dim, entries_to_highlight, 1)

        # j multiplication
        j = m1.get_mob_matrix()[0][1].copy()
        up_left = m1.get_mob_matrix()[1][0].copy()
        up_right = m1.get_mob_matrix()[1][2].copy()
        down_left = m1.get_mob_matrix()[2][0].copy()
        down_right = m1.get_mob_matrix()[2][2].copy()
        sign = signs[1].copy()
        sign.clear_updaters()

        j = play_multiplications(j, i, up_left, up_right, down_left, down_right, sign)

        # return back to color
        self.play(
            LaggedStart(
                *[ApplyMethod(entry.set_opacity, 1) for entry in entries_to_dim],
                lag_ratio=0.2,
                run_time=0.5,
            )
        )

        # Dim rows-cols
        entries_to_dim = VGroup()
        entries_to_highlight = VGroup()
        dim_rows_cols(entries_to_dim, entries_to_highlight, 2)

        # k multiplication
        k = m1.get_mob_matrix()[0][2].copy()
        up_left = m1.get_mob_matrix()[1][0].copy()
        up_right = m1.get_mob_matrix()[1][1].copy()
        down_left = m1.get_mob_matrix()[2][0].copy()
        down_right = m1.get_mob_matrix()[2][1].copy()
        sign = signs[2].copy()
        sign.clear_updaters()

        k = play_multiplications(k, j, up_left, up_right, down_left, down_right, sign)

        # return back to color
        self.play(
            LaggedStart(
                *[ApplyMethod(entry.set_opacity, 1) for entry in entries_to_dim],
                lag_ratio=0.2,
                run_time=0.5,
            )
        )

        self.wait(2)
