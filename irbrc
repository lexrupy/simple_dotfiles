# Completion
require 'irb/completion'

# History (nativo desde Ruby 3.4)
IRB.conf[:SAVE_HISTORY] = 1000
IRB.conf[:HISTORY_FILE] = File.expand_path("~/.irb_history")

# Prompt simples
IRB.conf[:PROMPT_MODE] = :SIMPLE

# Optional legacy gems (não quebram se faltarem)
%w[rubygems looksee/shortcuts wirble].each do |lib|
  begin
    require lib
  rescue LoadError
  end
end

# Helpers
class Object
  def local_methods(obj = self)
    (obj.methods - obj.class.superclass.instance_methods).sort
  end

  def ri(method = nil)
    unless method && method =~ /^[A-Z]/
      klass = self.is_a?(Class) ? name : self.class.name
      method = [klass, method].compact.join('#')
    end
    puts `ri '#{method}'`
  end
end

# Clipboard (Linux-compatible)
def copy(str)
  IO.popen('xclip -selection clipboard', 'w') { |f| f << str.to_s }
rescue
  warn "xclip não disponível"
end

def paste
  `xclip -selection clipboard -o`
rescue
  ""
end

# History copy (Reline-aware)
def copy_history
  history =
    if defined?(Reline)
      Reline::HISTORY.to_a
    else
      Readline::HISTORY.to_a
    end

  index = history.rindex("exit") || -1
  content = history[(index + 1)..-2].join("\n")
  puts content
  copy(content)
end

# Rails
load File.expand_path("~/.railsrc") if $0 == 'irb' && ENV['RAILS_ENV']

