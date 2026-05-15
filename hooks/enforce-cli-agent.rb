#!/usr/bin/env ruby
# frozen_string_literal: true

# PreToolUse hook for agent/subagent tools.
# Injects CLI preferences as additional context so subagents follow the same
# tool conventions as the parent session.

require "json"

result = {
  "decision" => "approve",
  "message" => <<~MESSAGE.strip
    CLI preferences: use fd instead of find, rg instead of grep,
    bat instead of cat. Do not use X11 tools (xdotool, xrandr, xclip,
    xsel, xinput, xprop, xwininfo) because this is a Wayland system.
    Never combine cd and git in one command; use git -C <path> instead.
  MESSAGE
}

$stdout.puts JSON.generate(result)

