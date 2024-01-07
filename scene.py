from manim import *

SHORT = 0.25
MEDIUM = 0.5
LONG = 2


def colorIJK(ijk: MathTex, ijk_tex_strings: [str], ijk_colors: [color]) -> None:
    for v in zip(ijk_tex_strings, ijk_colors):
        ijk.set_color_by_tex(v[0], v[1])


class VektorelCarpim(Scene):
    def construct(self):
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
        UL
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
            self.play(Write(text), run_time=SHORT)

        entries_to_dim = VGroup()
        entries_to_highlight = VGroup()

        # Dim rows-cols
        for col in range(len(m1.get_mob_matrix())):
            for row in range(len(m1.get_mob_matrix()[col])):
                entry = m1.get_mob_matrix()[col][row]
                if col == 0 and row == 0:
                    continue
                if col == 0 or row == 0:
                    entries_to_dim.add(entry)
                else:
                    entries_to_highlight.add(entry)

        self.play(
            LaggedStart(
                *[ApplyMethod(entry.set_opacity, 0.5) for entry in entries_to_dim],
                lag_ratio=0.2,
                run_time=0.5
            )
        )

        # highlight bottom right of the matrix
        self.play(multEq.animate.to_corner(LEFT, buff=0.5))
        self.play(Circumscribe(entries_to_highlight), run_time=1.5)
        eq_sign = MathTex("=").next_to(m1)
        self.play(Write(eq_sign), run_time=SHORT)

        # i right multiplication
        start_x, start_y = (1, 1)
        i = m1.get_mob_matrix()[0][0].copy()
        up_left = m1.get_mob_matrix()[start_y][start_x].copy()
        up_right = m1.get_mob_matrix()[start_y][start_x + 1].copy()
        down_left = m1.get_mob_matrix()[start_y + 1][start_x].copy()
        down_right = m1.get_mob_matrix()[start_y + 1][start_x + 1].copy()
        i_mult = m1.get_mob_matrix()[0][0].copy().next_to(eq_sign)
        self.play(TransformMatchingShapes(i, i_mult), run_time=MEDIUM)
        ul_dr_mult = MathTex("(5 * 2 ").next_to(i_mult)
        ur_dl_mult = MathTex("- 3 * 1)").next_to(ul_dr_mult)
        self.play(
            TransformMatchingShapes(VGroup(up_left, down_right), ul_dr_mult),
            run_time=MEDIUM,
        )
        self.play(
            TransformMatchingShapes(VGroup(up_right, down_left), ur_dl_mult),
            run_time=MEDIUM,
        )
        i_val = MathTex("7").next_to(i_mult)
        self.play(Transform(VGroup(ul_dr_mult, ur_dl_mult), i_val, run_time=MEDIUM))

        # return back to color
        self.play(
            LaggedStart(
                *[ApplyMethod(entry.set_opacity, 1) for entry in entries_to_dim],
                lag_ratio=0.2,
                run_time=0.5
            )
        )

        self.wait(2)
