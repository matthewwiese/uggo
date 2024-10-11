from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from .chart import Chart

@dataclass
class ScatterChart(Chart):
    point_color: str = 'blue'
    point_size: int = 5

    def __post_init__(self):
        super().__post_init__()
        self.max_x = max(x for x, _ in self.data) if self.data else 0
        self.max_y = max(y for _, y in self.data) if self.data else 0

    def draw_data(self, draw):
        chart_width = self.width - 2 * self.margin
        chart_height = self.height - 2 * self.margin

        for x, y in self.data:
            x_pos = self.margin + (x / self.max_x) * chart_width
            y_pos = self.height - self.margin - (y / self.max_y) * chart_height
            
            draw.ellipse([x_pos - self.point_size, y_pos - self.point_size,
                          x_pos + self.point_size, y_pos + self.point_size],
                         fill=self.point_color)

    def draw_labels(self, draw, image):
        super().draw_labels(draw, image, skip_y_labels=True)
        
        label_font = ImageFont.truetype("arial.ttf", 12)
        
        # Draw x-axis labels
        for x, _ in self.data:
            x_pos = self.margin + (x / self.max_x) * (self.width - 2 * self.margin)
            y_pos = self.height - self.margin + 15
            draw.text((x_pos, y_pos), str(x), fill='black', font=label_font, anchor='mt')

        # Draw y-axis labels
        for y, _ in self.data:
            y_pos = self.height - self.margin - y * (self.height - 2 * self.margin) / self.max_y
            draw.text((self.margin - 5, y_pos), str(y), fill='black', font=label_font, anchor='rm')

    def draw(self):
        image = super().draw()
        return image
