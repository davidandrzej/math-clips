from manim import *
import numpy as np

"""Manim scene: cosets, non‑injective map T(n)=n mod 3, quotient fixing injectivity,
   with labels nudged farther left so they no longer crowd the graphics.

Run with (community v0.18):
    manim -pqh coset_partition_quotient.py CosetQuotientScene
"""

class CosetQuotientScene(Scene):
    def construct(self):
        # ----------------------------- CONFIG ---------------------------------
        self.N = 12              # size of ℤ₁₂
        self.step = 3            # H = 3ℤ₁₂
        self.outer_R = 3.0       # radius of ℤ₁₂ circle
        self.inner_r = 1.2       # radius of inner ℤ₃ circle
        self.shift_right = 4.5   # slide for codomain later
        self.coset_colors = [BLUE, GREEN, YELLOW]

        # 1 : outer circle ℤ₁₂ --------------------------------------------------
        self.draw_z12_outer_circle()
        self.wait(0.8)

        # 1b : inner circle ℤ₃ + many‑to‑one map ------------------------------
        self.draw_inner_z3_circle()
        self.show_non_injective_map()
        self.wait(1.0)

        # 2 : highlight kernel 3ℤ₁₂ -------------------------------------------
        self.highlight_kernel()
        self.wait(1.4)

        # 3 : build cosets visually -------------------------------------------
        self.build_cosets()
        self.wait(1.2)

        # 4 : form quotient clusters & slide ℤ₃ right --------------------------
        self.form_quotient_clusters()
        self.wait(0.4)
        self.move_z3_codomain_right()
        self.wait(1.0)

        # 5 : injective factor & isomorphism ----------------------------------
        self.show_injective_factor()
        self.wait(4.0)

    # ---------------------------------------------------------------------
    def draw_z12_outer_circle(self):
        self.outer_dots = VGroup(); self.outer_labels = VGroup()
        for k in range(self.N):
            ang = TAU * k / self.N
            pos = self.outer_R * np.array([np.cos(ang), np.sin(ang), 0])
            d = Dot(pos, radius=0.08)
            t = MathTex(str(k), font_size=28).next_to(d, 0.25 * (pos / self.outer_R))
            self.outer_dots.add(d); self.outer_labels.add(t)

        # **label moved farther left (buff = 2.0)**
        outer_lbl = MathTex(r"\mathbb{Z}_{12}").next_to(self.outer_dots, LEFT, buff=2.0)

        self.play(
            LaggedStart(*[Create(d) for d in self.outer_dots], lag_ratio=0.03, run_time=4),
            LaggedStart(*[Write(l) for l in self.outer_labels], lag_ratio=0.03, run_time=4),
            Write(outer_lbl)
        )

    # ---------------------------------------------------------------------
    def draw_inner_z3_circle(self):
        base = Circle(radius=self.inner_r, color=WHITE, stroke_opacity=0.3)
        self.inner_circle = DashedVMobject(base, num_dashes=60)
        self.inner_dots = VGroup(); self.inner_labels = VGroup()
        for k in range(self.step):
            ang = TAU * k / self.step + PI/2
            pos = self.inner_r * np.array([np.cos(ang), np.sin(ang), 0])
            d = Dot(pos, radius=0.1)
            t = MathTex(str(k)).next_to(d, 0.25 * (pos / self.inner_r))
            self.inner_dots.add(d); self.inner_labels.add(t)
        self.z3_label = MathTex(r"\mathbb{Z}_{3}").next_to(self.inner_circle, RIGHT, buff=0.6)
        self.play(Create(self.inner_circle, run_time=2),
                  LaggedStart(*[Create(d) for d in self.inner_dots], lag_ratio=0.15, run_time=2),
                  LaggedStart(*[Write(l) for l in self.inner_labels], lag_ratio=0.15, run_time=2),
                  Write(self.z3_label))

    # ---------------------------------------------------------------------
    def show_non_injective_map(self):
        self.non_inj_arrows = VGroup()
        for idx, d in enumerate(self.outer_dots):
            tgt = self.inner_dots[idx % 3]
            self.non_inj_arrows.add(Arrow(d.get_center(), tgt.get_center(), buff=0.08, stroke_width=1.8))
        caption_tex = MathTex(r"T(n)=n\bmod 3\;\text{(not injective)}", font_size=30)
        caption_tex.to_corner(UL)
        self.play(Create(self.non_inj_arrows, run_time=3), FadeIn(caption_tex))
        self.non_inj_caption = caption_tex

    # ---------------------------------------------------------------------
    def highlight_kernel(self):
        idxs_H = list(range(0, self.N, self.step))
        kernel_dots = VGroup(*[self.outer_dots[i] for i in idxs_H])
        kernel_arrows = VGroup(*[self.non_inj_arrows[i] for i in idxs_H])
        rect = SurroundingRectangle(kernel_dots, buff=0.3, color=RED)
        txt = MathTex(r"\ker T = 3\mathbb{Z}_{12}").next_to(rect, DOWN)
        self.play(*[d.animate.set_color(RED) for d in kernel_dots],
                  *[a.animate.set_color(RED) for a in kernel_arrows])
        self.play(Create(rect), Write(txt))
        self.play(FadeOut(rect), FadeOut(txt))

    # ---------------------------------------------------------------------
    def build_cosets(self):
        base = np.array(list(range(0, self.N, self.step)))
        for rep in range(self.step):
            idxs = list((base + rep) % self.N)
            grp = VGroup(*[self.outer_dots[i] for i in idxs], *[self.outer_labels[i] for i in idxs])
            if rep > 0:
                arrow = Arrow(self.outer_dots[base[0]].get_center(),
                               self.outer_dots[idxs[0]].get_center(),
                               buff=0.05, color=self.coset_colors[rep])
                shift_lbl = MathTex(f"+{rep}").next_to(arrow, DOWN, buff=0.1)
                self.play(Create(arrow), Write(shift_lbl))
            self.play(LaggedStart(*[m.animate.set_color(self.coset_colors[rep]) for m in grp],
                                   lag_ratio=0.03, run_time=1.5))
            if rep > 0:
                self.play(FadeOut(arrow), FadeOut(shift_lbl))
        self.coset_groups = [VGroup(*[self.outer_dots[i] for i in list((base + rep) % self.N)])
                             for rep in range(self.step)]

    # ---------------------------------------------------------------------
    def form_quotient_clusters(self):
        self.cluster_centers = VGroup(); self.cluster_circles = VGroup(); self.cluster_labels = VGroup()
        target_R = 1.9; anims = []
        for j, grp in enumerate(self.coset_groups):
            ang = TAU * j / self.step + PI / 2
            center = target_R * np.array([np.cos(ang), np.sin(ang), 0])
            circ = DashedVMobject(Circle(radius=0.55, color=self.coset_colors[j], stroke_width=2), num_dashes=40)
            circ.move_to(center)
            c_dot = Dot(center, radius=0.12, color=self.coset_colors[j])
            lbl = MathTex(f"[{j}]").next_to(c_dot, RIGHT)
            self.cluster_centers.add(c_dot); self.cluster_circles.add(circ); self.cluster_labels.add(lbl)
            n = len(grp)
            for k, d in enumerate(grp):
                theta = TAU * k / n
                dest = center + 0.45 * np.array([np.cos(theta), np.sin(theta), 0])
                anims.append(d.animate.move_to(dest).set_opacity(0))
            anims += [Create(circ), GrowFromCenter(c_dot), Write(lbl)]
        self.play(*anims, lag_ratio=0.02, run_time=6)

        # **quotient label moved farther left (buff = 2.0)**
        quot_lbl = MathTex(r"\mathbb{Z}_{12}/3\mathbb{Z}_{12}")\
                     .next_to(self.cluster_circles, LEFT, buff=2.0)
        self.play(Write(quot_lbl))

    # ---------------------------------------------------------------------
    def move_z3_codomain_right(self):
        group = VGroup(self.inner_circle, self.inner_dots, self.inner_labels, self.z3_label)
        self.play(group.animate.shift(RIGHT * self.shift_right),
                  FadeOut(self.non_inj_arrows), FadeOut(self.non_inj_caption), run_time=3)
        self.codomain_dots = self.inner_dots

    # ---------------------------------------------------------------------
    def show_injective_factor(self):
        inj_arrows = VGroup()
        for j in range(self.step):
            inj_arrows.add(Arrow(self.cluster_centers[j].get_center(),
                                 self.codomain_dots[j].get_center(),
                                 buff=0.1, stroke_width=2.5, color=self.coset_colors[j]))
        caption = Text("Injective after quotient", font_size=24).to_corner(UL)
        self.play(Create(inj_arrows, run_time=2.5), FadeIn(caption))
        iso = MathTex(r"\cong", font_size=80).move_to(inj_arrows.get_center())
        self.play(Transform(inj_arrows, iso), run_time=2)
