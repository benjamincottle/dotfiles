import os
import psutil
import subprocess
from libqtile import qtile, bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.popup.toolkit import PopupGridLayout, PopupRelativeLayout, PopupImage, PopupText, PopupWidget


def show_graphs(qtile):
    controls = [
        PopupWidget(
            row=0,
            col=0,
            widget=widget.CPU(
                foreground=colour[2],
                format="    CPU {freq_current}GHz {load_percent}%"
            ),
            can_focus=True,
            highlight=None,
        ),
        PopupWidget(
            row=0,
            col=1,
            widget=widget.Memory(
                foreground=colour[2],
                format="   MEM {MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}" 
            ),
            can_focus=True,
            highlight=None,
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
        ),

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
terminal = "alacritty"
browser = "qutebrowser"
filemanager = "pcmanfm"
app_launcher = "rofi -show drun -theme ~/.config/rofi/rofi.rasi"
passwd_manager = "rofi-pass" 

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod], "o", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "i", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "m", lazy.layout.maximize(), desc="Maximise window"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc="Reset secondary window sizes"),
    Key([mod, "shift"], "space", lazy.layout.flip(), desc="Flip main window and stack"),
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    Key([mod], "x", lazy.window.toggle_fullscreen(), desc='Toggle fullscreen'),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "Left", lazy.screen.prev_group(), desc="Switch to previous group"),
    Key([mod], "Right", lazy.screen.next_group(), desc="Switch to next group"),
    Key([mod], "Down", lazy.screen.toggle_group(), desc="Switch last visited group"),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "period", lazy.spawn(app_launcher), desc="App launcher"),
    Key([mod], "comma", lazy.spawn(passwd_manager), desc="Password manager"),
    Key([mod], "q", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "f", lazy.spawn(filemanager), desc="Launch file manager"),
    Key([mod], "g", lazy.function(show_graphs), desc="Show simple performance graphs"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),

    Key([mod], "Tab", lazy.next_layout(), desc="Move to next layout"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(), desc="Move to previous layout"),

    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Toggle mute"),
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle"), desc="Toggle mic mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl -- set-sink-volume @DEFAULT_SINK@ -5%"), desc="Lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl -- set-sink-volume @DEFAULT_SINK@ +5%"), desc="Raise volume"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5"), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5"), desc="Increase brightness"),

    Key([mod, "control"], "b", lazy.hide_show_bar(position="top"), desc="Toggle qtile bar"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Quit qtile"),
    Key([mod, "control"], "s", lazy.spawn("shutdown now"), desc="Shutdown computer"),
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
                desc="Switch & move focused window to group {}".format(i.name),
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

groups.append(
    ScratchPad(
        'scratchpad', [
            DropDown(
                'calendar', 
                'yad --no-buttons --calendar', 
                x=0.88, 
                y=0.01, 
                width=0.1, 
                height=0.2, 
                opacity=1,
            )
        ]
    )
)

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
            padding_x=6,
            padding_y=2,
            margin_x=0,
            margin_y=3,
            invert_mouse_wheel=True,
            disable_drag=True,
            hide_unused=True,
            highlight_method="block",
            active=colour[2],
            inactive=nord[3],
            block_highlight_text_color=colour[2],
            other_screen_border=nord[3],
            other_current_screen_border=nord[3],
            this_screen_border=nord[0],
            this_current_screen_border=nord[0],
            urgent_border=nord[11],
            urgent_text=nord[11],
        ),
        widget.Spacer(length=10),
        widget.Prompt(
            padding=20,
            foreground=colour[2], 
            cursor_color=colour[2],
            prompt="run: ",
        ),
        widget.TaskList(
            foreground=colour[2],
            border=nord[0],
            margin=0,
            padding=3,
            padding_x=10,
            highlight_method="block",
            icon_size=0,
            txt_floating="???? ",
            txt_maximized="???? ",
            txt_minimized="???? ",
            urgent_alert_method="border",
            urgent_border=nord[11],
        ),
        widget.Spacer(length=5),
        widget.TextBox(
            text="???",
            foreground=colour[2],
            fontsize=22,
            mouse_callbacks = {'Button4': lambda:
                qtile.cmd_spawn("xbacklight -dec 3"),
                               'Button5': lambda: 
                qtile.cmd_spawn("xbacklight -inc 3")},
        ),
        widget.Spacer(length=5),
        widget.Backlight(
            backlight_name="intel_backlight",
            foreground=colour[2],
            markup=True,
            step=5,
            format="{percent:2.0%}",
            mouse_callbacks = {'Button4': lambda:
                qtile.cmd_spawn("xbacklight -dec 3"),
                               'Button5': lambda: 
                qtile.cmd_spawn("xbacklight -inc 3")},
        ),
        widget.Spacer(length=11),
        widget.TextBox(
            text="???",
            foreground=colour[2],
            fontsize=22,
            mouse_callbacks = {'Button3': lambda:
                qtile.cmd_spawn("pavucontrol")},
        ),
        widget.Spacer(length=5),
        widget.PulseVolume(
            foreground=colour[2],
            volume_app="pavucontrol",
        ),
        widget.Spacer(length=11),
        widget.Wlan(
            foreground=colour[2],
            fontsize=28,
            format="???",
            disconnected_message="???",
            interface="wlan0",
            mouse_callbacks = {'Button1': lambda:
                qtile.cmd_spawn("iwgtk")},
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
            display_format = "???",
            no_update_string = "???",
            foreground=colour[2],
            fontsize=28,
            colour_have_updates=nord[7],
            colour_no_updates=colour[2],
            mouse_callbacks = {'Button1': lambda:
                qtile.cmd_spawn(terminal + ' -e yay')},
        ),
        widget.Systray(
            padding=5,
            icon_size=26,
        ),
        widget.Spacer(length=10),
        widget.Clock(
            format="%a %d %b, %H:%M:%S", 
            foreground=colour[2],
            update_interval=5,
            mouse_callbacks = {'Button1': lazy.group['scratchpad'].dropdown_toggle('calendar')},
        ),
        widget.Spacer(length=10),
        widget.KeyboardLayout(
            foreground=colour[2],
            configured_keyboards=['us', 'dk'],
            display_map={'us': 'en', 'dk': 'dk'},
            mouse_callbacks = {'Button1': lazy.widget["keyboardlayout"].next_keyboard()},
        ),
        widget.Spacer(length=15),
    ],
    24,
    background = colour[0],
)

screens = [
    Screen(top=top,
    wallpaper="~/.config/qtile/wallpaper.png",
    wallpaper_mode="fill",
    )
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    border_width= 0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(title="Volume Control"),
        Match(title="iwgtk"),
        Match(title="Customize Look and Feel"),
        Match(title="Qalculate!"),
        Match(wm_class="Pinentry-gtk-2"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True



def floating_dialogs(window):
        window.floating = True



@hook.subscribe.client_new
def _swallow(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if not (dialog or transient):
        pid = window.window.get_net_wm_pid()
        ppid = psutil.Process(pid).ppid()
        cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
        for i in range(5):
            if not ppid:
                return
            if ppid in cpids:
                parent = window.qtile.windows_map.get(cpids[ppid])
                parent.minimized = True
                window.parent = parent
                return
            ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.startup
def startup():
    top.show(False)

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

