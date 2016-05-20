use sdl2;

use ui;
use utils::units::{Rect, RelArea};

use sdl2::pixels::Color;

const DEFAULT_THEME: KeyTheme = KeyTheme {
    background_color: Color::RGB(0x19, 0x3d, 0x55),
};

pub struct Key {
    area: RelArea,
    label: ui::Label,
    width_weight: f32,
    theme: KeyTheme,
}

impl Key {
    pub fn new(text: String) -> Key {
        Key {
            area: RelArea::copy((0.0, 0.0), (1.0, 1.0)),
            label: ui::Label::new(text),
            width_weight: 1.0,
            theme: DEFAULT_THEME,
        }
    }

    pub fn set_area(&mut self, area: RelArea) {
        self.area = area;
    }
    pub fn set_theme(&mut self, theme: KeyTheme) {
        self.theme = theme;
    }

    pub fn width_weight(&self) -> f32 { self.width_weight }
    pub fn set_width_weight(&mut self, width_weight: f32) {
        self.width_weight = width_weight;
    }
}

impl ui::Renderable for Key {
    fn render(&self, renderer: &mut sdl2::render::Renderer, area: &Rect) {
        renderer.set_draw_color(self.theme.background_color);

        let float_rect = self.area.to_abs(area);

        renderer.fill_rect(sdl2::rect::Rect::new_unwrap(
            float_rect.pos.0.round() as i32, float_rect.pos.1.round() as i32,
            float_rect.size.0.round() as u32, float_rect.size.1.round() as u32
            ));

        self.label.render(renderer, &self.area.to_abs(area));
    }
}

pub struct KeyTheme {
    background_color: Color,
}

