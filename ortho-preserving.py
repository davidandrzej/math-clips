from manim import *
import numpy as np

# Manim Community Edition
# Run (example): manim -pqh ortho-preserving.py OrthogonalityTrick

def dot(a, b):
    return float(np.dot(np.array(a, dtype=float), np.array(b, dtype=float)))

def angle_between(u, v):
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return 0.0
    c = np.clip(dot(u, v) / (nu * nv), -1.0, 1.0)
    return float(np.arccos(c))

def apply_matrix_2d(mat, vec3):
    vec2 = mat @ np.array(vec3[:2], dtype=float)
    return np.array([vec2[0], vec2[1], 0.0], dtype=float)

def make_vector(vec, color, z_index=2):
    return Vector(
        vec,
        color=color,
        stroke_width=6,
        max_tip_length_to_length_ratio=0.2,
    ).set_z_index(z_index)

def unit_direction(vec):
    vec = np.array(vec, dtype=float)
    norm = np.linalg.norm(vec[:2])
    if norm == 0:
        return np.array([1.0, 0.0, 0.0], dtype=float)
    return np.array([vec[0] / norm, vec[1] / norm, 0.0], dtype=float)

def label_at_end(vector, tex, scale=0.6, buff=0.1):
    label = MathTex(tex).scale(scale).set_z_index(4)
    def _update(mob):
        direction = unit_direction(vector.get_vector())
        mob.next_to(vector.get_end(), direction, buff=buff)
    label.add_updater(_update)
    return label

def angle_arc_between(vu, vv, radius=0.6):
    u_vec = np.array(vu.get_vector(), dtype=float)
    v_vec = np.array(vv.get_vector(), dtype=float)
    if np.linalg.norm(u_vec[:2]) == 0 or np.linalg.norm(v_vec[:2]) == 0:
        return Arc(radius=radius, start_angle=0, angle=0.01, color=WHITE)
    ang1 = np.arctan2(u_vec[1], u_vec[0])
    ang2 = np.arctan2(v_vec[1], v_vec[0])
    delta = (ang2 - ang1) % TAU
    if delta > PI:
        delta = TAU - delta
        start = ang2
    else:
        start = ang1
    if np.isclose(delta, 0.0):
        delta = 0.01
    return Arc(radius=radius, start_angle=start, angle=delta, color=WHITE).set_z_index(1)

class OrthogonalityTrick(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.add(plane)

        title = Tex(r"$u=e_1+e_2,\; v=e_1-e_2$").scale(0.7).to_corner(UL, buff=0.3)
        self.add(title)

        e1 = np.array([1, 0, 0], dtype=float)
        e2 = np.array([0, 1, 0], dtype=float)
        u = e1 + e2
        v = e1 - e2

        def build_vectors():
            ve1 = make_vector(e1, BLUE, z_index=2)
            ve2 = make_vector(e2, BLUE, z_index=2)
            vu = make_vector(u, YELLOW, z_index=3)
            vv = make_vector(v, YELLOW, z_index=3)
            labels = VGroup(
                label_at_end(ve1, "e_1"),
                label_at_end(ve2, "e_2"),
                label_at_end(vu, "u"),
                label_at_end(vv, "v"),
            )
            return ve1, ve2, vu, vv, labels

        def build_hud(vu, vv):
            angle_arc = always_redraw(lambda: angle_arc_between(vu, vv, radius=0.6))
            angle_prefix = MathTex(r"\angle(u,v)\approx").scale(0.65)
            angle_value = DecimalNumber(0, num_decimal_places=0).scale(0.65)
            angle_suffix = MathTex(r"^\circ").scale(0.65)
            angle_group = VGroup(angle_prefix, angle_value, angle_suffix)
            def _update_angle(mob):
                mob[1].set_value(angle_between(vu.get_vector(), vv.get_vector()) * 180 / np.pi)
                mob.arrange(RIGHT, buff=0.05)
                mob.to_corner(UR, buff=0.35).shift(DOWN * 0.2)
            angle_group.add_updater(_update_angle)
            _update_angle(angle_group)

            dot_prefix = MathTex(r"\langle u,v\rangle \approx").scale(0.65)
            dot_value = DecimalNumber(0, num_decimal_places=2, include_sign=True).scale(0.65)
            dot_group = VGroup(dot_prefix, dot_value)
            def _update_dot(mob):
                mob[1].set_value(dot(vu.get_vector()[:2], vv.get_vector()[:2]))
                mob.arrange(RIGHT, buff=0.05)
                mob.next_to(angle_group, DOWN, buff=0.2, aligned_edge=RIGHT)
            dot_group.add_updater(_update_dot)
            _update_dot(dot_group)

            return angle_arc, angle_group, dot_group

        ve1, ve2, vu, vv, labels = build_vectors()
        angle_arc, angle_label, dot_label = build_hud(vu, vv)

        self.play(Create(ve1), Create(ve2))
        self.play(Create(vu), Create(vv))
        self.play(FadeIn(labels))
        self.add(angle_arc, angle_label, dot_label)
        self.wait(0.8)

        # ------------------------------------------------------------
        # Part 1: Orthogonality-preserving transform (rotation + uniform scale)
        # ------------------------------------------------------------
        part1 = Tex("Example A: rotation + uniform scale").scale(0.7).to_edge(UP, buff=0.8)
        self.play(FadeIn(part1))

        theta = 35 * DEGREES
        s = 1.6
        A = s * np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)],
        ])

        targets_a = [
            make_vector(apply_matrix_2d(A, e1), BLUE, z_index=2),
            make_vector(apply_matrix_2d(A, e2), BLUE, z_index=2),
            make_vector(apply_matrix_2d(A, u), YELLOW, z_index=3),
            make_vector(apply_matrix_2d(A, v), YELLOW, z_index=3),
        ]
        self.play(
            Transform(ve1, targets_a[0]),
            Transform(ve2, targets_a[1]),
            Transform(vu, targets_a[2]),
            Transform(vv, targets_a[3]),
            run_time=2,
        )

        self.wait(0.6)
        self.play(FadeOut(part1))
        self.wait(0.3)

        self.play(FadeOut(VGroup(ve1, ve2, vu, vv, labels, angle_arc, angle_label, dot_label)))
        self.remove(angle_arc, angle_label, dot_label, labels)
        self.wait(0.2)

        ve1, ve2, vu, vv, labels = build_vectors()
        angle_arc, angle_label, dot_label = build_hud(vu, vv)
        self.play(Create(ve1), Create(ve2))
        self.play(Create(vu), Create(vv))
        self.play(FadeIn(labels))
        self.add(angle_arc, angle_label, dot_label)
        self.wait(0.5)

        # ------------------------------------------------------------
        # Part 2: Anisotropic stretch (breaks orthogonality)
        # ------------------------------------------------------------
        part2 = Tex("Example B: anisotropic scaling").scale(0.7).to_edge(UP, buff=0.8)
        self.play(FadeIn(part2))

        B = np.array([[2.0, 0.0],
                      [0.0, 1.0]])
        targets_b = [
            make_vector(apply_matrix_2d(B, e1), BLUE, z_index=2),
            make_vector(apply_matrix_2d(B, e2), BLUE, z_index=2),
            make_vector(apply_matrix_2d(B, u), YELLOW, z_index=3),
            make_vector(apply_matrix_2d(B, v), YELLOW, z_index=3),
        ]
        self.play(
            Transform(ve1, targets_b[0]),
            Transform(ve2, targets_b[1]),
            Transform(vu, targets_b[2]),
            Transform(vv, targets_b[3]),
            run_time=2,
        )

        warn = Tex("Orthogonality breaks.").scale(0.7).set_color(RED)
        warn.next_to(part2, DOWN, buff=0.2)
        self.play(FadeIn(warn))
        self.wait(1.6)

        self.play(FadeOut(part2), FadeOut(warn))
        self.wait(0.5)
