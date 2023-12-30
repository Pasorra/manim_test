from manim import *


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

        self.play(
            LaggedStart(
                Create(g[:2]),
                Create(g[2:]),
                lag_ratio=0.4,
            ),
            run_time=3,
        )

        # removing A = and B =
        self.play(ShrinkToCenter(vecA), ShrinkToCenter(vecB))
        self.play(g.remove(vecA, vecB).animate.center(), run_time=2)

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
            run_time=2,
        )

        # Create matrix
        m0 = Matrix(
            [ijk.tex_strings, [4, 5, 3], [2, 1, 2]],
            left_bracket="|",
            right_bracket="|",
        )
        for i in range(3):
            m0[0][i].color = ijk_colors[i]
        self.play(TransformMatchingShapes(newG, m0), run_time=3)

        # Write out AxB next to matrix
        axb = MathTex(r"A{\times}B=")
        m1 = m0.copy()
        multEq = VGroup(axb, m1).arrange()
        self.play(TransformMatchingShapes(m0, m1))
        self.wait()
        self.play(Write(axb), run_time=2)
        self.play(multEq.animate.to_corner(LEFT, buff=0.5), run_time=2)

        # Write signs above matrix columns
        text_objects = []
        for col_index in range(len(m1.get_columns()[0])):
            text = MathTex("+" if col_index % 2 == 0 else "-").set_color(
                GREEN if col_index % 2 == 0 else RED
            )
            text_objects.append((text, col_index))
        for text, col_index in text_objects:
            text.add_updater(
                lambda x, col_index=col_index: x.next_to(
                    [m1.get_columns()[col_index].get_x(), m1.get_rows()[0].get_y(), 0],
                    UP * (1.4 if col_index % 2 == 0 else 2),
                )
            )
            self.play(Write(text))

        # Select and highlight rows-cols
        for col in range(len(m1.get_mob_matrix())):
            for row in range(len(m1.get_mob_matrix()[col])):
                if col == 0 or row == 0:
                    entry = m1.get_mob_matrix()[col][row]
                    self.play(entry.animate.set_opacity(0.2), run_time=0.1)

        self.wait(2)
