from manim import *

class MatrixDotProductCenter(Scene):
    def construct(self):
        # --------------------------------------------------
        # 1) SETUP: Create A (4x3), x (3x1), but NOT b's boxes yet
        # --------------------------------------------------
        rows, cols = 4, 3
        box_size = 0.6
        box_buff = 0.1

        # 1a) Matrix A
        matrix_boxes = VGroup()
        for r in range(rows):
            row_group = VGroup()
            for c in range(cols):
                sq = Square(side_length=box_size)
                sq.set_fill(WHITE, opacity=1).set_stroke(WHITE, width=2)
                row_group.add(sq)
            row_group.arrange(RIGHT, buff=box_buff)
            matrix_boxes.add(row_group)
        matrix_boxes.arrange(DOWN, buff=box_buff, aligned_edge=LEFT)
        matrix_boxes.shift(3 * LEFT)
        
        # Give A a label, with bigger vertical buff
        label_A = MathTex("A")
        label_A.next_to(matrix_boxes, UP, buff=1.0)  # Increased from 0.5

        # 1b) Vector x (3x1)
        vector_boxes = VGroup()
        for _ in range(cols):
            sq = Square(side_length=box_size)
            sq.set_fill(BLACK, opacity=1).set_stroke(WHITE, width=2)
            vector_boxes.add(sq)
        vector_boxes.arrange(DOWN, buff=box_buff)
        vector_boxes.next_to(matrix_boxes, RIGHT, buff=2)

        # Label x with a bigger buff as well
        label_x = MathTex("x")
        label_x.next_to(vector_boxes, UP, buff=1.0)  # Increased from 0.5

        # Group A and x so we can center them together
        ax_group = VGroup(matrix_boxes, vector_boxes)
        ax_group.shift(UP * 0.5)

        # Add A, x, and their labels to the scene
        self.add(matrix_boxes, vector_boxes, label_A, label_x)

        # --------------------------------------------------
        # 2) PREPARE A PLACE FOR b, BUT DON'T SHOW BOXES YET
        # --------------------------------------------------
        b_placeholders = VGroup()
        for _ in range(rows):
            # Invisible square placeholders
            sq = Square(side_length=box_size)
            sq.set_opacity(0)  # fully invisible
            b_placeholders.add(sq)
        b_placeholders.arrange(DOWN, buff=box_buff)

        # Place b to the right of x
        b_placeholders.next_to(vector_boxes, RIGHT, buff=2)

        # Now center it vertically with A & x
        b_placeholders_center = b_placeholders.get_center()
        ax_center = ax_group.get_center()
        # Match their y-coordinates
        b_placeholders.move_to([b_placeholders_center[0], ax_center[1], 0])

        label_b = MathTex("b")
        label_b.next_to(b_placeholders, UP, buff=0.5)

        # We add the label b, but remove the placeholders from view
        self.add(label_b)
        result_positions = [sq.get_center() for sq in b_placeholders]
        self.remove(b_placeholders)

        # --------------------------------------------------
        # 3) DOT PRODUCT ANIMATION (Row by Row)
        # --------------------------------------------------

        def create_dithered_box(side_length):
            """Black fill + white stroke + horizontal stripes."""
            outer_sq = Square(side_length=side_length)
            outer_sq.set_fill(BLACK, opacity=1)
            outer_sq.set_stroke(WHITE, width=2)

            stripes = VGroup()
            top = side_length / 2
            bottom = -side_length / 2
            left = -side_length / 2
            right = side_length / 2
            stripe_spacing = 0.08
            y = top
            while y > bottom:
                line = Line([left, y, 0], [right, y, 0])
                line.set_stroke(WHITE, width=1, opacity=0.7)
                stripes.add(line)
                y -= stripe_spacing

            return VGroup(outer_sq, stripes)

        for i, row_group in enumerate(matrix_boxes):
            # Copy row i "in place"
            row_copy = row_group.copy()
            self.add(row_copy)  # on top of original

            # (a) Rotate + Move row_copy near x
            row_target = row_group.copy()
            row_center = row_target.get_center()
            row_target.rotate(-90 * DEGREES, about_point=row_center)

            shift_left = 1.0
            for sq_idx in range(cols):
                sq_t = row_target[sq_idx]
                sq_x = vector_boxes[sq_idx]
                desired_center = sq_x.get_center() + LEFT * shift_left
                sq_t.shift(desired_center - sq_t.get_center())

            # Animate into that position
            self.play(Transform(row_copy, row_target), run_time=2)

            # (b) "Pass through" x from left->right
            pass_distance = 2.0
            self.play(row_copy.animate.shift(RIGHT * pass_distance), run_time=2)

            # (c) Transform squares into dithered boxes
            dithered_copies = VGroup()
            for sq_copy in row_copy:
                new_box = create_dithered_box(box_size)
                new_box.move_to(sq_copy.get_center())
                dithered_copies.add(new_box)
            self.play(
                *[
                    Transform(sq_copy, d_box)
                    for sq_copy, d_box in zip(row_copy, dithered_copies)
                ],
                run_time=1
            )

            # (d) Merge partial-product squares into 1 final box
            final_box = create_dithered_box(box_size)
            final_box.move_to(row_copy.get_center())
            self.play(Transform(row_copy, final_box), run_time=1)

            # (e) Move that final box to the correct position
            self.play(row_copy.animate.move_to(result_positions[i]), run_time=1)

        self.wait(2)
