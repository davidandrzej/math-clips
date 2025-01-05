from manim import *

class RepeatedNGon(Scene):
    def construct(self):
        # ------------------------------
        # Coordinate Plane
        # ------------------------------

        for N in range(3, 9):
            self.clear()
            plane = NumberPlane(
                x_range=[-3, 3, 1],
                y_range=[-3, 3, 1],
                background_line_style={
                    "stroke_color": BLUE_E,
                    "stroke_width": 1,
                    "stroke_opacity": 0.4
                },
            )        
            self.play(FadeIn(plane))
            unit_circle = Circle(radius=1, color=WHITE)
            self.play(Create(unit_circle))
            self.wait()
            self.ngonAnimation(N)


                

                
    def ngonAnimation(self, N):
        # ------------------------------
        # 1) Parameters
        # ------------------------------
        angle_step = 2 * PI / N

        # ------------------------------
        # 2) Summation Equation & N=...
        # ------------------------------
        # Summation expression in terms of N
        # Placed in the top-right corner
        sum_expr = MathTex(
            r"\sum_{k=0}^{N-1} e^{2 \pi i \frac{k}{N}} = 0"
        ).to_corner(UP + RIGHT)

        # Label for N (e.g., "N = 8"), placed below the summation
        N_label = Tex(rf"N = {N}").next_to(sum_expr, DOWN, buff=0.3).align_to(sum_expr, RIGHT)

        # Show them on screen
        self.play(FadeIn(sum_expr), FadeIn(N_label))
        self.wait(1)

        # ------------------------------
        # 4) Unit Circle & Initial Vector
        # ------------------------------
        vector = Arrow(start=ORIGIN, end=RIGHT, buff=0, color=YELLOW)

        self.play(Create(vector))
        self.wait()

        # Keep track of endpoints for the inscribed N-gon
        previous_endpoint = vector.get_end()
        # Keep track of partial sums for the tip-to-tail path
        partial_position = ORIGIN

        # ------------------------------
        # 5) Bottom "k = ..." Label
        # ------------------------------
        # We'll transform this label from k=0 to k=1 to k=2, etc., instead of overwriting.
        current_k_label = Tex(r"k = 0").set_color(BLUE).to_edge(DOWN)
        self.play(FadeIn(current_k_label))

        # Draw initial dotted line
        # d) Tip-to-Tail partial sum (dotted blue line)
        dotted_line = DashedLine(
            start=ORIGIN,
            end=previous_endpoint,
            color=BLUE,
            dash_length=0.05
        )
        partial_position = previous_endpoint
        self.play(Create(dotted_line), run_time=0.5)

        # ------------------------------
        # 6) Animate Rotations & Summation Steps
        # ------------------------------
        for k in range(1,N):

            # b) Rotate the vector by angle_step
            self.play(Rotate(vector, angle=angle_step, about_point=ORIGIN), run_time=1)

            # Transform the old label into the new one
            new_k_label = Tex(rf"k = {k}").set_color(BLUE).to_edge(DOWN)
            self.play(ReplacementTransform(current_k_label, new_k_label))
            current_k_label = new_k_label

            # c) Draw the red line for the inscribed side
            new_endpoint = vector.get_end()
            edge_line = Line(previous_endpoint, new_endpoint, color=RED)
            self.play(Create(edge_line), run_time=0.3)
            previous_endpoint = new_endpoint

            # d) Tip-to-Tail partial sum (dotted blue line)
            current_vector = new_endpoint - ORIGIN
            next_partial_position = partial_position + current_vector
            dotted_line = DashedLine(
                start=partial_position,
                end=next_partial_position,
                color=BLUE,
                dash_length=0.05
            )
            self.play(Create(dotted_line), run_time=0.5)
            partial_position = next_partial_position

            self.wait(0.3)

        # ------------------------------
        # 7) Close the N-gon
        # ------------------------------
        first_endpoint = RIGHT  # (1,0)
        closing_line = Line(previous_endpoint, first_endpoint, color=RED)
        self.play(Create(closing_line), run_time=0.5)

        # Optionally fade out the final "k=..." label
        if current_k_label is not None:
            self.play(FadeOut(current_k_label))

        # ------------------------------
        # 8) Final partial sum at origin
        # ------------------------------
        # Because these vectors sum to zero (floating-point aside).
        if np.allclose(partial_position, ORIGIN, atol=1e-6):
            dot_at_origin = Dot(ORIGIN, color=YELLOW)
            self.play(FadeIn(dot_at_origin, scale=2))
        else:
            # Show discrepancy if there's floating-point offset
            final_line = DashedLine(partial_position, ORIGIN, color=BLUE, dash_length=0.05)
            self.play(Create(final_line), run_time=0.5)

        self.wait(2)


class Target(Scene):
    def __init__(self, N, **kwargs):
        super().__init__(**kwargs)
        self.N = N
    
    def construct(self):
        do_target_animation(self, self.N)


class InscribedNGonWithSummation(Scene):
    def construct(self):
        # ------------------------------
        # 1) Parameters
        # ------------------------------
        N = 8
        angle_step = 2 * PI / N

        # ------------------------------
        # 2) Summation Equation & N=...
        # ------------------------------
        # Summation expression in terms of N
        # Placed in the top-right corner
        sum_expr = MathTex(
            r"\sum_{k=0}^{N-1} e^{2 \pi i \frac{k}{N}} = 0"
        ).to_corner(UP + RIGHT)

        # Label for N (e.g., "N = 8"), placed below the summation
        N_label = Tex(rf"N = {N}").next_to(sum_expr, DOWN, buff=0.3).align_to(sum_expr, RIGHT)

        # Show them on screen
        self.play(FadeIn(sum_expr), FadeIn(N_label))
        self.wait(1)

        # ------------------------------
        # 3) Coordinate Plane (Optional)
        # ------------------------------
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
        )
        self.play(FadeIn(plane))

        # ------------------------------
        # 4) Unit Circle & Initial Vector
        # ------------------------------
        unit_circle = Circle(radius=1, color=WHITE)
        vector = Arrow(start=ORIGIN, end=RIGHT, buff=0, color=YELLOW)

        self.play(Create(unit_circle), Create(vector))
        self.wait()

        # Keep track of endpoints for the inscribed N-gon
        previous_endpoint = vector.get_end()
        # Keep track of partial sums for the tip-to-tail path
        partial_position = ORIGIN

        # ------------------------------
        # 5) Bottom "k = ..." Label
        # ------------------------------
        # We'll transform this label from k=0 to k=1 to k=2, etc., instead of overwriting.
        current_k_label = Tex(r"k = 0").set_color(BLUE).to_edge(DOWN)
        self.play(FadeIn(current_k_label))

        # Draw initial dotted line
        # d) Tip-to-Tail partial sum (dotted blue line)
        dotted_line = DashedLine(
            start=ORIGIN,
            end=previous_endpoint,
            color=BLUE,
            dash_length=0.05
        )
        partial_position = previous_endpoint
        self.play(Create(dotted_line), run_time=0.5)

        # ------------------------------
        # 6) Animate Rotations & Summation Steps
        # ------------------------------
        for k in range(1,N):

            # b) Rotate the vector by angle_step
            self.play(Rotate(vector, angle=angle_step, about_point=ORIGIN), run_time=1)

            # Transform the old label into the new one
            new_k_label = Tex(rf"k = {k}").set_color(BLUE).to_edge(DOWN)
            self.play(ReplacementTransform(current_k_label, new_k_label))
            current_k_label = new_k_label

            # c) Draw the red line for the inscribed side
            new_endpoint = vector.get_end()
            edge_line = Line(previous_endpoint, new_endpoint, color=RED)
            self.play(Create(edge_line), run_time=0.3)
            previous_endpoint = new_endpoint

            # d) Tip-to-Tail partial sum (dotted blue line)
            current_vector = new_endpoint - ORIGIN
            next_partial_position = partial_position + current_vector
            dotted_line = DashedLine(
                start=partial_position,
                end=next_partial_position,
                color=BLUE,
                dash_length=0.05
            )
            self.play(Create(dotted_line), run_time=0.5)
            partial_position = next_partial_position

            self.wait(0.3)

        # ------------------------------
        # 7) Close the N-gon
        # ------------------------------
        first_endpoint = RIGHT  # (1,0)
        closing_line = Line(previous_endpoint, first_endpoint, color=RED)
        self.play(Create(closing_line), run_time=0.5)

        # Optionally fade out the final "k=..." label
        if current_k_label is not None:
            self.play(FadeOut(current_k_label))

        # ------------------------------
        # 8) Final partial sum at origin
        # ------------------------------
        # Because these vectors sum to zero (floating-point aside).
        if np.allclose(partial_position, ORIGIN, atol=1e-6):
            dot_at_origin = Dot(ORIGIN, color=YELLOW)
            self.play(FadeIn(dot_at_origin, scale=2))
        else:
            # Show discrepancy if there's floating-point offset
            final_line = DashedLine(partial_position, ORIGIN, color=BLUE, dash_length=0.05)
            self.play(Create(final_line), run_time=0.5)

        self.wait(2)
