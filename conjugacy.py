from manim import *

def rotation_about_origin(theta: float):
    """
    Returns a 3x3 rotation matrix (in homogeneous coordinates)
    for rotating by 'theta' around the origin in 2D.
    """
    import numpy as np
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [            0,              0, 1]
    ])

class S3ConjugacyClasses(Scene):
    def construct(self):
        # ------------------------------------------------------
        # 0) SET UP TITLES AND TEXT
        # ------------------------------------------------------
        # Main title at the top
        heading_text = Tex(r"Symmetric Group $S_3$ Conjugacy Classes").to_edge(UP)
        
        # Explanatory texts
        identity_text = Tex(r"No change, $e = \text{identity}$").next_to(heading_text, DOWN).align_to(heading_text, LEFT)
        reflection_text = Tex(r"Reflection, transposition, e.g.\ $(1\;2)$").move_to(identity_text)
        rotation_text = Tex(r"Rotation, 3-cycle, e.g.\ $(1\;2\;3)$").move_to(identity_text)

        # Show the main title on screen
        self.play(Write(heading_text))
        self.wait(0.5)

        # ------------------------------------------------------
        # 1) CONSTRUCT THE ORIGINAL EQUILATERAL TRIANGLE
        # ------------------------------------------------------
        # Coordinates for an equilateral triangle side=2, centered at origin
        A = np.array([-1, -np.sqrt(3)/2, 0])
        B = np.array([ 1, -np.sqrt(3)/2, 0])
        C = np.array([ 0,  np.sqrt(3)/2, 0])

        triangle = Polygon(A, B, C).set_stroke(WHITE, 3)
        labelA   = Text("A").scale(0.5).move_to(A * 1.1)
        labelB   = Text("B").scale(0.5).move_to(B * 1.1)
        labelC   = Text("C").scale(0.5).move_to(C * 1.1)

        # Show the "identity" text
        self.play(Write(identity_text))
        self.wait(0.5)

        # Draw the triangle
        self.play(Create(triangle), FadeIn(labelA), FadeIn(labelB), FadeIn(labelC))
        self.wait(1)

        # ------------------------------------------------------
        # 2) REFLECTION (TRANSPOSITION)
        #    Example reflection about x=0 line (x -> -x)
        # ------------------------------------------------------
        # Switch text from identity to reflection
        self.play(ReplacementTransform(identity_text, reflection_text))
        self.wait(0.5)

        # Reflection matrix (about vertical line x=0)
        reflect_x0 = np.array([
            [-1,  0, 0],
            [ 0,  1, 0],
            [ 0,  0, 1]
        ])

        # Animate reflection
        self.play(
            triangle.animate.apply_matrix(reflect_x0),
            labelA.animate.apply_matrix(reflect_x0),
            labelB.animate.apply_matrix(reflect_x0),
            labelC.animate.apply_matrix(reflect_x0),
            run_time=2
        )
        self.wait(1)

        # Bring the triangle back to original
        self.play(
            triangle.animate.apply_matrix(reflect_x0),
            labelA.animate.apply_matrix(reflect_x0),
            labelB.animate.apply_matrix(reflect_x0),
            labelC.animate.apply_matrix(reflect_x0),
            run_time=2
        )
        self.wait(1)

        # ------------------------------------------------------
        # 3) ROTATION (3-cycle)
        #    Example rotation by +120 degrees
        # ------------------------------------------------------
        # Switch text from reflection to rotation
        self.play(ReplacementTransform(reflection_text, rotation_text))
        self.wait(0.5)

        # Rotation by +120° about the origin
        rot_120 = rotation_about_origin(2 * PI / 3)

        # Animate rotation
        self.play(
            triangle.animate.apply_matrix(rot_120),
            labelA.animate.apply_matrix(rot_120),
            labelB.animate.apply_matrix(rot_120),
            labelC.animate.apply_matrix(rot_120),
            run_time=2
        )
        self.wait(2)

        # (Optional) rotate further or revert if desired:
        # rot_240 = rotation_about_origin(4*PI/3)
        # self.play(
        #     triangle.animate.apply_matrix(rot_240),
        #     labelA.animate.apply_matrix(rot_240),
        #     labelB.animate.apply_matrix(rot_240),
        #     labelC.animate.apply_matrix(rot_240),
        #     run_time=2
        # )
        # self.wait(2)


class OldS3ConjugacyClasses(Scene):
    def construct(self):
        # ------------------------------------------------------
        # 1) CONSTRUCT THE ORIGINAL EQUILATERAL TRIANGLE
        # ------------------------------------------------------
        # Coordinates for an equilateral triangle of side length 2, centered at the origin:
        A = np.array([-1, -np.sqrt(3)/2, 0])
        B = np.array([ 1, -np.sqrt(3)/2, 0])
        C = np.array([ 0,  np.sqrt(3)/2, 0])

        triangle = Polygon(A, B, C).set_stroke(WHITE, 3)
        labelA   = Text("A").scale(0.5).move_to(A*1.1)
        labelB   = Text("B").scale(0.5).move_to(B*1.1)
        labelC   = Text("C").scale(0.5).move_to(C*1.1)

        self.play(Create(triangle), FadeIn(labelA), FadeIn(labelB), FadeIn(labelC))
        self.wait(1)

        # ------------------------------------------------------
        # 2) EXAMPLE OF A REFLECTION (ONE REPRESENTATIVE)
        #    Reflection about the vertical line x = 0
        # ------------------------------------------------------
        reflect_x0 = np.array([
            [-1,  0, 0],  # x -> -x
            [ 0,  1, 0],  # y ->  y
            [ 0,  0, 1]
        ])
        
        self.play(
            triangle.animate.apply_matrix(reflect_x0),
            labelA.animate.apply_matrix(reflect_x0),
            labelB.animate.apply_matrix(reflect_x0),
            labelC.animate.apply_matrix(reflect_x0),
            run_time=2
        )
        self.wait(1)

        # Bring the triangle back
        self.play(
            triangle.animate.apply_matrix(reflect_x0),
            labelA.animate.apply_matrix(reflect_x0),
            labelB.animate.apply_matrix(reflect_x0),
            labelC.animate.apply_matrix(reflect_x0),
            run_time=2
        )
        self.wait(1)

        # ------------------------------------------------------
        # 3) EXAMPLE OF A ROTATION (ONE REPRESENTATIVE)
        #    Rotation by +120 degrees about the origin
        # ------------------------------------------------------
        rot_120 = rotation_about_origin(2*PI/3)
        
        self.play(
            triangle.animate.apply_matrix(rot_120),
            labelA.animate.apply_matrix(rot_120),
            labelB.animate.apply_matrix(rot_120),
            labelC.animate.apply_matrix(rot_120),
            run_time=2
        )
        self.wait(2)

        # (Optionally revert and/or show the -120° rotation)
        # rot_240 = rotation_about_origin(4*PI/3)
        # self.play(
        #     triangle.animate.apply_matrix(rot_240),
        #     labelA.animate.apply_matrix(rot_240),
        #     labelB.animate.apply_matrix(rot_240),
        #     labelC.animate.apply_matrix(rot_240),
        #     run_time=2
        # )
        # self.wait(2)
