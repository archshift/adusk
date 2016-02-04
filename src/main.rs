extern crate sdl2;

struct Screen {
	size: Rect,
}

trait Renderable {
	fn render(&self, area: &Rect);
}

struct Keyboard {
	area: RelArea,
	keys: Vec<Key>,
}

impl Renderable for Keyboard {
    fn render(&self, area: &Rect) {
    	for key in &self.keys {
    		key.render(&self.area.to_abs(area));
    	}
    }
}

struct Key {
	area: RelArea,
	label: Label,
}

impl Renderable for Key {
	fn render(&self, area: &Rect) {
		self.label.render(&self.area.to_abs(area));
	}
}

struct Label {
	text: String,
}

impl Renderable for Label {
	fn render(&self, area: &Rect) {

	}
}

struct Rect {
	pos: (f32, f32),
	size: (f32, f32),
}

struct RelCoords {
	rel_coords: (f32, f32),
}

impl RelCoords {
	fn new(abs: (f32, f32), area: &Rect) -> RelCoords {
		let (abs_x, abs_y) = abs;
		RelCoords {
			rel_coords: ((abs_x - area.pos.0) / area.size.0, (abs_y - area.pos.1) / area.size.1),
		}
	}

	fn copy(rel: (f32, f32)) -> RelCoords {
		RelCoords {
			rel_coords: rel,
		}
	}

	fn to_abs(&self, area: &Rect) -> (f32, f32) {
		(self.rel_coords.0 * area.size.0 + area.pos.0, self.rel_coords.1 * area.size.1 + area.pos.1)
	}
}

struct RelArea {
	pos: RelCoords,
	size: (f32, f32),
}

impl RelArea {
	fn new(abs: Rect, area: &Rect) -> RelArea {
		let (abs_w, abs_h) = abs.size;

		RelArea {
			pos: RelCoords::new(abs.pos, area),
			size: (abs_w / area.size.0, abs_h / area.size.1),
		}
	}

	fn copy(rel_pos: (f32, f32), rel_size: (f32, f32)) -> RelArea {
		RelArea {
			pos: RelCoords::copy(rel_pos),
			size: rel_size,
		}
	}

	fn to_abs(&self, area: &Rect) -> Rect {
		Rect {
			pos: self.pos.to_abs(area),
			size: (self.size.0 * area.size.0, self.size.1 * area.size.1),
		}
	}
}

fn main() {
	let sdl_context = sdl2::init().unwrap();
	let sdl_video_context = sdl_context.video().unwrap();

	let mut window = match sdl_video_context.window("adusk", 640, 480)
			.position_centered()
			.borderless()
			.opengl()
			.build() {
		Ok(window) => window,
		Err(err) => panic!("failed to create window: {}", err)
	};

	window.show();

	let mut renderer = match window.renderer().accelerated().build() {
		Ok(renderer) => renderer,
		Err(err) => panic!("failed to create renderer: {}", err)
	};

	'event : loop {
		for event in sdl_context.event_pump().unwrap().poll_iter() {
			match event {
				sdl2::event::Event::Quit{..} => break 'event,
				_ => continue
			}
		}

		renderer.clear();
		renderer.present();
	}
}
