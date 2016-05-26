use sdl2;
use sdl2::pixels::Color;

use ui;
use utils::units::{Rect, RelArea};

const DEFAULT_BG_COLOR: Color = Color::RGB(0x0f, 0x28, 0x3c);

pub struct Keyboard {
    area: RelArea,
    keys: Vec<Vec<ui::Key>>,
}

impl Keyboard {
    pub fn new() -> Keyboard {
        Keyboard {
            area: RelArea::copy((0.02, 0.02), (0.96, 0.96)),
            keys: Vec::<Vec<ui::Key>>::new(),
        }
    }

    fn total_width_weights(row: &Vec<ui::Key>) -> f32 {
        row.into_iter().fold(0f32, |acc, key| acc + key.width_weight())
    }

    pub fn keys(&self) -> &Vec<Vec<ui::Key>> { &self.keys }

    pub fn set_keys(&mut self, key_rows: Vec<Vec<ui::Key>>) {
        self.keys = key_rows;

        let spacing = 0.015f32;

        let rows = self.keys.len() as f32;
        let total_v_spacing = spacing * (rows + 1.0);
        // Divide non-whitespace by num rows
        let key_height = (1.0 - total_v_spacing) / rows;

        let mut y_pos = spacing;
        for ref mut row in self.keys.iter_mut() {
            let total_width_weights = Keyboard::total_width_weights(&row);
            let total_h_spacing = spacing * (row.len() as f32 + 1.0);
            let avg_key_width = (1.0 - total_h_spacing) / total_width_weights;

            let mut x_pos = spacing;
            for ref mut key in row.iter_mut() {
                let key_width = avg_key_width * key.width_weight();

                key.set_area(RelArea::copy((x_pos, y_pos), (key_width, key_height)));

                x_pos += key_width + spacing;
            }

            y_pos += key_height + spacing;

            // Make sure we iterated through the correct amount of units
            assert_eq!(x_pos.round(), 1.0);
        }

        // Make sure we iterated through the correct amount of units
        assert_eq!(y_pos.round(), 1.0);
    }
}

impl ui::Renderable for Keyboard {
    fn render(&self, renderer: &mut sdl2::render::Renderer, area: &Rect) {
        renderer.set_draw_color(DEFAULT_BG_COLOR);

        let float_rect = self.area.to_abs(area);

        renderer.fill_rect(sdl2::rect::Rect::new_unwrap(
            float_rect.pos.0.round() as i32, float_rect.pos.1.round() as i32,
            float_rect.size.0.round() as u32, float_rect.size.1.round() as u32
            ));

        for row in &self.keys {
            for key in row {
                key.render(renderer, &float_rect);
            }
        }
    }
}
