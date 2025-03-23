from manim import *
import numpy as np

class QueueFlowDiagram(Scene):
    def construct(self):
        # -------------------------------
        # GLOBAL TIMELINE SETUP
        # -------------------------------
        global_clock = ValueTracker(0)
        self.add(global_clock)

        # -------------------------------
        # SETUP: FLOW CHART (Left Side)
        # -------------------------------
        # Set up the Flow axes with a y_range that matches the number of items.
        items_data = [
            {"color": BLUE,   "arrival": 0,    "processing_start": 0,   "finish": 3},
            {"color": RED,    "arrival": 2,    "processing_start": 3,   "finish": 6},
            {"color": GREEN,  "arrival": 2.05, "processing_start": 6,   "finish": 9},
            {"color": YELLOW, "arrival": 2.1,  "processing_start": 9,   "finish": 12},
            {"color": PURPLE, "arrival": 5,    "processing_start": 12,  "finish": 15},
        ]
        n_items = len(items_data)
        flow_axes = Axes(
            x_range=[0, 16, 1],
            y_range=[0, n_items, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True, "color": WHITE},
        )
        # Downscale the Flow chart by 40%
        flow_axes.scale(0.6)
        flow_axes.to_edge(LEFT, buff=1)
        self.play(Create(flow_axes))
        time_label = Text("Time", font_size=24).next_to(flow_axes, DOWN)
        self.play(Write(time_label))
        # A vertical yellow line indicates the current global time.
        time_line = always_redraw(lambda: 
            Line(
                start=flow_axes.c2p(global_clock.get_value(), 0),
                end=flow_axes.c2p(global_clock.get_value(), n_items),
                color=YELLOW
            )
        )
        self.add(time_line)

        # Create the Flow bars, dots, and connection lines.
        flow_bars = VGroup()
        # Reversed vertical ordering: first item at the bottom.
        for i, item in enumerate(items_data):
            row = i  # row 0 is the bottom.
            start = item["processing_start"]
            finish = item["finish"]
            bar_width = flow_axes.c2p(finish, 0)[0] - flow_axes.c2p(start, 0)[0]
            bar = Rectangle(
                width=bar_width, height=0.5,
                fill_color=item["color"], fill_opacity=0.8, stroke_width=0
            )
            # Place the bar so its center is at x=(start+finish)/2 and y=row+0.5.
            bar.move_to(flow_axes.c2p((start + finish) / 2, row + 0.5))
            # Dot marking the arrival time.
            dot = Dot(point=flow_axes.c2p(item["arrival"], row + 0.5), color=item["color"])
            # Thin line connecting the dot to the left edge of the bar.
            connection_line = Line(
                start=flow_axes.c2p(item["arrival"], row + 0.5),
                end=flow_axes.c2p(start, row + 0.5),
                color=item["color"],
                stroke_width=2
            )
            flow_bars.add(connection_line, bar, dot)
        self.play(FadeIn(flow_bars))

        # -------------------------------
        # SETUP: QUEUE ANIMATION (To the Right of the Flow Chart)
        # -------------------------------
        queue_offset = flow_axes.get_right() + RIGHT * 1.5

        pipe_top = Line(
            start=[0, 0.5, 0] + queue_offset,
            end=[3, 0.5, 0] + queue_offset,
            color=WHITE
        )
        pipe_bottom = Line(
            start=[0, -0.5, 0] + queue_offset,
            end=[3, -0.5, 0] + queue_offset,
            color=WHITE
        )
        self.play(Create(pipe_top), Create(pipe_bottom))
        processing_box_center = np.array([3.5, 0, 0]) + queue_offset
        proc_box = Rectangle(width=1, height=1, color=WHITE)
        proc_box.move_to(processing_box_center)
        proc_box_label = Text("Processing", font_size=24)
        proc_box_label.next_to(proc_box, UP)
        self.play(Create(proc_box), Write(proc_box_label))

        # Create block objects for the queue.
        blocks = []
        for i, item in enumerate(items_data):
            block = Square(side_length=0.5, fill_color=item["color"], fill_opacity=1)
            block.move_to(np.array([-1, 0, 0]) + queue_offset)
            blocks.append(block)
            self.add(block)

        def get_waiting_slot(index):
            gap = 0.8
            x = 2.2 - index * gap
            return np.array([x, 0, 0]) + queue_offset

        processing_block = None
        waiting_queue = []

        events = [
            (0,    "arrival", 0),
            (2,    "arrival", 1),
            (2.05, "arrival", 2),
            (2.1,  "arrival", 3),
            (3,    "processing_finish", 0),
            (5,    "arrival", 4),
            (6,    "processing_finish", 1),
            (9,    "processing_finish", 2),
            (12,   "processing_finish", 3),
            (15,   "processing_finish", 4),
        ]

        for event in events:
            event_time, event_type, idx = event
            current = global_clock.get_value()
            if event_time > current:
                dt = event_time - current
                self.play(global_clock.animate.increment_value(dt), run_time=dt)
            if event_type == "arrival":
                if idx == 0:
                    processing_block = idx
                    self.play(blocks[idx].animate.move_to(processing_box_center), run_time=0.5)
                else:
                    waiting_queue.append(idx)
                    target_pos = get_waiting_slot(len(waiting_queue) - 1)
                    self.play(blocks[idx].animate.move_to(target_pos), run_time=0.5)
            elif event_type == "processing_finish":
                if processing_block is not None:
                    self.play(FadeOut(blocks[processing_block]), run_time=0.5)
                if waiting_queue:
                    next_block = waiting_queue.pop(0)
                    processing_block = next_block
                    self.play(blocks[next_block].animate.move_to(processing_box_center), run_time=0.5)
                    for i, b_idx in enumerate(waiting_queue):
                        self.play(blocks[b_idx].animate.move_to(get_waiting_slot(i)), run_time=0.3)
                else:
                    processing_block = None

        self.wait(2)
