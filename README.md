# adusk

Forked from [NOTtheMessiah/scosk](https://github.com/NOTtheMessiah/scosk)

## Dependencies

* GNU / Linux
* Python 3
* [PySDL2](http://pysdl2.readthedocs.org), [SDL2_ttf](http://www.libsdl.org/projects/SDL_ttf/), [SDL2_gfx](http://www.ferzkopp.net/Software/SDL_gfx-2.0/)
* [Standalone Steam Controller Driver](https://github.com/ynsta/steamcontroller)

## About

adusk aims to provide a standalone virtual keyboard for use with the Steam Controller; going above
and beyond Valve's existing implementation of a virtual keyboard, while also unencumbered
by the need to have Steam perpetually running in the background.

This program is still highly experimental, and does not have much practical use at the moment,
as it is not integrated with `sc-desktop.py` or similar standalone mouse drivers for the Steam
Controller.

#### Installation

```
python3 setup.py install
```

#### Usage

```
adusk
```

#### Configuration

By default, adusk will look for data/configuration files in the following
locations (in order of descending priority):

**Environment-specified paths:**

- `$ADUSK_DATA/`

**User paths:**

- `~/.config/adusk/`
- `~/.adusk/`

**System paths:**

- `sys.prefix/adusk` (where `sys.prefix` is usually `/usr/local/`)

In the case of user paths, adusk will only search for configuration files within.
Otherwise, adusk will look in the folder for both configuration (within the `cfg/`
subfolder), and for other data used by the program.

#### What it does

- It's a virtual keyboard!

#### What it doesn't (yet!) do

- Integration with `sc-desktop.py`
- Running as a daemon
- Conjuring via the Steam Controller itself
- Moving/scaling the keyboard with the controller
- Alternate symbols
- General user-friendliness
