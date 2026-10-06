import random
import hashlib
import os
import platform
import shutil
import sys, time
from datetime import datetime

frames = [
r"""
                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~ 
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~

                                                      |_  |
                                                        | |
__                      ____                            | |
\ ````''''----....____.'\   ````''''--------------------| |--.               _____      .-.
 :.                      `-._                           | |   `''-----''''```     ``''|`: :|
  '::.                       `'--.._____________________| |                           | : :|
    '::..       ----....._______________________________| |                           | : :|
      `'-::...__________________________________________| |   .-''-..-'`-..-'`-..-''-.| : :|
           ```'''---------------------------------------| |--'                         `'-'
                                                        | |
                                                       _| |
                                                      |___|
""",

r"""
██╗██╗   ██╗ █████╗ ███╗   ██╗    ████████╗███████╗██████╗ ███╗   ███╗
██║██║   ██║██╔══██╗████╗  ██║    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██║██║   ██║███████║██╔██╗ ██║       ██║   █████╗  ██████╔╝██╔████╔██║
██║╚██╗ ██╔╝██╔══██║██║╚██╗██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
██║ ╚████╔╝ ██║  ██║██║ ╚████║       ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                                      
""",
]

def place_knife(frame, shift):
    skull_text, knife_text = frame.strip("\n").split("\n\n", 1)
    skull_lines = skull_text.splitlines()
    knife_lines = knife_text.splitlines()
    knife_offset = max(0, (len(skull_lines) - len(knife_lines)) // 2)
    skull_width = max(map(len, skull_lines))
    knife_start = skull_width + 4 + shift
    combined_lines = []

    for line_number in range(max(len(skull_lines), knife_offset + len(knife_lines))):
        canvas = list(skull_lines[line_number]) if line_number < len(skull_lines) else []
        knife_index = line_number - knife_offset
        if 0 <= knife_index < len(knife_lines):
            for character_index, character in enumerate(knife_lines[knife_index]):
                target_index = knife_start + character_index
                if target_index < 0 or character == " ":
                    continue
                if target_index < len(canvas) and canvas[target_index] != " ":
                  continue
                if target_index >= len(canvas):
                    canvas.extend(" " * (target_index - len(canvas) + 1))
                canvas[target_index] = character
        combined_lines.append("".join(canvas).rstrip())

    return "\n" + "\n".join(combined_lines) + "\n"


skull_frame = frames[0]
message_frame = frames[1]
additional_message_frames = frames[2:]
knife_shifts = tuple(round(-54 * frame_index / 59) for frame_index in range(60))
debris_marker = "\x01"


def add_debris(frame, stage):
  frame_lines = [list(line) for line in frame.strip("\n").splitlines()]
  skull_lines = skull_frame.strip("\n").split("\n\n", 1)[0].splitlines()
  skull_width = max(map(len, skull_lines))
  impact_row = len(skull_lines) // 2
  impact_col = skull_width - 2
  particles = (
    (-7, 2, -12, 18, "#"),
    (-5, 0, -10, 14, "@"),
    (-3, 0, -7, 11, "*"),
    (-1, 2, -3, 20, "X"),
    (1, 3, -1, 25, "+"),
    (3, 1, 6, 18, "*"),
    (5, 0, 11, 15, "@"),
    (7, 2, 13, 20, "#"),
    (-2, 4, -8, 28, "/"),
    (2, 4, 9, 29, "\\"),
    (0, 1, -3, 10, "o"),
    (4, 2, 8, 24, "O"),
    (-6, 5, -15, 32, "*"),
    (-4, 3, -9, 24, "#"),
    (0, 5, 2, 34, "@"),
    (2, 5, 14, 31, "X"),
    (6, 4, 16, 27, "+"),
    (8, 1, 18, 24, "o"),
    (-8, 4, -14, 20, "#"),
    (-6, 6, -11, 18, "@"),
    (-2, 6, -5, 17, "*"),
    (2, 6, 6, 19, "X"),
    (5, 5, 12, 21, "#"),
    (8, 4, 15, 18, "@"),
    (0, 1, -10, 13, "#"),
    (0, 1, -8, 11, "@"),
    (0, 1, -6, 9, "*"),
    (0, 1, -4, 7, "X"),
    (0, 1, -2, 5, "+"),
    (0, 1, 0, 3, "o"),
    (0, 1, 2, 5, "+"),
    (0, 1, 4, 7, "X"),
    (0, 1, 6, 9, "*"),
    (0, 1, 8, 11, "@"),
    (0, 1, 10, 13, "#"),
    (-1, 7, 3, 22, "+"),
    (4, 7, 9, 23, "o"),
  )
  progress = stage / (len(knife_shifts) - 1)
  debris_spread = 0.65
  horizontal_spread = 0.8
  triangle_start = len(particles) - 11
  debris_random = random.Random(31415)
  horizontal_offsets = [debris_random.randint(-2, 8) for _ in particles]
  for particle_index, (start_row, start_col, end_row, end_col, character) in enumerate(particles):
    speed = 0.55 if particle_index % 5 == 0 else 1.0
    particle_progress = min(1.0, progress * speed)
    if particle_progress < 0.15:
      continue
    row = impact_row + round(start_row + (end_row - start_row) * particle_progress * debris_spread)
    if particle_index >= triangle_start:
      randomized_end_col = abs(end_row) + 3
    else:
      randomized_end_col = end_col + horizontal_offsets[particle_index]
    column = impact_col + round(start_col + (randomized_end_col - start_col) * particle_progress * horizontal_spread)
    if row < 0 or column < 0:
      continue
    while row >= len(frame_lines):
      frame_lines.append([])
    if column >= len(frame_lines[row]):
      frame_lines[row].extend(" " * (column - len(frame_lines[row]) + 1))
    frame_lines[row][column] = debris_marker + character

  return "\n" + "\n".join("".join(line).rstrip() for line in frame_lines) + "\n"


knife_frames = [
  add_debris(place_knife(skull_frame, shift), stage)
  for stage, shift in enumerate(knife_shifts)
]


def reveal_message(frame, message, visible_lines):
  frame_lines = frame.strip("\n").splitlines()
  message_lines = message.strip("\n").splitlines()
  frame_width = max(map(len, frame_lines))

  frame_lines.append("")
  for line in message_lines[:visible_lines]:
    frame_lines.append(" " * max(0, (frame_width - len(line)) // 2) + line)

  return "\n" + "\n".join(frame_lines) + "\n"


def reveal_message_smooth(frame, message):
  message_lines = message.strip("\n").splitlines()
  total_characters = sum(len(line) for line in message_lines)
  reveal_step = max(1, total_characters // 20)
  smooth_frames = []

  for visible_characters in range(reveal_step, total_characters + reveal_step, reveal_step):
    remaining_characters = min(visible_characters, total_characters)
    frame_lines = frame.strip("\n").splitlines()
    frame_width = max(map(len, frame_lines))
    frame_lines.append("")

    for line in message_lines:
      if remaining_characters <= 0:
        break
      visible_line = line[:remaining_characters]
      padding = max(0, (frame_width - len(line)) // 2)
      frame_lines.append(" " * padding + visible_line)
      remaining_characters -= len(line)

    smooth_frames.append("\n" + "\n".join(frame_lines) + "\n")

  return smooth_frames


message_frames = [
  reveal_message(knife_frames[-1], message_frame, visible_lines)
  for visible_lines in range(1, len(message_frame.strip("\n").splitlines()) + 1)
]
for additional_message in additional_message_frames:
  message_frames.extend(reveal_message_smooth(message_frames[-1], additional_message))
frames = knife_frames + message_frames


def render_frame(frame):
  rendered = []
  marker_found = False

  for character in frame:
    if character == debris_marker:
      rendered.append("\033[91m")
      marker_found = True
    elif marker_found:
      rendered.append(character)
      rendered.append("\033[38;2;180;255;180m")
      marker_found = False
    else:
      rendered.append(character)

  return "".join(rendered)


def terminal_hud(started_at, telemetry_visible):
  terminal_size = shutil.get_terminal_size()
  elapsed = time.perf_counter() - started_at
  finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(__file__, "rb") as source_file:
    source_hash = hashlib.sha256(source_file.read()).hexdigest()[:16]
  effective_fps = len(frames) / elapsed if elapsed else 0
  working_directory = os.getcwd()
  executable = os.path.basename(sys.executable)
  telemetry_lines = (
    f"| PID        : {os.getpid():<34}|",
    f"| EXECUTABLE : {executable:<34}|",
    f"| FPS        : {effective_fps:>7.2f}                        |",
    f"| SOURCE ID  : {source_hash:<25}|",
    f"| WORKDIR    : {working_directory[:33]:<33}|",
  )
  return (
    "\n\n"
    "+--------------- RUNTIME REPORT -----------------+\n"
    f"| PYTHON     : {platform.python_version():<34}|\n"
    f"| PLATFORM   : {platform.system()} {platform.release():<25}|\n"
    f"| TERMINAL   : {terminal_size.columns}x{terminal_size.lines:<29}|\n"
    f"| FRAMES     : {len(frames):<34}|\n"
    f"| ELAPSED    : {elapsed:>7.2f} seconds                  |\n"
    f"| COMPLETED  : {finished_at:<30}|\n"
    "+-------------------------------------------------+\n"
    "\n"
    "+-------------- SESSION TELEMETRY ---------------+\n"
    + "\n".join(telemetry_lines[:telemetry_visible])
    + ("\n" if telemetry_visible else "")
    + "+-------------------------------------------------+"
  )

started_at = time.perf_counter()
sys.stdout.write("\033[?251")
try:
	for  _ in range(1):
		for frame_index, frame in enumerate(frames):
			sys.stdout.write("\033[H\033[2J")
			sys.stdout.write("\033[38;2;180;255;180m" + render_frame(frame) + "\033[0m")
			sys.stdout.flush()
			time.sleep(0.03 if frame_index < len(knife_frames) else 0.18)
	for telemetry_visible in range(0, 6):
		sys.stdout.write("\033[H\033[2J\033[38;2;180;255;180m" + render_frame(frames[-1]) + "\033[0m" + terminal_hud(started_at, telemetry_visible))
		sys.stdout.flush()
		time.sleep(0.18)
finally:
	sys.stdout.write("\033[?25h\033[0m\n")