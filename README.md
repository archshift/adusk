# Steam Controller On-Screen Keyboard

Forked from [NOTtheMessiah/scosk](https://github.com/NOTtheMessiah/scosk)

## Dependencies

* GNU / Linux
* Python 3
* [PySDL2](http://http://pysdl2.readthedocs.org)
* [Standalone Steam Controller Driver](https://github.com/ynsta/steamcontroller)

## Usage

```
python3 adusk.py
```

## About

adusk aims to provide a standalone virtual keyboard for use with the Steam Controller; going above
and beyond Valve's existing implementation of a virtual keyboard, while also unencumbered
by the need to have Steam perpetually running in the background.

This program is still highly experimental, and does not have much practical use at the moment,
as it is not integrated with `sc-desktop.py` or similar standalone mouse drivers for the Steam
Controller.

#### What it does

- It's a virtual keyboard!

#### What it doesn't (yet!) do

- Integration with `sc-desktop.py`
- Easy configuration by the user
- Running as a daemon
- Conjuring via the Steam Controller itself
- Moving/scaling the keyboard with the controller
- Alternate symbols
- General user-friendliness