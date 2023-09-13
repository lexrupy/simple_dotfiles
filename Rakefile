require 'rake'
require 'erb'

desc "install the dot files into user's home directory"
task :install do
  if File.exists?("#{ENV['HOME']}/.bash")
    puts "You already have a ~/.bash file or directory, you will need to remove it manually before continue. Make sure that it is not a system directory or you have personal data inside it."
    exit
  end
  system %Q{ln -s "$PWD" "$HOME/.bash"}

  replace_all = false

  Dir['*'].each do |file|
    next if %w[Rakefile README.rdoc LICENSE zsh profile completion config dot_config vendor bin].include? file

    if File.exist?(File.join(ENV['HOME'], ".#{file.sub('.erb', '')}"))
      if File.identical? file, File.join(ENV['HOME'], ".#{file.sub('.erb', '')}")
        puts "identical ~/.#{file.sub('.erb', '')}"
      elsif replace_all
        replace_file(file)
      else
        print "overwrite ~/.#{file.sub('.erb', '')}? [ynaq] "
        case $stdin.gets.chomp
        when 'a'
          replace_all = true
          replace_file(file)
        when 'y'
          replace_file(file)
        when 'q'
          exit
        else
          puts "skipping ~/.#{file.sub('.erb', '')}"
        end
      end
    else
      link_file(file)
    end
  end
  
  # Link .config folders
  Dir['dot_config/*'].each do |file|
    link_file(file, location='config')
  end
  
  # Link binary files
  Dir['bin/*'].each do |file|
    link_file(file, location='bin')
  end
  
  puts "To complete setup, put this line in your ~/.bashrc"
  puts "    . ~/.bash/profile"
  puts 'If you are using RVM and have in your .bashrc file the line:'
  puts '    "if [[ -n "$PS1" ]] ; then" '
  puts 'include the configuration line just before the last fi before '
  puts 'rvm stuff at end of file.'
end

def replace_file(file)
  system %Q{rm "$HOME/.#{file.sub('.erb', '')}"}
  link_file(file)
end

def link_file(file, location=nil)
  if file =~ /.erb$/
    puts "generating ~/.#{file.sub('.erb', '')}"
    File.open(File.join(ENV['HOME'], ".#{file.sub('.erb', '')}"), 'w') do |new_file|
      new_file.write ERB.new(File.read(file)).result(binding)
    end
  else
    puts "linking ~/.#{file}"
    if location == 'config'
     system %Q{ln -fs "$PWD/#{file}" "$HOME/#{file.sub('dot_', '.')}"}
    elsif location == 'bin'
      system %Q{mkdir -p $HOME/.local/bin}
      system %Q{ln -fs "$PWD/#{file}" "$HOME/.local/#{file}"}
    else
     system %Q{ln -fs "$PWD/#{file}" "$HOME/.#{file}"}
    end
  end
end

