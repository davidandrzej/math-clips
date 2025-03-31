from manim import *
import numpy as np

# Cross-fade the 4 sub-scenes together via, eg: 
#
# ffmpeg -i MatrixTScene.mp4 -i MatrixSScene.mp4 -i CompositionSetupScene.mp4 -i MatrixMultiplicationScene.mp4 \
# -filter_complex "\
# [0:v]format=yuv420p, setpts=PTS-STARTPTS[v0]; \
# [1:v]format=yuv420p, setpts=PTS-STARTPTS[v1]; \
# [2:v]format=yuv420p, setpts=PTS-STARTPTS[v2]; \
# [3:v]format=yuv420p, setpts=PTS-STARTPTS[v3]; \
# [v0][v1]xfade=transition=fade:duration=1:offset=18[v01]; \
# [v01][v2]xfade=transition=fade:duration=1:offset=46[v012]; \
# [v012][v3]xfade=transition=fade:duration=1:offset=59[v]" \
# -map "[v]" -c:v libx264 -profile:v baseline -pix_fmt yuv420p -movflags +faststart -c:a aac output.mp4


# Set the frame dimensions (works for Manim Community v0.16+)
config.frame_width = 16
config.frame_height = 9


class MatrixMultiplicationScene(Scene):
    def construct(self):
        # Create matrices A, B, and AB, and display them at the top.
        matrix_A = Matrix([[4, 1, 8],
                           [5, 6, 0]])
        matrix_B = Matrix([[3],
                           [7],
                           [2]])
        matrix_AB = Matrix([["0"],
                            ["0"]])
        times_sign = Tex("$\\times$")
        equals_sign = Tex("$=$")
        matrices = VGroup(matrix_A, times_sign, matrix_B, equals_sign, matrix_AB).arrange(RIGHT, buff=1)
        matrices.to_edge(UP)
        self.play(Write(matrices))
        self.wait(0.5)

        # Helper function: compute a label position offset perpendicular to an arrow.
        def offset_label_position(arrow, offset=0.3):
            direction = arrow.get_end() - arrow.get_start()
            # Rotate by 90° to get a perpendicular offset.
            rotated = np.array([-direction[1], direction[0], 0])
            norm = np.linalg.norm(rotated)
            normal = rotated / norm if norm != 0 else rotated
            return arrow.get_midpoint() + normal * offset

        # Define a downward shift for the graph.
        graph_shift = DOWN * 1.6

        # --- Define positions for the graph nodes (shifted downward) ---
        u_pos = LEFT * 5 + graph_shift
        v_positions = [np.array([0, 2, 0]) + graph_shift,
                       np.array([0, 0, 0]) + graph_shift,
                       np.array([0, -2, 0]) + graph_shift]
        sv_positions = [np.array([2, 2, 0]) + graph_shift,
                        np.array([2, 0, 0]) + graph_shift,
                        np.array([2, -2, 0]) + graph_shift]
        w_positions = [np.array([5, 1, 0]) + graph_shift,
                       np.array([5, -1, 0]) + graph_shift]

        # --- Create nodes for the graph ---
        # u node (domain of T)
        u_dot = Dot(point=u_pos, color=BLUE)
        u_label = Tex("$u_1$").next_to(u_dot, DOWN)
        # Add the input basis vector for U.
        u_basis = MathTex(r"[1]").next_to(u_dot, LEFT, buff=0.5)
        u_group = VGroup(u_dot, u_label, u_basis)
        self.play(FadeIn(u_group))
        self.wait(0.5)

        # v nodes
        v_dots = VGroup(*[Dot(point=pos, color=GREEN) for pos in v_positions])
        v_labels = VGroup(*[
            Tex(f"$v_{{{i+1}}}$").next_to(v_dots[i], UP)
            for i in range(len(v_positions))
        ])
        self.play(FadeIn(v_dots), *[FadeIn(label) for label in v_labels])
        self.wait(0.5)

        # S(v) nodes (showing the intermediate step S(v))
        sv_dots = VGroup(*[Dot(point=pos, color=ORANGE) for pos in sv_positions])
        sv_labels = VGroup(*[
            Tex(f"$S(v_{{{i+1}}})$").next_to(sv_dots[i], UP)
            for i in range(len(sv_positions))
        ])
        self.play(FadeIn(sv_dots), *[FadeIn(label) for label in sv_labels])
        self.wait(0.5)

        # w nodes (codomain of S)
        w_dots = VGroup(*[Dot(point=pos, color=RED) for pos in w_positions])
        w_labels = VGroup(*[
            Tex(f"$w_{{{i+1}}}$").next_to(w_dots[i], UP)
            for i in range(len(w_positions))
        ])
        self.play(FadeIn(w_dots), *[FadeIn(label) for label in w_labels])
        self.wait(0.5)
        # Add basis vectors for W.
        w_basis = VGroup(
            MathTex(r"\begin{pmatrix}1\\0\end{pmatrix}").next_to(w_dots[0], RIGHT, buff=0.5),
            MathTex(r"\begin{pmatrix}0\\1\end{pmatrix}").next_to(w_dots[1], RIGHT, buff=0.5)
        )
        self.play(FadeIn(w_basis))
        self.wait(0.5)

        # --- Draw arrows from u -> v with weights B ---
        # B = [[3], [7], [2]]
        B_values = [3, 7, 2]
        arrows_u_v = VGroup()
        labels_u_v = VGroup()
        for i, v in enumerate(v_dots):
            arrow = Arrow(u_dot.get_center(), v.get_center(), buff=0.1)
            arrows_u_v.add(arrow)
            label_pos = offset_label_position(arrow, offset=0.3)
            weight_label = Tex(f"$ {B_values[i]}$").scale(0.7).move_to(label_pos)
            labels_u_v.add(weight_label)
        self.play(*[Create(arrow) for arrow in arrows_u_v],
                  *[FadeIn(label) for label in labels_u_v])
        self.wait(0.5)

        # --- Draw short arrows from v -> S(v) ---
        arrows_v_sv = VGroup()
        for i in range(len(v_dots)):
            arrow = Arrow(v_dots[i].get_center(), sv_dots[i].get_center(), buff=0.1, stroke_width=2)
            arrows_v_sv.add(arrow)
        self.play(*[Create(arrow) for arrow in arrows_v_sv])
        self.wait(0.5)

        # --- Draw arrows from S(v) -> w with weights A ---
        # A = [[4, 1, 8],
        #      [5, 6, 0]]
        A_values = [[4, 1, 8],
                    [5, 6, 0]]
        arrows_sv_w = VGroup()
        labels_sv_w = VGroup()
        for i, sv in enumerate(sv_dots):
            for j, w in enumerate(w_dots):
                arrow = Arrow(sv.get_center(), w.get_center(), buff=0.1, stroke_width=2)
                arrows_sv_w.add(arrow)
                label_pos = offset_label_position(arrow, offset=0.3)
                weight = A_values[j][i]  # row j, column i
                label = Tex(f"$ {weight}$").scale(0.7).move_to(label_pos)
                labels_sv_w.add(label)
        self.play(*[Create(arrow) for arrow in arrows_sv_w],
                  *[FadeIn(label) for label in labels_sv_w])
        self.wait(0.5)

        # --- Animate the computation of M(ST) and update the AB matrix ---
        for j, w in enumerate(w_dots):
            total = 0
            for i in range(3):
                product = A_values[j][i] * B_values[i]
                # Group the arrows along the path from u -> v, v -> S(v), and S(v) -> w.
                path_arrows = VGroup(arrows_u_v[i], arrows_v_sv[i])
                index = i * len(w_dots) + j  # corresponding arrow in arrows_sv_w
                path_arrows.add(arrows_sv_w[index])
                self.play(Indicate(path_arrows, color=YELLOW, scale_factor=1.2))
                self.wait(0.5)

                # Highlight corresponding A and B entries in the matrices.
                a_entry = matrix_A.get_entries()[j * 3 + i]
                b_entry = matrix_B.get_entries()[i]
                self.play(Indicate(a_entry, color=YELLOW),
                          Indicate(b_entry, color=YELLOW))
                self.wait(0.5)

                # Show the multiplication term on the left (near u node).
                term = Tex(f"$ {A_values[j][i]}\\times {B_values[i]} = {product}$").scale(0.7)
                term.next_to(u_dot, LEFT, buff=1.0)
                self.play(Write(term))
                self.wait(0.5)

                total += product
                ab_entry = matrix_AB.get_entries()[j]
                new_val = Tex(f"$ {total}$").scale(0.8).move_to(ab_entry.get_center())
                self.play(Transform(ab_entry, new_val))
                self.wait(0.5)
                self.play(FadeOut(term))
            self.wait(1)
        self.wait(2)

        
class MatrixTScene(Scene):
    def construct(self):
        # Title at the top
        title = MathTex(r"How\ M(T)\ maps\ u_1\ to\ 3v_1+7v_2+2v_3").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Show that M(T) = [3, 7, 2] below the title.
        mt_text = MathTex(r"M(T)= [3,\;7,\;2]").next_to(title, DOWN)
        self.play(Write(mt_text))
        self.wait(0.5)
        
        # Create u1 as a blue dot on the left with a label and its coordinate [1].
        u_dot = Dot(point=LEFT * 6, color=BLUE)
        u_label = MathTex(r"u_1").next_to(u_dot, DOWN)
        u_vector = MathTex(r"[1]").next_to(u_dot, LEFT)
        u_group = VGroup(u_dot, u_label, u_vector)
        self.play(FadeIn(u_group))
        self.wait(0.5)
        
        # Create three green dots for v1, v2, v3 on the right.
        v_positions = [RIGHT * 6 + UP * 2, RIGHT * 6, RIGHT * 6 + DOWN * 2]
        v_dots = VGroup(*[Dot(point=pos, color=GREEN) for pos in v_positions])
        v_labels = VGroup(*[MathTex(f"v_{{{i+1}}}").next_to(v_dots[i], UP) for i in range(3)])
        self.play(FadeIn(v_dots), FadeIn(v_labels))
        self.wait(0.5)
        
        # For each v node, add a standard basis label to the right.
        v_std_labels = VGroup(
            MathTex(r"\begin{pmatrix}1\\0\\0\end{pmatrix}").next_to(v_dots[0], RIGHT, buff=0.5),
            MathTex(r"\begin{pmatrix}0\\1\\0\end{pmatrix}").next_to(v_dots[1], RIGHT, buff=0.5),
            MathTex(r"\begin{pmatrix}0\\0\\1\end{pmatrix}").next_to(v_dots[2], RIGHT, buff=0.5)
        )
        self.play(FadeIn(v_std_labels))
        self.wait(0.5)
        
        # Draw arrows from u1 to each v_i with weight labels.
        weights = [3, 7, 2]
        arrows = VGroup()
        weight_labels = VGroup()
        for i, v in enumerate(v_dots):
            arrow = Arrow(u_dot.get_center(), v.get_center(), buff=0.1)
            arrows.add(arrow)
            # Place the weight label near the middle of the arrow.
            label = MathTex(str(weights[i])).scale(0.7).move_to(arrow.get_midpoint() + UP * 0.3)
            weight_labels.add(label)
        self.play(
            *[Create(arrow) for arrow in arrows],
            *[FadeIn(label) for label in weight_labels]
        )
        self.wait(0.5)
        
        # Display the mapping expression at the bottom.
        mapping_expr = MathTex(r"T(u_1)=3v_1+7v_2+2v_3").to_edge(DOWN)
        self.play(Write(mapping_expr))
        self.wait(1)
        
        # Sequentially highlight each arrow in yellow.
        for arrow in arrows:
            self.play(Indicate(arrow, color=YELLOW, scale_factor=1.2))
            self.wait(0.5)
        
        self.wait(2)

        
class MatrixSScene(Scene):
    def construct(self):
        # Title and M(S) label at the top.
        title = MathTex(r"How\ S\ maps\ v_i\ to\ a\ linear\ combination\ of\ w_j").to_edge(UP)
        self.play(Write(title))
        ms_label = MathTex(r"M(S)=\begin{pmatrix}4 & 1 & 8\\5 & 6 & 0\end{pmatrix}").next_to(title, DOWN)
        self.play(Write(ms_label))
        self.wait(0.5)

        # Create three v nodes (domain) on the left.
        v_positions = [LEFT * 6 + UP * 2, LEFT * 6, LEFT * 6 + DOWN * 2]
        v_dots = VGroup(*[Dot(point=pos, color=GREEN) for pos in v_positions])
        self.play(FadeIn(v_dots))
        self.wait(0.5)
        
        # Create v labels (e.g., "v₁", "v₂", "v₃")
        v_labels = VGroup(*[MathTex(f"v_{{{i+1}}}") for i in range(3)])
        for i in range(3):
            # Place these to the RIGHT of the v dots.
            v_labels[i].next_to(v_dots[i], RIGHT, buff=0.5)
        self.play(FadeIn(v_labels))
        self.wait(0.5)
        
        # Add input basis vector labels for each v node (placed further to the LEFT of the v labels).
        v_input_labels = VGroup(
            MathTex(r"\begin{pmatrix}1\\0\\0\end{pmatrix}"),
            MathTex(r"\begin{pmatrix}0\\1\\0\end{pmatrix}"),
            MathTex(r"\begin{pmatrix}0\\0\\1\end{pmatrix}")
        )
        for i in range(3):
            v_input_labels[i].next_to(v_labels[i], LEFT, buff=0.8)
        self.play(FadeIn(v_input_labels))
        self.wait(0.5)
        
        # Create two w nodes (codomain) on the right.
        w_positions = [RIGHT * 6 + UP, RIGHT * 6 + DOWN]
        w_dots = VGroup(*[Dot(point=pos, color=RED) for pos in w_positions])
        self.play(FadeIn(w_dots))
        self.wait(0.5)
        
        # Create w labels placed to the right of the w nodes.
        w_labels = VGroup(*[MathTex(f"w_{{{i+1}}}") for i in range(2)])
        for i in range(2):
            w_labels[i].next_to(w_dots[i], RIGHT, buff=0.3)
        self.play(FadeIn(w_labels))
        self.wait(0.5)
        
        # Add standard basis labels for w nodes (pushed further right so they don't overlap with the w labels).
        w_std_labels = VGroup(
            MathTex(r"\begin{pmatrix}1\\0\end{pmatrix}"),
            MathTex(r"\begin{pmatrix}0\\1\end{pmatrix}")
        )
        for i in range(2):
            w_std_labels[i].next_to(w_dots[i], RIGHT, buff=1.0)
        self.play(FadeIn(w_std_labels))
        self.wait(0.5)
        
        # Draw arrows from each v node to each w node with weight labels.
        # The mapping is: S(v₁)=4w₁+5w₂, S(v₂)=1w₁+6w₂, S(v₃)=8w₁+0w₂.
        weights = [[4, 5], [1, 6], [8, 0]]
        arrows = VGroup()
        weight_labels = VGroup()
        for i, v in enumerate(v_dots):
            for j, w in enumerate(w_dots):
                arrow = Arrow(v.get_center(), w.get_center(), buff=0.1)
                arrows.add(arrow)
                # Place the weight label at 1/4 along the arrow.
                label = MathTex(str(weights[i][j])).scale(0.7)
                # Alternate vertical offset: for j even, offset upward; for j odd, downward.
                offset = UP * 0.3 if j % 2 == 0 else DOWN * 0.3
                label.move_to(arrow.point_from_proportion(0.25) + offset)
                weight_labels.add(label)
        self.play(Create(arrows), FadeIn(weight_labels))
        self.wait(0.5)
        
        # For each v node, animate its mapping by writing a mapping expression at the bottom.
        for i in range(3):
            mapping_expr = MathTex(
                f"S(v_{{{i+1}}})=", f"{weights[i][0]}w_1", "+", f"{weights[i][1]}w_2"
            ).to_edge(DOWN)
            self.play(Write(mapping_expr))
            self.wait(0.5)
            # Highlight the two arrows corresponding to this v₍ᵢ₊₁₎.
            arrow1 = arrows[2 * i]
            arrow2 = arrows[2 * i + 1]
            self.play(Indicate(arrow1, color=YELLOW, scale_factor=1.2),
                      Indicate(arrow2, color=YELLOW, scale_factor=1.2))
            self.wait(1)
            self.play(FadeOut(mapping_expr))
        self.wait(2)


class CompositionSetupScene(Scene):
    def construct(self):
        # Title at the top.
        title = MathTex(r"\textbf{Composition of Linear Maps}").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Define the maps.
        maps = VGroup(
            MathTex(r"T: U \to V"),
            MathTex(r"S: V \to W"),
            MathTex(r"\Rightarrow S \circ T: U \to W")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(title, DOWN, buff=1)
        self.play(Write(maps))
        self.wait(1)
        
        # Matrix representations.
        matrices = VGroup(
            MathTex(r"M(T)=B"),
            MathTex(r"M(S)=A")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(maps, DOWN, buff=1)
        self.play(Write(matrices))
        self.wait(1)
        
        # Composition expressed in matrices.
        comp_eq = MathTex(r"M(S\circ T)=M(S)M(T)").next_to(matrices, DOWN, buff=1)
        self.play(Write(comp_eq))
        self.wait(1)
        
        # Derivation: how matrix multiplication encodes the composition.
        derivation = VGroup(
            MathTex(r"T(u_k)=\sum_{r=1}^n B_{r,k}\,v_r"),
            MathTex(r"S(v_r)=\sum_{j=1}^m A_{j,r}\,w_j"),
            MathTex(r"\implies S(T(u_k))=\sum_{r=1}^n A_{j,r}B_{r,k}\,w_j"),
            MathTex(r"\text{Thus, }(M(S\circ T))_{j,k}=\sum_{r=1}^n A_{j,r}B_{r,k}")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).scale(0.8).next_to(comp_eq, DOWN, buff=1)
        self.play(Write(derivation))
        self.wait(2)
