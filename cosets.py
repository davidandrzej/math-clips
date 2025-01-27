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

# class CosetsAndWaveInZ12(Scene):
#     def construct(self):
#         ##################################################
#         # 1) Basic Setup and Parameters
#         ##################################################
#         n = 12                      # Size of Z_12
#         spacing = 1.0               # Horizontal spacing
#         dot_radius = 0.1            # Radius for each point
#         H = {0, 4, 8}               # Subgroup H = <4>
#         coset_colors = [RED, GREEN, BLUE, ORANGE]

#         # Function f(x) = offset + amplitude * sin((pi/2)*x),
#         # period = 4 in the x-variable.
#         wave_offset = 2.0
#         wave_amplitude = 0.7
#         def f(x):
#             return wave_offset + wave_amplitude * math.sin((math.pi / 2) * x)

#         # We'll center points 0..11 around x=0:
#         left_x = - (n - 1) * spacing / 2

#         ##################################################
#         # 2) Create the Sine Wave (segments from x=k to x=k+1)
#         ##################################################
#         wave_segments = VGroup()
#         for k in range(n):
#             # Start at (k, f(k)) => End at (k+1, f(k+1)),
#             # shifted horizontally so that integer k is at x = left_x + k*spacing.
#             start_point = np.array([left_x + k * spacing, f(k), 0])
#             end_point   = np.array([left_x + (k + 1) * spacing, f(k + 1), 0])
#             segment = Line(
#                 start=start_point,
#                 end=end_point,
#                 color=coset_colors[k % 4],
#                 stroke_width=3
#             )
#             wave_segments.add(segment)

#         # Animate the creation of all wave segments at once
#         self.play(Create(wave_segments))
#         self.wait()

#         ##################################################
#         # 3) Create Z_12 points (dots) and numeric labels
#         ##################################################
#         points = VGroup()
#         labels = VGroup()

#         for k in range(n):
#             x_coord = left_x + k * spacing
#             dot = Dot([x_coord, 0, 0], radius=dot_radius)
#             label = Tex(str(k)).next_to(dot, DOWN, buff=0.2)
#             points.add(dot)
#             labels.add(label)

#         self.play(Create(points), Write(labels))
#         self.wait()

#         ##################################################
#         # 4) Top Labels: G, H, and Periodicity f(x)=f(x+4)
#         ##################################################
#         top_label_line1 = MathTex(r"G = \mathbb{Z}_{12},\quad H = \{0,4,8\} = \langle 4\rangle")
#         top_label_line2 = MathTex(r"f(x) = f(x + 4)")
#         top_labels = VGroup(top_label_line1, top_label_line2).arrange(DOWN)
#         top_labels.to_edge(UP)
#         self.play(Write(top_labels))
#         self.wait()

#         ##################################################
#         # 5) Highlight Subgroup H
#         ##################################################
#         subgroup_circles = VGroup()
#         for h in H:
#             circle = Circle(radius=0.3, color=YELLOW)
#             circle.move_to(points[h].get_center())
#             subgroup_circles.add(circle)

#         self.play(Create(subgroup_circles))
#         self.wait()

#         ##################################################
#         # 6) Show Cosets g + H
#         ##################################################
#         # We'll place the coset labels in 2 rows, 2 columns:
#         #   g=0 -> top-left, g=1 -> top-right,
#         #   g=2 -> bottom-left, g=3 -> bottom-right.
#         coset_positions = [
#             (-4, -1.5),  # g=0
#             ( 0, -1.5),  # g=1
#             (-4, -2.5),  # g=2
#             ( 0, -2.5)   # g=3
#         ]

#         for g in range(4):
#             coset = sorted(((x + g) % n) for x in H)
#             color = coset_colors[g]

#             # Draw circles around coset elements
#             coset_group = VGroup()
#             for c in coset:
#                 c_circle = Circle(radius=0.3, color=color).move_to(points[c].get_center())
#                 coset_group.add(c_circle)
#             self.play(Create(coset_group))

#             # Create & show the coset label
#             coset_label_str = f"{g}+H = " + "{" + ",".join(str(x) for x in coset) + "}"
#             coset_label = Tex(coset_label_str)
#             (x_pos, y_pos) = coset_positions[g]
#             coset_label.move_to([x_pos, y_pos, 0])
#             self.play(Write(coset_label))

#             # Draw arrows: from each coset element to the label + to the wave
#             arrows = VGroup()
#             for c in coset:
#                 # Arrow from dot to coset label
#                 arrow_label = Arrow(
#                     start=points[c].get_bottom() + DOWN * 0.1,
#                     end=coset_label.get_top() + UP * 0.05,
#                     buff=0.1, stroke_width=3,
#                     color=color
#                 )
#                 arrows.add(arrow_label)

#                 # Arrow from dot to midpoint of wave segment [c, c+1]
#                 mid_x = c + 0.5
#                 mid_point = np.array([
#                     left_x + mid_x * spacing,
#                     f(mid_x),
#                     0
#                 ])
#                 arrow_wave = Arrow(
#                     start=points[c].get_top() + UP * 0.1,
#                     end=mid_point,
#                     buff=0, stroke_width=3,
#                     color=color
#                 )
#                 arrows.add(arrow_wave)

#             # Animate the creation of all arrows
#             self.play(Create(arrows))
#             self.wait(1)

#             # Fade the arrows out before next coset
#             self.play(FadeOut(arrows))
#             self.wait(0.5)

#         self.wait(2)

# class CosetsAndWaveInZ12(Scene):
#     def construct(self):
#         # ---------------------------
#         # 1) Basic parameters
#         # ---------------------------
#         n = 12                      # Size of Z_n = Z_{12}
#         spacing = 1.0               # Horizontal spacing for points
#         dot_radius = 0.1            # Radius of each point on the line
#         # Colors used for cosets/wave segments
#         coset_colors = [RED, GREEN, BLUE, ORANGE]
        
#         # Subgroup H = <4> = {0,4,8}
#         H = {0, 4, 8}
        
#         # ---------------------------
#         # 2) Create the number line points and labels
#         # ---------------------------
#         # We'll center the 12 points around the origin. The leftmost point (0) is at x=left_x.
#         left_x = - (n - 1) * spacing / 2
#         points = VGroup()
#         labels = VGroup()
        
#         for k in range(n):
#             x_coord = left_x + k * spacing
#             dot = Dot([x_coord, 0, 0], radius=dot_radius)
#             # Put the dot slightly higher in z so circles behind are visible
#             dot.set_z_index(2)
            
#             label = Tex(str(k)).next_to(dot, DOWN, buff=0.2)
#             label.set_z_index(3)
            
#             points.add(dot)
#             labels.add(label)
        
#         self.play(Create(points), Write(labels))
#         self.wait(0.5)
        
#         # ---------------------------
#         # 3) Top label: G and H together
#         # ---------------------------
#         top_label = MathTex(r"G = \mathbb{Z}_{12},\quad H = \{0,4,8\} = \langle 4\rangle")
#         top_label.to_edge(UP)
#         top_label.set_z_index(5)
#         self.play(Write(top_label))
#         self.wait(0.5)

#         # ---------------------------
#         # 4) Plot a sine wave of period 4 above the number line
#         #    color-coded to match each point/coset.
#         # ---------------------------
#         # We'll draw the wave from x=0 to x=12 so we see three full periods (since period=4).
#         # However, the group has points 0..11; the segment [11,12] will just match point 11's color.
        
#         wave_y_offset = 2.0       # Vertical shift so wave sits above the line
#         wave_amplitude = 0.7      # Amplitude of the sine wave
#         wave_segments = VGroup()
        
#         # Function for the sine wave at a parameter t (0 <= t <= 12):
#         #   x(t) = left_x + t * spacing  (so it aligns over the number line)
#         #   y(t) = wave_y_offset + wave_amplitude*sin((pi/2)*t)
#         def wave_func(t):
#             return np.array([
#                 left_x + t * spacing,
#                 wave_y_offset + wave_amplitude * np.sin((PI/2)*t),
#                 0
#             ])
        
#         # Build 12 small segments [k, k+1] and color them based on coset_colors[k % 4]
#         for k in range(n):
#             segment = ParametricFunction(
#                 wave_func,
#                 t_range=[k, k+1],
#                 color=coset_colors[k % 4],
#                 stroke_width=3
#             )
#             # Place the wave behind the top label but above the circles
#             segment.set_z_index(1)
#             wave_segments.add(segment)
        
#         # Animate the wave creation (all at once or piecewise)
#         self.play(LaggedStartMap(Create, wave_segments, lag_ratio=0.05))
#         self.wait(1)

#         # ---------------------------
#         # 5) Highlight subgroup H
#         # ---------------------------
#         subgroup_circles = VGroup()
#         for h in H:
#             circle = Circle(radius=0.3, color=YELLOW)
#             circle.move_to(points[h].get_center())
#             # Place behind the dot itself
#             circle.set_z_index(1)
#             subgroup_circles.add(circle)
        
#         self.play(LaggedStartMap(Create, subgroup_circles, lag_ratio=0.2))
#         self.wait(1)
        
#         # ---------------------------
#         # 6) Show cosets g + H
#         # ---------------------------
#         # We'll place coset labels in two rows, 2 columns each, to avoid overlap.
#         coset_positions = [
#             (-4, -1.5),  # g=0 -> top-left
#             ( 0, -1.5),  # g=1 -> top-right
#             (-4, -2.5),  # g=2 -> bottom-left
#             ( 0, -2.5)   # g=3 -> bottom-right
#         ]
        
#         for g in range(4):
#             # Coset elements sorted
#             coset = sorted(((x + g) % n) for x in H)
#             color = coset_colors[g % 4]
            
#             # Circles around coset elements
#             coset_circles = VGroup(
#                 *[
#                     Circle(radius=0.3, color=color)
#                         .move_to(points[c].get_center())
#                         .set_z_index(1)
#                     for c in coset
#                 ]
#             )
#             self.play(LaggedStartMap(Create, coset_circles, lag_ratio=0.2))
            
#             # Label the coset
#             coset_label_str = f"{g}+H = " + "{" + ",".join(str(c) for c in coset) + "}"
#             coset_label = Tex(coset_label_str)
#             coset_label.set_z_index(5)
            
#             x_pos, y_pos = coset_positions[g]
#             coset_label.move_to([x_pos, y_pos, 0])
#             self.play(Write(coset_label))
            
#             # Draw arrows from each element to its label
#             arrows = VGroup()
#             for c in coset:
#                 arrow = Arrow(
#                     start=points[c].get_bottom() + DOWN*0.1,
#                     end=coset_label.get_top() + UP*0.05,
#                     buff=0.1,
#                     stroke_width=3,
#                     color=color
#                 )
#                 arrow.set_z_index(4)
#                 arrows.add(arrow)
            
#             self.play(LaggedStartMap(Create, arrows, lag_ratio=0.2))
#             self.wait(1)
            
#             # Remove arrows
#             self.play(FadeOut(arrows))
#             self.wait(0.5)
        
#         # Final pause
#         self.wait(2)

class CosetsOfHInZ12(Scene):
    def construct(self):
        # Parameters
        n = 12               # Size of Z_n
        spacing = 1.0        # Horizontal spacing between points
        subgroup_color = YELLOW
        coset_colors = [RED, GREEN, BLUE, ORANGE]
        
        # Define subgroup H = <4> = {0,4,8} in Z_12
        H = {0, 4, 8}
        
        # Create 12 equally spaced points for Z_{12}
        points = VGroup()
        labels = VGroup()
        
        # We'll center the number line around the origin
        left_x = - (n - 1) * spacing / 2  # x-position of the "0" element
        for i in range(n):
            dot = Dot([left_x + i * spacing, 0, 0], radius=0.1)
            dot.set_z_index(2)  # Ensure dots appear above circles
            label = Tex(str(i)).next_to(dot, DOWN, buff=0.2)
            label.set_z_index(3)  # Labels on top of dots
            points.add(dot)
            labels.add(label)
        
        # Draw the points and their labels
        self.play(Create(points), Write(labels))
        self.wait()
        
        # Add a top-level label for G = Z_{12}
        g_label = MathTex("G = \\mathbb{Z}_{12}")
        g_label.to_edge(UP)
        g_label.set_z_index(5)
        self.play(Write(g_label))
        self.wait()
        
        # Highlight subgroup H = {0,4,8} = <4>
        subgroup_circles = VGroup()
        for h in H:
            circle = Circle(radius=0.3, color=subgroup_color)
            circle.move_to(points[h].get_center())
            circle.set_z_index(1)  # Slightly behind the dots so dots sit 'inside' the circle
            subgroup_circles.add(circle)
        
        self.play(LaggedStartMap(Create, subgroup_circles, lag_ratio=0.2))
        
        # Subgroup label H above the line (with generator notation)
        h_center_x = (
            points[0].get_center()[0] + 
            points[4].get_center()[0] + 
            points[8].get_center()[0]
        ) / 3
        h_label = MathTex(r"H = \{0,4,8\} = \langle 4 \rangle")
        h_label.move_to([h_center_x, 1, 0])
        h_label.set_z_index(5)
        self.play(Write(h_label))
        self.wait(1)
        
        # Prepare positions for the coset labels, using two rows:
        #   g=0 -> top-left
        #   g=1 -> top-right
        #   g=2 -> bottom-left
        #   g=3 -> bottom-right
        coset_positions = [
            (-4, -1.5),  # g=0
            ( 0, -1.5),  # g=1
            (-4, -2.5),  # g=2
            ( 0, -2.5)   # g=3
        ]
        
        for g in range(4):
            # Sort the coset elements in ascending order
            coset = sorted((x + g) % n for x in H)
            color = coset_colors[g % len(coset_colors)]
            
            # Highlight the elements of this coset
            coset_circles = VGroup(
                *[
                    Circle(radius=0.3, color=color)
                        .move_to(points[c].get_center())
                        .set_z_index(1)  # Place circles behind the dots
                    for c in coset
                ]
            )
            self.play(LaggedStartMap(Create, coset_circles, lag_ratio=0.2))
            
            # Create a label for the coset (sorted)
            coset_label_str = f"{g}+H = " + "{" + ",".join(str(c) for c in coset) + "}"
            coset_label_mobj = Tex(coset_label_str)
            coset_label_mobj.set_z_index(5)  # On top
                        
            # Position the label from our predefined positions
            x_pos, y_pos = coset_positions[g]
            coset_label_mobj.move_to([x_pos, y_pos, 0])
            self.play(Write(coset_label_mobj))
            
            # Draw arrows from each coset element to the coset label
            arrows = VGroup()
            for c in coset:
                arrow = Arrow(
                    start=points[c].get_bottom() + DOWN*0.1,
                    end=coset_label_mobj.get_top() + UP*0.05,
                    buff=0.1,
                    stroke_width=3,
                    color=color
                )
                arrow.set_z_index(4)  # Arrows above circles, below label
                arrows.add(arrow)
            
            self.play(LaggedStartMap(Create, arrows, lag_ratio=0.2))
            self.wait(1)
            
            # Remove arrows before moving to the next coset
            self.play(FadeOut(arrows))
            self.wait(0.5)
        
        # Final pause
        self.wait(2)

# class CosetsOfHInZ12(Scene):
#     def construct(self):
#         # Some configurable parameters
#         n = 12               # Size of Z_n
#         spacing = 1.0        # Horizontal spacing between points
#         subgroup_color = YELLOW
#         coset_colors = [RED, GREEN, BLUE, ORANGE]
        
#         # Define subgroup H = <4> = {0,4,8} in Z_12
#         H = {0, 4, 8}
        
#         # Create 12 equally spaced points for Z_{12}
#         points = VGroup()
#         labels = VGroup()
        
#         # We'll center the number line roughly at the origin
#         left_x = - (n - 1) * spacing / 2  # x-position of the "0" element
#         for i in range(n):
#             dot = Dot([left_x + i*spacing, 0, 0], radius=0.1)
#             label = Tex(str(i)).next_to(dot, DOWN, buff=0.2)
#             points.add(dot)
#             labels.add(label)
        
#         # Draw the points and their labels
#         self.play(Create(points), Write(labels))
#         self.wait()
        
#         # Add a top-level label for G = Z_12
#         g_label = MathTex("G = \\mathbb{Z}_{12}")
#         g_label.to_edge(UP)
#         self.play(Write(g_label))
#         self.wait()
        
#         # Highlight subgroup H = {0,4,8} = <4>
#         subgroup_circles = VGroup()
#         for h in H:
#             circle = Circle(radius=0.3, color=subgroup_color)
#             circle.move_to(points[h].get_center())
#             subgroup_circles.add(circle)
        
#         self.play(LaggedStartMap(Create, subgroup_circles, lag_ratio=0.2))
        
#         # Subgroup label H above the line (with generator notation)
#         h_center_x = (
#             points[0].get_center()[0] + 
#             points[4].get_center()[0] + 
#             points[8].get_center()[0]
#         ) / 3
#         h_label = MathTex(r"H = \{0,4,8\} = \langle 4 \rangle")
#         h_label.move_to([h_center_x, 1, 0])
#         self.play(Write(h_label))
#         self.wait(1)
        
#         # We will place the coset labels along y = -1.5, spaced horizontally
#         # at x positions that accommodate four labels comfortably.
#         coset_label_x_positions = [-6, -2, 2, 6]
#         coset_label_y = -1.5
        
#         for g, x_pos in zip(range(4), coset_label_x_positions):
#             coset = [(x + g) % n for x in H]
#             color = coset_colors[g % len(coset_colors)]
            
#             # Animate highlighting of this coset
#             coset_circles = VGroup(
#                 *[
#                     Circle(radius=0.3, color=color).move_to(points[c].get_center())
#                     for c in coset
#                 ]
#             )
#             self.play(LaggedStartMap(Create, coset_circles, lag_ratio=0.2))
            
#             # Create a label for the coset: g+H = {...}
#             coset_label_str = f"{g}+H = " + "{" + ",".join(str(x) for x in coset) + "}"
#             coset_label_mobj = Tex(coset_label_str)
            
#             # Place it at the desired (x_pos, coset_label_y)
#             coset_label_mobj.move_to([x_pos, coset_label_y, 0])
#             self.play(Write(coset_label_mobj))
            
#             # Draw arrows from each coset element to the coset label
#             arrows = VGroup()
#             for c in coset:
#                 arrow = Arrow(
#                     start=points[c].get_bottom() + DOWN*0.1,
#                     end=coset_label_mobj.get_top() + UP*0.05,
#                     buff=0.1,
#                     stroke_width=3,
#                     color=color
#                 )
#                 arrows.add(arrow)
            
#             self.play(LaggedStartMap(Create, arrows, lag_ratio=0.2))
#             self.wait(1)
            
#             # After viewing the arrows for this coset, remove them before moving to the next coset
#             self.play(FadeOut(arrows))
#             self.wait(0.5)
        
#         # Final pause
#         self.wait(2)



# # class CosetsOfHInZ12(Scene):
# #     def construct(self):
# #         # Some configurable parameters
# #         n = 12               # Size of Z_n
# #         spacing = 1.0        # Horizontal spacing between points
# #         subgroup_color = YELLOW
# #         coset_colors = [RED, GREEN, BLUE, ORANGE]
        
# #         # Define subgroup H = <4> = {0,4,8} in Z_12
# #         H = {0, 4, 8}
        
# #         # Create 12 equally spaced points for Z_{12}
# #         points = VGroup()
# #         labels = VGroup()
        
# #         # We'll center the number line roughly at the origin
# #         # so that 0..11 are distributed around the center.
# #         # The leftmost point will be at some negative x-offset
# #         # to keep the points centered in the scene.
        
# #         left_x = - (n - 1) * spacing / 2  # x-position of the "0" element
# #         for i in range(n):
# #             dot = Dot([left_x + i*spacing, 0, 0], radius=0.1)
# #             label = Tex(str(i)).next_to(dot, DOWN, buff=0.2)
# #             points.add(dot)
# #             labels.add(label)
        
# #         # Draw the points and their labels
# #         self.play(Create(points), Write(labels))
# #         self.wait()
        
# #         # Highlight subgroup H
# #         # We will circle them or change their color.
# #         subgroup_circles = VGroup()
# #         for h in H:
# #             circle = Circle(radius=0.3, color=subgroup_color)
# #             circle.move_to(points[h].get_center())
# #             subgroup_circles.add(circle)
        
# #         self.play(LaggedStartMap(Create, subgroup_circles, lag_ratio=0.2))
        
# #         # Subgroup label H above the line
# #         # We'll position it above the midpoint of the three elements in H.
# #         # You can adjust x/y shifts to taste.
# #         h_center_x = (
# #             points[0].get_center()[0] + 
# #             points[4].get_center()[0] + 
# #             points[8].get_center()[0]
# #         ) / 3
# #         h_label = MathTex("H = \\{0,4,8\\}")
# #         h_label.move_to([h_center_x, 1, 0])
# #         self.play(Write(h_label))
# #         self.wait(1)
        
# #         # Now highlight each coset g + H for g = 0,1,2,3 in a different color
# #         for g in range(4):
# #             coset = [(x + g) % n for x in H]
# #             color = coset_colors[g % len(coset_colors)]
            
# #             # Animate highlighting of this coset
# #             coset_circles = VGroup(
# #                 *[
# #                     Circle(radius=0.3, color=color).move_to(points[c].get_center())
# #                     for c in coset
# #                 ]
# #             )
# #             self.play(LaggedStartMap(Create, coset_circles, lag_ratio=0.2))
            
# #             # Create a label for the coset (optional: show it as g+H or as {...,...,...})
# #             coset_label_str = f"{g}+H = " + "{" + ",".join(str(x) for x in coset) + "}"
# #             coset_label_mobj = Tex(coset_label_str)
            
# #             # Position the label below the midpoint of these coset elements
# #             coset_center_x = sum(points[c].get_center()[0] for c in coset) / len(coset)
# #             coset_label_mobj.move_to([coset_center_x, -1.3 - 0.3*g, 0])
            
# #             # Animate the label
# #             self.play(Write(coset_label_mobj))
            
# #             # Draw arrows from each coset element to its coset label
# #             arrows = VGroup()
# #             for c in coset:
# #                 arrow = Arrow(
# #                     start=points[c].get_bottom() + DOWN*0.1,
# #                     end=coset_label_mobj.get_top() + UP*0.05,
# #                     buff=0.1,
# #                     stroke_width=3,
# #                     color=color
# #                 )
# #                 arrows.add(arrow)
            
# #             self.play(LaggedStartMap(Create, arrows, lag_ratio=0.2))
# #             self.wait(1)
        
# #         self.wait(2)  # Final pause for viewing
