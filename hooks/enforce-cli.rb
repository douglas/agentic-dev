#!/usr/bin/env ruby
# frozen_string_literal: true

# PreToolUse hook to enforce CLI preferences.
# Extracts command verbs by stripping quoted strings first, then splitting on
# shell operators to find the first token of each pipeline segment.

require "json"

def strip_quoted(command)
  command
    .gsub(/'[^']*'/, '""')
    .gsub(/"(?:[^"\\]|\\.)*"/, '""')
    .gsub(/\$\([^)]*\)/, '""')
    .gsub(/`[^`]*`/, '""')
end

def command_verbs(command)
  strip_quoted(command).split(/\s*(?:\||&&|;)\s*/).filter_map do |segment|
    segment.split.each do |token|
      next if token.match?(/\A\w+=/)
      next if %w[env sudo nohup].include?(token)

      break token
    end
  end
end

def command_from(input)
  input.dig("tool_input", "command").to_s
end

begin
  command = command_from(JSON.parse($stdin.read))
  verbs = command_verbs(command)

  rules = [
    ["grep", "Blocked: use rg (ripgrep) instead of grep"],
    ["egrep", "Blocked: use rg (ripgrep) instead of egrep"],
    ["fgrep", "Blocked: use rg (ripgrep) instead of fgrep"],
    ["find", "Blocked: use fd instead of find"],
    ["cat", "Blocked: use bat instead of cat"],
    ["xdotool", "Blocked: X11 tools do not work on Wayland"],
    ["xrandr", "Blocked: X11 tools do not work on Wayland"],
    ["xclip", "Blocked: X11 tools do not work on Wayland; use wl-copy/wl-paste"],
    ["xsel", "Blocked: X11 tools do not work on Wayland; use wl-copy/wl-paste"],
    ["xinput", "Blocked: X11 tools do not work on Wayland"],
    ["xprop", "Blocked: X11 tools do not work on Wayland"],
    ["xwininfo", "Blocked: X11 tools do not work on Wayland"]
  ].freeze

  rules.each do |match, message|
    next unless verbs.include?(match)

    $stderr.puts message
    exit 2
  end

  if verbs.include?("cd") && verbs.include?("git")
    $stderr.puts "Blocked: do not combine cd and git; use git -C <path> instead"
    exit 2
  end
rescue StandardError => e
  $stderr.puts "enforce-cli.rb: #{e.class}: #{e.message}"
end

exit 0

