from manim import *
import math
import numpy as np

class CosetsAndWaveInZ12(Scene):
    def construct(self):
        ##################################################
        # 1) Basic Setup & Function Definitions
        ##################################################
        n = 12                            # |Z_12|=12
        spacing = 1.0                     # horizontal spacing
        dot_radius = 0.1                  # size of points
        coset_colors = [RED, GREEN, BLUE, ORANGE]
        
        # Subgroup H = <4> = {0,4,8}
        H = {0, 4, 8}
        
        # We'll shift everything (wave & line) by Y_SHIFT downward
        # so there's extra space at the top for the combined label.
        Y_SHIFT = -0.7

        # Sine-wave-like function with period 4:
        #   wave_offset is the base vertical shift for the wave
        #   wave_amplitude is how tall/low the wave goes
        WAVE_OFFSET = 2.0
        WAVE_AMPLITUDE = 0.7
        
        # f(x) = wave_offset + wave_amplitude*sin((π/2)*x), then shifted by Y_SHIFT
        def f(x):
            return (WAVE_OFFSET + Y_SHIFT
                    + WAVE_AMPLITUDE * math.sin((math.pi/2)*x))

        # Center the points 0..11 horizontally
        left_x = - (n - 1) * spacing / 2

        ##################################################
        # 2) Top label: G, H, and f(x)=f(x+4) in one line
        ##################################################
        top_label = MathTex(
            r"G = \mathbb{Z}_{12},\quad H = \{0,4,8\} = \langle 4\rangle,\quad f(x) = f(x+4)"
        )
        top_label.to_edge(UP)  # place at top of the scene
        self.play(Write(top_label))
        self.wait()

        ##################################################
        # 3) Create & Animate the Wave Segments
        ##################################################
        wave_segments = VGroup()
        for k in range(n):
            start_point = np.array([left_x + k * spacing,     f(k),   0])
            end_point   = np.array([left_x + (k+1) * spacing, f(k+1), 0])
            segment = Line(
                start=start_point,
                end=end_point,
                color=coset_colors[k % 4],
                stroke_width=3
            )
            wave_segments.add(segment)
        
        self.play(Create(wave_segments))
        self.wait()

        ##################################################
        # 4) Create Z_12 Points (Dots) & Numeric Labels
        ##################################################
        points = VGroup()
        labels = VGroup()
        for k in range(n):
            x_coord = left_x + k * spacing
            # The number line is at y=Y_SHIFT
            dot = Dot([x_coord, Y_SHIFT, 0], radius=dot_radius)
            label = Tex(str(k)).next_to(dot, DOWN, buff=0.2)
            points.add(dot)
            labels.add(label)

        self.play(Create(points), Write(labels))
        self.wait()

        ##################################################
        # 5) Highlight Subgroup H
        ##################################################
        subgroup_circles = VGroup()
        for h in H:
            circle = Circle(radius=0.3, color=YELLOW)
            circle.move_to(points[h].get_center())
            subgroup_circles.add(circle)

        self.play(Create(subgroup_circles))
        self.wait()

        ##################################################
        # 6) Show Cosets g + H with Labels & Arrows
        ##################################################
        # We'll place coset labels below the line in 2 rows, 2 columns:
        #   g=0 -> top-left
        #   g=1 -> top-right
        #   g=2 -> bottom-left
        #   g=3 -> bottom-right
        # Shift them relative to Y_SHIFT so they're safely in view.
        coset_positions = [
            (-4, Y_SHIFT - 1.6),  # g=0 (top-left)
            ( 0, Y_SHIFT - 1.6),  # g=1 (top-right)
            (-4, Y_SHIFT - 2.6),  # g=2 (bottom-left)
            ( 0, Y_SHIFT - 2.6)   # g=3 (bottom-right)
        ]

        for g in range(4):
            # Sort coset elements
            coset = sorted(((x + g) % n) for x in H)
            color = coset_colors[g]

            # Draw circles around coset elements
            coset_group = VGroup()
            for c in coset:
                c_circle = Circle(radius=0.3, color=color).move_to(points[c].get_center())
                coset_group.add(c_circle)
            self.play(Create(coset_group))

            # Label for coset
            coset_label_str = f"{g}+H = " + "{" + ",".join(str(x) for x in coset) + "}"
            coset_label = Tex(coset_label_str)
            (x_pos, y_pos) = coset_positions[g]
            coset_label.move_to([x_pos, y_pos, 0])
            self.play(Write(coset_label))

            # Draw arrows: from each coset element to label & wave
            arrows = VGroup()
            for c in coset:
                # Arrow from dot to coset label
                arrow_label = Arrow(
                    start=points[c].get_bottom() + DOWN*0.1,
                    end=coset_label.get_top() + UP*0.05,
                    buff=0.1,
                    stroke_width=3,
                    color=color
                )
                arrows.add(arrow_label)

                # Arrow from dot to midpoint of wave segment [c, c+1]
                mid_x = c + 0.5
                mid_point = np.array([left_x + mid_x*spacing, f(mid_x), 0])
                arrow_wave = Arrow(
                    start=points[c].get_top() + UP*0.1,
                    end=mid_point,
                    buff=0,
                    stroke_width=3,
                    color=color
                )
                arrows.add(arrow_wave)

            self.play(Create(arrows))
            self.wait(1)

            # Remove arrows
            self.play(FadeOut(arrows))
            self.wait(0.5)

        # Final pause
        self.wait(2)
