use sdl2;

use utils::units::Rect;

pub trait Renderable {
    fn render(&self, renderer: &mut sdl2::render::Renderer, area: &Rect);
}
