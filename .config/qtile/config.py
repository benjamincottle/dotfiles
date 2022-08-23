import os
import subprocess
from libqtile import qtile, bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.popup.toolkit import PopupGridLayout, PopupRelativeLayout, PopupImage, PopupText, PopupWidget

@lazy.window.function
def move_floating_window(window, x: int = 0, y: int = 0):
    new_x = window.float_x + x
    new_y = window.float_y + y
    window.cmd_set_position_floating(new_x, new_y)


@lazy.window.function 
def resize_floating_window(window, width: int = 0, height: int = 0): 
    window.cmd_set_size_floating(window.width + width, window.height + height)


def cal():
    curr_cal=subprocess.run(["cal", "--one", "--monday"], stdout=subprocess.PIPE)
    return curr_cal.stdout.decode()


def show_cal(qtile):
    controls = [
        PopupWidget(
            pos_x=0.05,
            pos_y=0.05,
            width=1.0,
            height=1.0,
            widget=widget.GenPollText(
                foreground=colour[2],
                func=cal,
            ),
            can_focus=True,
            highlight=None,
        ),
    ]

    layout = PopupRelativeLayout(
                 qtile,
                 margin=0,
                 width=180,
                 height=155,
                 controls=controls,
                 background=colour[0],
                 initial_focus=None,
                 close_on_click=True,
              )

    layout.show(x=1155, y=30, centered=False, warp_pointer=False)


def show_graphs(qtile):
    controls = [
        PopupText(
            text="    CPU",
            font="Hack Nerd Font Mono",
            fontsize=14,
            foreground=colour[2],
            row=0,
            col=0,
        ),
        PopupText(
            text="    Memory",
            font="Hack Nerd Font Mono",
            fontsize=14,
            foreground=colour[2],
            row=0,
            col=1,
        ),
        PopupWidget(
            row=1,
            col=0,
            row_span=5,
            widget=widget.CPUGraph(
                border_color=nord[3],
                fill_color=nord[3],
                graph_color=nord[3],
                type="linefill",
            ),
            can_focus=True,
            highlight=None,
        ),
        PopupWidget(
            row=1,
            col=1,
            row_span=5,
            widget=widget.MemoryGraph(
                border_color=nord[3],
                fill_color=nord[3],
                graph_color=nord[3],
                type="linefill",
            ),
            can_focus=True,
            highlight=None,
        )
    ]

    layout = PopupGridLayout(
                 qtile,
                 margin=5,
                 width=600,
                 height=200,
                 rows=6,
                 cols=2,
                 controls=controls,
                 background=colour[0],
                 initial_focus=None,
                 close_on_click=True,
              )

    layout.show(centered=True)


mod = "mod4"
terminal = guess_terminal()
browser = "google-chrome-stable"
filemanager = "pcmanfm"
text_editor = "subl"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "control"], "space", lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod], "o", lazy.layout.grow(), desc="grow window"),
    Key([mod], "i", lazy.layout.shrink(), desc="shrink window"),
    Key([mod], "m", lazy.layout.maximize(), desc="maximise window"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset secondary window sizes"),
    Key([mod, "shift"], "space", lazy.layout.flip()),

    Key([mod, 'shift'], "u", move_floating_window(x=10), desc="move window right"),
    Key([mod, 'shift'], 'y', move_floating_window(x=-10), desc="move window left"),
    Key([mod, 'shift'], 'i', move_floating_window(y=10), desc="move window down"),
    Key([mod, 'shift'], 'o', move_floating_window(y=-10), desc="move window up"),
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    Key([mod, "control"], "h", resize_floating_window(width=-10), desc='decrease window width'), 
    Key([mod, "control"], "l", resize_floating_window(width=10), desc='increase window width'), 
    Key([mod, "control"], "j", resize_floating_window(height=-10), desc='decrease window height'),
    Key([mod, "control"], "k", resize_floating_window(height=10), desc='increase window height'), 
    # Keyboard multimedia keys
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Toggle mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl -- set-sink-volume @DEFAULT_SINK@ -5%"), desc="Lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl -- set-sink-volume @DEFAULT_SINK@ +5%"), desc="Raise volume"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5"), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5"), desc="Increase brightness"),
    # Launch importants
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "period", lazy.spawn("rofi -show drun -theme ~/.config/rofi/rofi.rasi"), desc="App launcher"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "f", lazy.spawn(filemanager), desc="Launch filemanager"),
    Key([mod], "s", lazy.spawn(text_editor), desc="Launch text editor"),
    Key([mod, "shift"], "g", lazy.function(show_graphs)),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.spawn(terminal + " -e shutdown now"), desc="Shutdown computer"),
    Key([mod, "control", "shift"], "q", lazy.shutdown(), desc="Quit qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout.")
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

nord = [
    "#2e3440", "#3b4252", "#434c5e", "#4c566a",           # Polar Night
    "#d8dee9", "#e5e9f0", "#eceff4",                      # Snow Storm
    "#8fbcbb", "#88c0d0", "#81a1c1", "#5e81ac",           # Frost
    "#bf616a", "#d08770", "#ebcb8b", "#a3be8c", "#b48ead" # Aurora
    ]

colour = [
        "#212529", "#6c6f74", "#81858b"
        ]

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colour[2],
    "border_normal": nord[3],
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
]

widget_defaults = dict(
    font="Hack Nerd Font Mono",
    fontsize=14,
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=10),
                widget.CurrentLayoutIcon(
                    foreground=colour[2],
                    use_mask=True,
                    scale=0.8,
                ),
                widget.Spacer(length=5),
                widget.CurrentLayout(
                    foreground=colour[2], 
                    width=75,
                ),
                widget.Spacer(length=5),
                widget.GroupBox(
                    active=colour[2],
                    borderwidth=1,
                    inactive=nord[3],
                    this_screen_border=colour[2],
                    this_current_screen_border=colour[2],
                    urgent_border=nord[11],
                    urgent_text=nord[11],
                    other_screen_border=nord[3],
                    other_current_screen_border=nord[3],
                    hide_unused=True,
                    fontsize=10,
                    padding_y=2,
                    padding_x=6,
                    margin_x=0,
                    margin_y=3,
                ),
                widget.Spacer(length=10),
                widget.Prompt(
                    padding=20,
                    foreground=colour[2], 
                    cursor_color=colour[2],
                    prompt="run: ",
                ),
                widget.WindowName(
                    foreground=colour[2]
                ),
                #widget.Chord(
                #    chords_colors={
                #        "launch": ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                #),
                widget.TextBox(
                    text="盛",
                    foreground=colour[2],
                    fontsize=22,
                ),
                widget.Spacer(length=5),
                widget.Backlight(
                    backlight_name="intel_backlight",
                    foreground=colour[2],
                    markup=True,
                    step=5,
                    format="{percent:2.0%}",
                ),
                widget.Spacer(length=11),
                widget.WiFiIcon(
                    active_colour=colour[2],
                    expanded_timeout=3,
                    foreground=colour[2],
                    inactive_colour=nord[3],
                    padding_y=5,
                ),
                widget.Spacer(length=9),
                widget.PulseVolume(
                    emoji=True,
                    foreground=colour[2],
                    volume_app="pavucontrol",
                    fontsize=16,
                ),
                widget.Spacer(length=10),
                widget.UPowerWidget(
                    battery_height=10,
                    battery_width=20,
                    border_charge_colour=nord[7],
                    border_colour=colour[2],
                    border_critical_colour=nord[11],
                    fill_critical=nord[11],
                    fill_low=nord[12],
                    fill_normal=colour[2],
                    text_displaytime=3,
                    foreground=colour[2],
                ),
                widget.Spacer(length=10),
                widget.CheckUpdates(
                    update_interval = 1800,
                    distro = "Arch_checkupdates",
                    display_format = "",
                    no_update_string = "",
                    foreground=colour[2],
                    fontsize=28,
                    colour_have_updates=nord[7],
                    colour_no_updates=colour[2],
                    mouse_callbacks = {'Button1': lambda:
                        qtile.cmd_spawn(terminal + ' -e yay')},
                ),
                widget.Systray(),
                widget.Spacer(length=10),
                widget.Clock(
                        format="%a %d %b, %H:%M:%S", 
                        foreground=colour[2],
                        update_interval=5,
                        mouse_callbacks = {'Button1': lazy.function(show_cal)},
                ),
                widget.Spacer(length=10),
                widget.KeyboardLayout(
                    foreground=colour[2],
                    configured_keyboards=['us', 'dk'],
                    display_map={'us': 'en', 'dk': 'dk'},
                    mouse_callbacks = {'Button1': lazy.widget["keyboardlayout"].next_keyboard()},
                ),
                widget.Spacer(length=15),
                #widget.QuickExit(
                #    default_text=" [ x ] ", 
                #    countdown_start=3, 
                #    countdown_format=" [ {} ] ", 
                #    foreground=colour[2],
                #    mouse_callbacks = {'Button3': lambda:
                #        qtile.cmd_spawn(terminal + ' -e shutdown -h now')},
                #),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background = colour[0],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Volume Control"),
        Match(title="iwgtk"),
        Match(title="Customize Look and Feel"),
        Match(title="Qalculate!"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

