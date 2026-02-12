
from manim import *
import numpy as np

class KernelInjectiveIllustration(Scene):
    """
    Visual proof sketch that a homomorphism (here, a linear map) has
    trivial kernel  ⇔  it is injective.

    The scene is split in two parts:

    1.  **Trivial kernel ⇒ Injective**

        A transformation with no non‑zero kernel (rotation+shear) is applied.
        Two distinct vectors are shown to land at different images.

    2.  **Non‑trivial kernel ⇒ Not Injective**

        A projection onto the x‑axis is used.  Two different vectors land
        on the *same* image; the whole y‑axis is highlighted as the kernel.

    Finally, the equivalence statement is displayed as a takeaway box.
    """
    def construct(self):
        # ----------  Title  ----------
        title = MathTex(r"\text{Trivial Kernel} \iff \text{Injective}", font_size=48)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_edge(UP, buff=0.4))

        # ----------  Domain / Codomain setup  ----------
        plane_scale = 0.8
        plane_edge_buff = 0.2
        domain_plane   = NumberPlane(x_range=[-4, 4], y_range=[-3, 3],
                                     background_line_style={"stroke_opacity": 0.2}).scale(plane_scale)
        codomain_plane = domain_plane.copy()

        domain_plane.to_edge(LEFT,  buff=plane_edge_buff)
        codomain_plane.to_edge(RIGHT, buff=plane_edge_buff)

        domain_label   = MathTex(r"\text{Domain } V", font_size=32).next_to(domain_plane,   UP)
        codomain_label = MathTex(r"\text{Codomain } W", font_size=32).next_to(codomain_plane, UP)

        self.play(Create(domain_plane), Create(codomain_plane),
                  FadeIn(domain_label, codomain_label))
        self.wait(0.5)

        # Arrow indicating the map ϕ
        arrow_map = Arrow(
            domain_plane.get_right(),
            codomain_plane.get_left(),
            max_tip_length_to_length_ratio=0.12,
            stroke_width=6,
            buff=0,
        )
        phi_tex   = MathTex(r"\varphi").next_to(arrow_map, UP, buff=0.1)
        self.play(Create(arrow_map), Write(phi_tex))
        self.wait(0.5)

        diagram_group = VGroup(
            domain_plane,
            codomain_plane,
            domain_label,
            codomain_label,
            arrow_map,
            phi_tex,
        )

        # ════════════════════════════════════════════════════════════
        # PART 1 — Trivial kernel  ⇒  Injective
        # ════════════════════════════════════════════════════════════
        self.trivial_kernel_part(domain_plane, codomain_plane)

        # ════════════════════════════════════════════════════════════
        # PART 2 — Non‑trivial kernel  ⇒  Not injective
        # ════════════════════════════════════════════════════════════
        self.non_trivial_kernel_part(domain_plane, codomain_plane)

        # ----------  Wrap‑up slide  ----------
        self.play(FadeOut(diagram_group), FadeOut(title))

        summary_title = Tex(r"\textbf{Key Fact:}", font_size=40)
        summary_math = MathTex(
            r"\ker\varphi = \{0\} \iff \varphi \text{ is injective}",
            font_size=40,
        )
        summary = VGroup(summary_title, summary_math).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.3,
        )
        box = SurroundingRectangle(summary, buff=0.4)
        self.play(FadeIn(summary, box))
        self.wait(2)

        self.post_video_proof()

        self.wait(2)

    # ---------------------------------------------------------------
    #  Helper blocks
    # ---------------------------------------------------------------
    def trivial_kernel_part(self, domain_plane, codomain_plane):
        """Show that a map with trivial kernel is injective."""
        # A full‑rank linear map (rotation + shear) ⇒ ker = {0}
        matrix = [[1, -0.5],
                  [0.5, 1]]

        # Two distinct domain vectors
        v1 = np.array([2, 1, 0])
        v2 = np.array([-1, 2, 0])
        img1 = matrix @ v1[:2]
        img2 = matrix @ v2[:2]

        vec_v1     = Arrow(domain_plane.c2p(0, 0), domain_plane.c2p(*v1[:2]),
                           buff=0, color=BLUE)
        vec_v2     = Arrow(domain_plane.c2p(0, 0), domain_plane.c2p(*v2[:2]),
                           buff=0, color=GREEN)
        vec_img1   = Arrow(codomain_plane.c2p(0, 0), codomain_plane.c2p(*img1),
                           buff=0, color=BLUE)
        vec_img2   = Arrow(codomain_plane.c2p(0, 0), codomain_plane.c2p(*img2),
                           buff=0, color=GREEN)

        # Domain vectors appear
        self.play(GrowArrow(vec_v1), GrowArrow(vec_v2))
        self.wait(0.3)

        # Their images appear
        self.play(GrowArrow(vec_img1), GrowArrow(vec_img2))
        self.wait(0.3)

        note_line1 = MathTex(
            r"\text{Distinct vectors} \mapsto \text{distinct images}",
            font_size=28,
        )
        note_line2 = MathTex(r"\Rightarrow \text{Injective}", font_size=28)
        note = VGroup(note_line1, note_line2).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.1,
        ).next_to(codomain_plane, DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(1.5)

        self.play(FadeOut(vec_v1, vec_v2, vec_img1, vec_img2, note))

    def non_trivial_kernel_part(self, domain_plane, codomain_plane):
        """Show that a non‑trivial kernel means non‑injective."""
        # Projection onto x‑axis ⇒ ker = y‑axis
        matrix = [[1, 0],
                  [0, 0]]

        w1   = np.array([2, 3, 0])
        w2   = np.array([2, -1, 0])
        img  = matrix @ w1[:2]          # same image for w1 & w2

        vec_w1   = Arrow(domain_plane.c2p(0, 0), domain_plane.c2p(*w1[:2]),
                         buff=0, color=BLUE)
        vec_w2   = Arrow(domain_plane.c2p(0, 0), domain_plane.c2p(*w2[:2]),
                         buff=0, color=GREEN)
        vec_img1 = Arrow(
            codomain_plane.c2p(0, 0),
            codomain_plane.c2p(*img),
            buff=0,
            color=BLUE,
            stroke_width=8,
            stroke_opacity=0.6,
        )
        vec_img2 = Arrow(
            codomain_plane.c2p(0, 0),
            codomain_plane.c2p(*img),
            buff=0,
            color=GREEN,
            stroke_width=4,
            stroke_opacity=0.9,
        )

        self.play(GrowArrow(vec_w1), GrowArrow(vec_w2))
        self.wait(0.3)
        self.play(GrowArrow(vec_img1), GrowArrow(vec_img2))
        self.wait(0.3)

        note_line1 = MathTex(
            r"\text{Different vectors share an image}",
            font_size=26,
        )
        note_line2 = MathTex(r"\Rightarrow \text{Not injective}", font_size=26)
        note = VGroup(note_line1, note_line2).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.1,
        ).next_to(codomain_plane, DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(1)

        # Highlight kernel (y‑axis)
        y_axis = Line(
            domain_plane.c2p(0, -3),
            domain_plane.c2p(0, 3),
            color=RED,
            stroke_width=6,
        )
        ker_label = MathTex(r"\ker\varphi", color=RED).next_to(y_axis, LEFT, buff=0.2)
        self.play(Create(y_axis), FadeIn(ker_label))
        self.wait(0.5)

        ker_vec = np.array([0, 2.5, 0])
        vec_ker = Arrow(
            domain_plane.c2p(0, 0),
            domain_plane.c2p(*ker_vec[:2]),
            buff=0,
            color=RED,
        )
        zero_dot = Dot(codomain_plane.c2p(0, 0), color=RED)
        zero_label = MathTex(r"\mathbf{0}", color=RED).next_to(
            zero_dot,
            DOWN,
            buff=0.1,
        )
        self.play(GrowArrow(vec_ker))
        self.play(FadeIn(zero_dot, zero_label))
        self.wait(1)

        self.play(
            FadeOut(
                vec_w1,
                vec_w2,
                vec_img1,
                vec_img2,
                y_axis,
                ker_label,
                vec_ker,
                zero_dot,
                zero_label,
                note,
            )
        )

    def post_video_proof(self):
        """Post-video proof from phi(ab)=phi(a)phi(b)."""
        title = Tex(r"\textbf{Equational proof}", font_size=38)

        proof_lines = VGroup(
            MathTex(
                r"\ker\varphi=\{e\}\ \text{and}\ \varphi(a)=\varphi(b)",
                font_size=30,
            ),
            MathTex(
                r"\varphi(ab^{-1})=\varphi(a)\varphi(b)^{-1}=e",
                font_size=30,
            ),
            MathTex(
                r"ab^{-1}\in\ker\varphi \Rightarrow ab^{-1}=e \Rightarrow a=b",
                font_size=30,
            ),
            MathTex(
                r"\Rightarrow \varphi \text{ is injective.}",
                font_size=30,
            ),
            MathTex(
                r"\text{If } \varphi \text{ injective and } \varphi(x)=e,",
                font_size=30,
            ),
            MathTex(
                r"x=e \Rightarrow \ker\varphi=\{e\}",
                font_size=30,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        proof_group = VGroup(title, proof_lines).arrange(DOWN, buff=0.5)
        proof_group.to_edge(UP, buff=0.7)

        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(title))
        for line in proof_lines:
            self.play(Write(line))
            self.wait(0.4)
